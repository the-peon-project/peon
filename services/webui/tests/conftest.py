"""
Test fixtures for PEON WebUI tests.
Provides in-process test harness for database and FastAPI app testing.
"""
import os
import sys
import tempfile
import pytest
from fastapi.testclient import TestClient


def pytest_configure():
    """Configure Python path for test imports."""
    # Add the backend directory to sys.path so core/ can be imported
    backend_dir = os.path.join(os.path.dirname(__file__), "..", "backend")
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)


def pytest_runtest_setup(item):
    """Set up temp database path before each test."""
    # Create a temporary database path for this test
    tmpdir = tempfile.mkdtemp()
    db_path = os.path.join(tmpdir, "test_peon.db")
    os.environ["DATABASE_PATH"] = db_path
    item.temp_db_path = tmpdir  # Store for cleanup


def pytest_runtest_teardown(item):
    """Clean up temp database after each test."""
    if hasattr(item, 'temp_db_path'):
        import shutil
        shutil.rmtree(item.temp_db_path, ignore_errors=True)


@pytest.fixture
def app_client():
    """Create a test client with in-process FastAPI app and initialized DB."""
    # Import and initialize app (DATABASE_PATH is already set by pytest_runtest_setup)
    from server import app
    from core.database import init_db
    
    # Initialize database
    init_db()
    
    # Create test client
    client = TestClient(app)
    yield client


class SeedHelper:
    """Helper class for seeding test data."""
    
    def __init__(self, app_client):
        self.app_client = app_client
    
    def make_user(self, username: str, role: str = "user", password: str = "Test1234!") -> str:
        """Insert a user with known password hash and return the user id."""
        import uuid
        from core.security import get_password_hash
        from core.database import get_db
        
        user_id = str(uuid.uuid4())
        password_hash = get_password_hash(password)
        created_at = "2026-01-01T00:00:00+00:00"
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (id, username, email, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, username, f"{username}@test.local", password_hash, role, created_at)
        )
        conn.commit()
        conn.close()
        return user_id
    
    def login(self, username: str, password: str = "Test1234!") -> dict:
        """Login as a user and return auth headers."""
        response = self.app_client.post(
            "/api/auth/login",
            json={"username": username, "password": password}
        )
        assert response.status_code == 200, f"Login failed: {response.text}"
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def raw_exec(self, query: str, params: tuple = ()):
        """Execute raw SQL (for seeding data before init_db)."""
        from core.database import get_db
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
    
    def raw_query(self, query: str, params: tuple = ()):
        """Execute raw SELECT query."""
        from core.database import get_db
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        return result
    
    def count_table(self, table: str) -> int:
        """Get row count of a table."""
        from core.database import get_db
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        conn.close()
        return count


@pytest.fixture
def seed(app_client):
    """Return a SeedHelper instance for test data seeding."""
    return SeedHelper(app_client)
