"""
Test schema migration for friend-group multi-tenancy feature.

This test verifies:
1. New tables exist (friend_groups, group_members, group_servers, group_announcements, admin_alerts)
2. chat_messages table has group_id column
3. Migration is idempotent (safe to call init_db() multiple times)
4. One-time migration steps work correctly (chat wipe, moderator->user role flip)
"""
import pytest


class TestNewTablesExist:
    """Test that the new friend-group tables exist and chat_messages has group_id column."""
    
    def test_new_tables_exist_and_chat_has_group_id(self):
        """
        Connect via get_db(), assert the five tables exist and chat_messages has a group_id column.
        This test FAILS before migration is implemented.
        """
        from core.database import get_db, init_db
        
        # Call init_db to create tables and run migration
        init_db()
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check that the five new tables exist
        required_tables = [
            'friend_groups',
            'group_members',
            'group_servers',
            'group_announcements',
            'admin_alerts'
        ]
        
        for table in required_tables:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table,)
            )
            result = cursor.fetchone()
            assert result is not None, f"Table '{table}' does not exist"
        
        # Check that chat_messages has a group_id column
        cursor.execute("PRAGMA table_info(chat_messages)")
        columns = {row[1] for row in cursor.fetchall()}
        assert 'group_id' in columns, "chat_messages table missing 'group_id' column"
        
        conn.close()


class TestMigrationIdempotency:
    """Test that migration is idempotent (safe to call init_db() multiple times)."""
    
    def test_init_db_is_idempotent(self):
        """
        Call init_db() twice, verify no errors occur.
        This test FAILS before migration is implemented because tables don't exist yet.
        """
        from core.database import init_db
        
        # First call - should create tables
        init_db()
        
        # Second call - should be safe (no errors)
        init_db()
        
        # Verify tables exist after second call
        from core.database import get_db
        conn = get_db()
        cursor = conn.cursor()
        
        required_tables = [
            'friend_groups',
            'group_members',
            'group_servers',
            'group_announcements',
            'admin_alerts'
        ]
        
        for table in required_tables:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table,)
            )
            result = cursor.fetchone()
            assert result is not None, f"Table '{table}' does not exist after second init_db()"
        
        conn.close()


class TestMigrationOneTimeSteps:
    """Test the one-time migration steps (chat wipe, moderator->user role flip)."""
    
    def test_chat_wiped_and_moderator_role_migrated(self):
        """
        Insert a moderator user + 2 chat rows BEFORE first init_db() call.
        Assert after: 0 chat rows, user role is 'user'.
        Run twice to verify idempotency.
        """
        import os
        import tempfile
        import uuid
        from core.database import get_db, init_db
        from core.security import get_password_hash
        
        # Create a temp database for this test
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_migrate.db")
            os.environ["DATABASE_PATH"] = db_path
                
            # Create tables first (without running migration - use init_db and then reset migration flag)
            init_db()
                
            # Reset the migration flag so the migration runs when we call init_db again
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM system_config WHERE key = 'migration_v3_done'")
            conn.commit()
            conn.close()
                
            # Insert raw data
            conn = get_db()
            cursor = conn.cursor()
            
            # Create a moderator user (will be migrated to 'user')
            user_id = str(uuid.uuid4())
            password_hash = get_password_hash("Test1234!")
            created_at = "2026-01-01T00:00:00+00:00"
            cursor.execute(
                "INSERT INTO users (id, username, email, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, "moderator_user", "moderator_user@test.local", password_hash, "moderator", created_at)
            )
            
            # Insert 2 chat messages
            from datetime import datetime, timezone
            now = datetime.now(timezone.utc).isoformat()
            cursor.execute(
                "INSERT INTO chat_messages (id, user_id, message, created_at) VALUES (?, ?, ?, ?)",
                ("msg1", user_id, "First message", now)
            )
            cursor.execute(
                "INSERT INTO chat_messages (id, user_id, message, created_at) VALUES (?, ?, ?, ?)",
                ("msg2", user_id, "Second message", now)
            )
            conn.commit()
            
            cursor.execute("SELECT COUNT(*) FROM chat_messages")
            assert cursor.fetchone()[0] == 2, "Expected 2 chat messages before migration"
            
            conn.close()
            
            # First init_db() call - should run migration
            init_db()
            
            # Verify: 0 chat rows
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM chat_messages")
            chat_count = cursor.fetchone()[0]
            assert chat_count == 0, f"Expected 0 chat messages after migration, got {chat_count}"
            
            # Verify: moderator user is now 'user' role
            cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
            role = cursor.fetchone()[0]
            assert role == "user", f"Expected role 'user', got '{role}'"
            
            conn.close()
            
            # Second init_db() call - should be idempotent (no error)
            init_db()
            
            # Verify still 0 chat messages after second call
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM chat_messages")
            chat_count = cursor.fetchone()[0]
            assert chat_count == 0, f"Expected 0 chat messages after second init_db(), got {chat_count}"
            conn.close()


