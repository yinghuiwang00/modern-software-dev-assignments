"""Database initialization and schema management."""

from __future__ import annotations

import logging
import sqlite3
from contextlib import contextmanager

from .config import get_settings

logger = logging.getLogger(__name__)


def get_db_connection() -> sqlite3.Connection:
    """Get a database connection.

    Returns:
        sqlite3.Connection: Database connection with row factory enabled.
    """
    settings = get_settings()
    settings.database_dir.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(settings.database_file))
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def get_db_connection_context():
    """Context manager for database connections.

    Yields:
        sqlite3.Connection: Database connection with row factory enabled.
    """
    settings = get_settings()
    settings.database_dir.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(settings.database_file))
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    except Exception as e:
        connection.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        connection.close()


def init_db() -> None:
    """Initialize the database schema.

    Creates tables if they don't exist:
    - notes: Stores meeting notes
    - action_items: Stores extracted action items
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Create notes table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );
            """
        )

        # Create action_items table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_id INTEGER,
                text TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (note_id) REFERENCES notes(id)
            );
            """
        )

        connection.commit()
        connection.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
