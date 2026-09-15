import uuid
from datetime import datetime, timezone
from typing import List, Optional

from core.database import get_db, dict_from_row


class SessionService:
    """Service for gaming sessions and their RSVPs"""

    @staticmethod
    def get_sessions(status: Optional[str] = None) -> List[dict]:
        """Get all gaming sessions (optionally filtered by status), each with its RSVPs"""
        conn = get_db()
        cursor = conn.cursor()

        query = '''
            SELECT s.*, u.username as creator_username
            FROM gaming_sessions s
            LEFT JOIN users u ON s.created_by = u.id
        '''
        params = []

        if status:
            query += " WHERE s.status = ?"
            params.append(status)

        query += " ORDER BY s.scheduled_time ASC"

        cursor.execute(query, params)
        sessions = []

        for row in cursor.fetchall():
            session = dict_from_row(row)

            # Get RSVPs for this session
            cursor.execute('''
                SELECT r.*, u.username
                FROM session_rsvps r
                JOIN users u ON r.user_id = u.id
                WHERE r.session_id = ?
            ''', (session['id'],))
            session['rsvps'] = [dict_from_row(r) for r in cursor.fetchall()]

            sessions.append(session)

        conn.close()
        return sessions

    @staticmethod
    def get_session_by_id(session_id: str) -> Optional[dict]:
        """Get a gaming session by id (without RSVPs)"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gaming_sessions WHERE id = ?", (session_id,))
        session = cursor.fetchone()
        conn.close()
        return dict_from_row(session) if session else None

    @staticmethod
    def create_session(
        title: str,
        description: Optional[str],
        orchestrator_id: str,
        server_uid: Optional[str],
        scheduled_time: str,
        duration_minutes: int,
        created_by: str
    ) -> dict:
        """Create a new gaming session"""
        conn = get_db()
        cursor = conn.cursor()

        session_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        cursor.execute('''
            INSERT INTO gaming_sessions (id, title, description, orchestrator_id, server_uid, scheduled_time, duration_minutes, created_by, created_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'scheduled')
        ''', (session_id, title, description, orchestrator_id, server_uid, scheduled_time, duration_minutes, created_by, now))

        conn.commit()
        conn.close()

        return {
            "id": session_id,
            "title": title,
            "description": description,
            "orchestrator_id": orchestrator_id,
            "server_uid": server_uid,
            "scheduled_time": scheduled_time,
            "duration_minutes": duration_minutes,
            "created_by": created_by,
            "created_at": now,
            "status": "scheduled"
        }

    ALLOWED_UPDATE_FIELDS = {
        'title', 'description', 'server_uid', 'scheduled_time', 'duration_minutes', 'status'
    }

    @staticmethod
    def update_session(session_id: str, updates: dict) -> Optional[dict]:
        """Update a gaming session's fields. Returns None if the session doesn't exist."""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM gaming_sessions WHERE id = ?", (session_id,))
        if not cursor.fetchone():
            conn.close()
            return None

        updates = {k: v for k, v in updates.items() if k in SessionService.ALLOWED_UPDATE_FIELDS}

        if not updates:
            conn.close()
            return SessionService.get_session_by_id(session_id)

        fields = [f"{k} = ?" for k in updates.keys()]
        values = list(updates.values()) + [session_id]

        cursor.execute(f"UPDATE gaming_sessions SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()

        cursor.execute("SELECT * FROM gaming_sessions WHERE id = ?", (session_id,))
        updated = dict_from_row(cursor.fetchone())
        conn.close()

        return updated

    @staticmethod
    def delete_session(session_id: str) -> Optional[dict]:
        """Delete a gaming session and its RSVPs. Returns the deleted session, or None if not found."""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM gaming_sessions WHERE id = ?", (session_id,))
        session = cursor.fetchone()
        if not session:
            conn.close()
            return None

        session_dict = dict_from_row(session)

        cursor.execute("DELETE FROM session_rsvps WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM gaming_sessions WHERE id = ?", (session_id,))

        conn.commit()
        conn.close()

        return session_dict

    @staticmethod
    def session_exists(session_id: str) -> bool:
        """Check whether a gaming session exists"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM gaming_sessions WHERE id = ?", (session_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    @staticmethod
    def upsert_rsvp(session_id: str, user_id: str, status: str) -> str:
        """Create or update a user's RSVP for a session. Returns the RSVP id."""
        conn = get_db()
        cursor = conn.cursor()

        rsvp_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        cursor.execute('''
            INSERT INTO session_rsvps (id, session_id, user_id, status, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(session_id, user_id) DO UPDATE SET status = ?, created_at = ?
        ''', (rsvp_id, session_id, user_id, status, now, status, now))

        conn.commit()
        conn.close()

        return rsvp_id

    @staticmethod
    def cancel_rsvp(session_id: str, user_id: str) -> bool:
        """Cancel a user's RSVP for a session. Returns False if none existed."""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM session_rsvps
            WHERE session_id = ? AND user_id = ?
        ''', (session_id, user_id))

        found = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return found
