import uuid
from datetime import datetime, timezone
from typing import List, Optional

from core.database import get_db, dict_from_row


class ChatService:
    """Service for chat messages and online-user lookups"""

    @staticmethod
    def get_recent_messages(limit: int) -> List[dict]:
        """Get the most recent chat messages, oldest first"""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT m.id, m.message, m.created_at, u.id as user_id, u.username
            FROM chat_messages m
            JOIN users u ON m.user_id = u.id
            ORDER BY m.created_at DESC
            LIMIT ?
        ''', (limit,))

        messages = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()

        return list(reversed(messages))

    @staticmethod
    def create_message(user_id: str, message: str) -> dict:
        """Create a new chat message"""
        conn = get_db()
        cursor = conn.cursor()

        msg_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        cursor.execute(
            "INSERT INTO chat_messages (id, user_id, message, created_at) VALUES (?, ?, ?, ?)",
            (msg_id, user_id, message, now)
        )
        conn.commit()
        conn.close()

        return {
            "id": msg_id,
            "message": message,
            "created_at": now,
            "user_id": user_id,
        }

    @staticmethod
    def get_message_by_id(message_id: str) -> Optional[dict]:
        """Get a chat message by id"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chat_messages WHERE id = ?", (message_id,))
        msg = cursor.fetchone()
        conn.close()
        return dict_from_row(msg) if msg else None

    @staticmethod
    def delete_message(message_id: str) -> bool:
        """Delete a chat message by id. Returns False if it did not exist."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_messages WHERE id = ?", (message_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    @staticmethod
    def clear_all() -> int:
        """Delete all chat messages. Returns the number of messages deleted."""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM chat_messages")
        count = cursor.fetchone()[0]

        cursor.execute("DELETE FROM chat_messages")
        conn.commit()
        conn.close()

        return count

    @staticmethod
    def get_users_by_ids(user_ids: List[str]) -> List[dict]:
        """Get username/role details for a list of user ids"""
        if not user_ids:
            return []

        conn = get_db()
        cursor = conn.cursor()

        placeholders = ','.join(['?' for _ in user_ids])
        cursor.execute(f'''
            SELECT id, username, role FROM users WHERE id IN ({placeholders})
        ''', user_ids)

        users = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()

        return users
