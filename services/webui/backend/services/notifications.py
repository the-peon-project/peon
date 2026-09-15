import json
from typing import Optional

from core.database import get_db


class NotificationService:
    """Service for storing/retrieving notification channel configuration
    (Discord webhook, email/SMTP) in system_config"""

    CONFIG_KEY_DISCORD = 'notification_discord'
    CONFIG_KEY_EMAIL = 'notification_email'

    @staticmethod
    def get_config(config_key: str) -> Optional[dict]:
        """Get notification configuration from database"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM system_config WHERE key = ?", (config_key,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return json.loads(row['value'])
        return None

    @staticmethod
    def save_config(config_key: str, config: dict) -> None:
        """Save notification configuration to database"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO system_config (key, value)
            VALUES (?, ?)
        ''', (config_key, json.dumps(config)))
        conn.commit()
        conn.close()