class TestSchemaStructure:
    """Verify the exact schema structure of new tables."""
    
    def test_friend_groups_schema(self):
        """Verify friend_groups table structure."""
        from core.database import get_db, init_db
        
        init_db()
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(friend_groups)")
        columns = {row[1]: row for row in cursor.fetchall()}
        
        assert 'id' in columns, "friend_groups missing 'id' column"
        assert 'name' in columns, "friend_groups missing 'name' column"
        assert 'description' in columns, "friend_groups missing 'description' column"
        assert 'created_by' in columns, "friend_groups missing 'created_by' column"
        assert 'created_at' in columns, "friend_groups missing 'created_at' column"
        
        # Check name is UNIQUE
        name_info = columns['name']
        assert name_info[3] == 1, "name column should be UNIQUE"
        
        conn.close()
    
    def test_group_members_schema(self):
        """Verify group_members table structure."""
        from core.database import get_db, init_db
        
        init_db()
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(group_members)")
        columns = {row[1]: row for row in cursor.fetchall()}
        
        assert 'id' in columns, "group_members missing 'id' column"
        assert 'group_id' in columns, "group_members missing 'group_id' column"
        assert 'user_id' in columns, "group_members missing 'user_id' column"
        assert 'role' in columns, "group_members missing 'role' column"
        assert 'joined_at' in columns, "group_members missing 'joined_at' column"
        
        conn.close()
    
    def test_group_servers_schema(self):
        """Verify group_servers table structure."""
        from core.database import get_db, init_db
        
        init_db()
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(group_servers)")
        columns = {row[1]: row for row in cursor.fetchall()}
        
        assert 'id' in columns, "group_servers missing 'id' column"
        assert 'group_id' in columns, "group_servers missing 'group_id' column"
        assert 'orchestrator_id' in columns, "group_servers missing 'orchestrator_id' column"
        assert 'server_uid' in columns, "group_servers missing 'server_uid' column"
        assert 'created_by' in columns, "group_servers missing 'created_by' column"
        assert 'created_at' in columns, "group_servers missing 'created_at' column"
        
        conn.close()
    
    def test_group_announcements_schema(self):
        """Verify group_announcements table structure."""
        from core.database import get_db, init_db
        
        init_db()
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(group_announcements)")
        columns = {row[1]: row for row in cursor.fetchall()}
        
        assert 'id' in columns, "group_announcements missing 'id' column"
        assert 'group_id' in columns, "group_announcements missing 'group_id' column"
        assert 'user_id' in columns, "group_announcements missing 'user_id' column"
        assert 'message' in columns, "group_announcements missing 'message' column"
        assert 'created_at' in columns, "group_announcements missing 'created_at' column"
        
        conn.close()
    
    def test_admin_alerts_schema(self):
        """Verify admin_alerts table structure."""
        from core.database import get_db, init_db
        
        init_db()
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(admin_alerts)")
        columns = {row[1]: row for row in cursor.fetchall()}
        
        assert 'id' in columns, "admin_alerts missing 'id' column"
        assert 'kind' in columns, "admin_alerts missing 'kind' column"
        assert 'message' in columns, "admin_alerts missing 'message' column"
        assert 'detail' in columns, "admin_alerts missing 'detail' column"
        assert 'created_at' in columns, "admin_alerts missing 'created_at' column"
        assert 'acknowledged_at' in columns, "admin_alerts missing 'acknowledged_at' column"
        
        conn.close()
