"""Repository for note data access operations."""

from __future__ import annotations

import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import List, Optional

from ..config import get_settings
from ..schemas import Note

logger = logging.getLogger(__name__)


class NoteRepository:
    """Repository for managing note database operations."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize the repository with database path.

        Args:
            db_path: Path to the SQLite database file. If None, uses default from settings.
        """
        settings = get_settings()
        self.db_path = db_path or str(settings.database_file)

    @contextmanager
    def _get_connection(self) -> sqlite3.Connection:
        """Context manager for database connections.

        Yields:
            sqlite3.Connection: Database connection with row factory enabled.
        """
        settings = get_settings()
        settings.database_dir.mkdir(parents=True, exist_ok=True)

        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
        except Exception as e:
            connection.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            connection.close()

    def create(self, content: str) -> int:
        """Create a new note.

        Args:
            content: Content of the note.

        Returns:
            int: ID of the created note.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO notes (content) VALUES (?)",
                (content,),
            )
            conn.commit()
            note_id = int(cursor.lastrowid)
            logger.info(f"Created note with ID {note_id}")
            return note_id

    def get_by_id(self, note_id: int) -> Optional[Note]:
        """Get a note by ID.

        Args:
            note_id: ID of the note to retrieve.

        Returns:
            Optional[Note]: The note if found, None otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, content, created_at FROM notes WHERE id = ?",
                (note_id,),
            )
            row = cursor.fetchone()
            if row:
                logger.info(f"Retrieved note with ID {note_id}")
                return Note(id=row["id"], content=row["content"], created_at=row["created_at"])
            logger.warning(f"Note with ID {note_id} not found")
            return None

    def list_all(self, limit: Optional[int] = None) -> List[Note]:
        """List all notes, ordered by ID descending.

        Args:
            limit: Maximum number of notes to return.

        Returns:
            List[Note]: List of notes.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if limit:
                cursor.execute(
                    "SELECT id, content, created_at FROM notes ORDER BY id DESC LIMIT ?",
                    (limit,),
                )
            else:
                cursor.execute(
                    "SELECT id, content, created_at FROM notes ORDER BY id DESC",
                )
            rows = cursor.fetchall()
            notes = [
                Note(id=row["id"], content=row["content"], created_at=row["created_at"])
                for row in rows
            ]
            logger.info(f"Retrieved {len(notes)} notes")
            return notes

    def delete(self, note_id: int) -> bool:
        """Delete a note by ID.

        Args:
            note_id: ID of the note to delete.

        Returns:
            bool: True if note was deleted, False if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            conn.commit()
            if cursor.rowcount > 0:
                logger.info(f"Deleted note with ID {note_id}")
                return True
            logger.warning(f"Note with ID {note_id} not found for deletion")
            return False
