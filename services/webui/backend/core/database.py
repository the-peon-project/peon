import sqlite3
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def get_db():
    """Get database connection with row factory"""
    # Use DATABASE_PATH environment variable if set (for containers)
    # Otherwise fall back to ROOT_DIR / 'peon.db' for local development
    db_path_str = os.environ.get('DATABASE_PATH', str(ROOT_DIR / 'peon.db'))
    db_path = Path(db_path_str)
    
    # Ensure the parent directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # Better concurrency
    return conn

def dict_from_row(row):
    """Convert SQLite row to dictionary"""
    return dict(zip(row.keys(), row)) if row else None

def init_db():
    """Initialize database with all required tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            is_chat_banned INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Orchestrator instances table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orchestrators (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            base_url TEXT NOT NULL,
            api_key TEXT NOT NULL,
            description TEXT,
            version TEXT,
            is_active INTEGER DEFAULT 1,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_synced TEXT,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    
    # User-Orchestrator access table (multitenancy)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_orchestrator_access (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            orchestrator_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (orchestrator_id) REFERENCES orchestrators(id),
            UNIQUE(user_id, orchestrator_id)
        )
    ''')
    
    # Server links table (user access to specific servers)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS server_links (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            orchestrator_id TEXT NOT NULL,
            server_uid TEXT NOT NULL,
            permissions TEXT DEFAULT 'read',
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (orchestrator_id) REFERENCES orchestrators(id),
            UNIQUE(user_id, orchestrator_id, server_uid)
        )
    ''')
    
    # Cached servers table (synced every 5 minutes)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cached_servers (
            id TEXT PRIMARY KEY,
            orchestrator_id TEXT NOT NULL,
            server_data TEXT NOT NULL,
            synced_at TEXT NOT NULL,
            FOREIGN KEY (orchestrator_id) REFERENCES orchestrators(id)
        )
    ''')
    
    # System config table (for admin wizard and feature flags)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    
    # Gaming sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gaming_sessions (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            orchestrator_id TEXT NOT NULL,
            server_uid TEXT,
            scheduled_time TEXT NOT NULL,
            duration_minutes INTEGER DEFAULT 120,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            status TEXT DEFAULT 'scheduled',
            FOREIGN KEY (orchestrator_id) REFERENCES orchestrators(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    
    # Session RSVPs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_rsvps (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            status TEXT DEFAULT 'attending',
            created_at TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES gaming_sessions(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(session_id, user_id)
        )
    ''')
    
    # Chat messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Audit log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            username TEXT NOT NULL,
            action_type TEXT NOT NULL,
            category TEXT NOT NULL,
            target_type TEXT,
            target_id TEXT,
            details TEXT,
            ip_address TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Online users tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS online_users (
            user_id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            last_seen TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Friend-group multi-tenancy tables (idempotent CREATE)
    # friend_groups: Named groups for organizing servers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friend_groups (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    
    # group_members: Membership in friend groups
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_members (
            id TEXT PRIMARY KEY,
            group_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'member',
            joined_at TEXT NOT NULL,
            UNIQUE(group_id, user_id),
            FOREIGN KEY (group_id) REFERENCES friend_groups(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # group_servers: Servers associated with groups
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_servers (
            id TEXT PRIMARY KEY,
            group_id TEXT NOT NULL,
            orchestrator_id TEXT NOT NULL,
            server_uid TEXT NOT NULL,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(orchestrator_id, server_uid),
            FOREIGN KEY (group_id) REFERENCES friend_groups(id),
            FOREIGN KEY (orchestrator_id) REFERENCES orchestrators(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    
    # group_announcements: Messages for group members
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_announcements (
            id TEXT PRIMARY KEY,
            group_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (group_id) REFERENCES friend_groups(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # admin_alerts: System alerts for admins
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_alerts (
            id TEXT PRIMARY KEY,
            kind TEXT NOT NULL,
            message TEXT NOT NULL,
            detail TEXT,
            created_at TEXT NOT NULL,
            acknowledged_at TEXT
        )
    ''')
    
    # Add group_id column to chat_messages if it doesn't exist
    try:
        cursor.execute("ALTER TABLE chat_messages ADD COLUMN group_id TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # One-time migration: v3 (run only once, guarded by system_config key)
    db_path_str = os.environ.get('DATABASE_PATH', str(ROOT_DIR / 'peon.db'))
    db_path = Path(db_path_str)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn_mig = sqlite3.connect(db_path)
    cursor_mig = conn_mig.cursor()
    cursor_mig.execute("SELECT value FROM system_config WHERE key = 'migration_v3_done'")
    row = cursor_mig.fetchone()
    
    if row is None:
        # Migration not yet run - execute one-time steps
        # 1. Check if chat_messages exists and its schema
        cursor_mig.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_messages'")
        chat_messages_exists = cursor_mig.fetchone() is not None
        
        if chat_messages_exists:
            cursor_mig.execute("PRAGMA table_info(chat_messages)")
            old_cols = [row[1] for row in cursor_mig.fetchall()]
            
            # Check if group_id already exists
            has_group_id = 'group_id' in old_cols
            
            if has_group_id:
                # Table exists with correct schema - just delete all messages
                cursor_mig.execute('DELETE FROM chat_messages')
            else:
                # Table exists without group_id - recreate with new schema and copy data
                cursor_mig.execute('''
                    CREATE TABLE IF NOT EXISTS chat_messages_new (
                        id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        message TEXT NOT NULL,
                        group_id TEXT,
                        created_at TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                ''')
                
                # Copy data from old table (group_id will be NULL)
                cursor_mig.execute('INSERT INTO chat_messages_new (id, user_id, message, created_at) SELECT id, user_id, message, created_at FROM chat_messages')
                
                # Drop old table and rename new
                cursor_mig.execute('DROP TABLE IF EXISTS chat_messages')
                cursor_mig.execute('ALTER TABLE chat_messages_new RENAME TO chat_messages')
        else:
            # chat_messages doesn't exist - create with new schema
            cursor_mig.execute('''
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    group_id TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
        
        # 2. Delete all chat messages (as per spec: "chat_messages" is wiped)
        cursor_mig.execute('DELETE FROM chat_messages')
        
        # 3. Migrate moderators to users
        cursor_mig.execute("UPDATE users SET role = 'user' WHERE role = 'moderator'")
        
        # Mark migration as done
        cursor_mig.execute("INSERT INTO system_config (key, value) VALUES ('migration_v3_done', '1')")
        conn_mig.commit()
    conn_mig.close()
    
    # Add new columns to existing tables if they don't exist
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN is_chat_banned INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    conn.commit()
    conn.close()
