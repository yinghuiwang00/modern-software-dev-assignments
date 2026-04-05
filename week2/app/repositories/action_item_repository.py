"""Repository for action item data access operations."""

from __future__ import annotations

import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import List, Optional

from ..config import get_settings
from ..schemas import ActionItem

logger = logging.getLogger(__name__)


class ActionItemRepository:
    """Repository for managing action item database operations."""

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

    def create_many(self, items: List[str], note_id: Optional[int] = None) -> List[int]:
        """Create multiple action items.

        Args:
            items: List of action item texts.
            note_id: Optional note ID to associate with the items.

        Returns:
            List[int]: List of created action item IDs.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            ids: List[int] = []
            for item in items:
                cursor.execute(
                    "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
                    (note_id, item),
                )
                ids.append(int(cursor.lastrowid))
            conn.commit()
            logger.info(f"Created {len(ids)} action items for note {note_id}")
            return ids

    def get_by_id(self, action_item_id: int) -> Optional[ActionItem]:
        """Get an action item by ID.

        Args:
            action_item_id: ID of the action item to retrieve.

        Returns:
            Optional[ActionItem]: The action item if found, None otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, note_id, text, done, created_at FROM action_items WHERE id = ?",
                (action_item_id,),
            )
            row = cursor.fetchone()
            if row:
                logger.info(f"Retrieved action item with ID {action_item_id}")
                return ActionItem(
                    id=row["id"],
                    note_id=row["note_id"],
                    text=row["text"],
                    done=bool(row["done"]),
                    created_at=row["created_at"],
                )
            logger.warning(f"Action item with ID {action_item_id} not found")
            return None

    def list_all(self, note_id: Optional[int] = None, limit: Optional[int] = None) -> List[ActionItem]:
        """List action items, optionally filtered by note ID.

        Args:
            note_id: Optional note ID to filter by.
            limit: Maximum number of items to return.

        Returns:
            List[ActionItem]: List of action items.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if note_id is not None:
                if limit:
                    cursor.execute(
                        "SELECT id, note_id, text, done, created_at FROM action_items WHERE note_id = ? ORDER BY id DESC LIMIT ?",
                        (note_id, limit),
                    )
                else:
                    cursor.execute(
                        "SELECT id, note_id, text, done, created_at FROM action_items WHERE note_id = ? ORDER BY id DESC",
                        (note_id,),
                    )
            else:
                if limit:
                    cursor.execute(
                        "SELECT id, note_id, text, done, created_at FROM action_items ORDER BY id DESC LIMIT ?",
                        (limit,),
                    )
                else:
                    cursor.execute(
                        "SELECT id, note_id, text, done, created_at FROM action_items ORDER BY id DESC",
                    )
            rows = cursor.fetchall()
            action_items = [
                ActionItem(
                    id=row["id"],
                    note_id=row["note_id"],
                    text=row["text"],
                    done=bool(row["done"]),
                    created_at=row["created_at"],
                )
                for row in rows
            ]
            logger.info(f"Retrieved {len(action_items)} action items")
            return action_items

    def update_done_status(self, action_item_id: int, done: bool) -> bool:
        """Update the done status of an action item.

        Args:
            action_item_id: ID of the action item to update.
            done: New done status.

        Returns:
            bool: True if action item was updated, False if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE action_items SET done = ? WHERE id = ?",
                (1 if done else 0, action_item_id),
            )
            conn.commit()
            if cursor.rowcount > 0:
                logger.info(f"Updated action item {action_item_id} done status to {done}")
                return True
            logger.warning(f"Action item with ID {action_item_id} not found for update")
            return False

    def delete(self, action_item_id: int) -> bool:
        """Delete an action item by ID.

        Args:
            action_item_id: ID of the action item to delete.

        Returns:
            bool: True if action item was deleted, False if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM action_items WHERE id = ?", (action_item_id,))
            conn.commit()
            if cursor.rowcount > 0:
                logger.info(f"Deleted action item with ID {action_item_id}")
                return True
            logger.warning(f"Action item with ID {action_item_id} not found for deletion")
            return False
