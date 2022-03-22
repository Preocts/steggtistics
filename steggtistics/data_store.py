"""Database storage for steggtistics."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from steggtistics.model.event import Event


class DataStore:
    """Database storage for steggtistics."""

    def __init__(self, store_path: str | Path) -> None:
        """Open datastore at path."""
        self._path = store_path
        self._db = sqlite3.connect(store_path)

        self._build_table()

    def _build_table(self) -> None:
        """Build table if doesn't exist."""
        with self._cursor() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS events(id TEXT, type TEXT, "
                "public TEXT, created_at TEXT, repo_name TEXT, repo_url TEXT)"
            )
            self._db.commit()

    def row_count(self) -> int:
        """Return total number of rows in loaded database file."""
        with self._cursor() as cursor:
            cursor.execute("SELECT COUNT(id) FROM events")
            return cursor.fetchone()[0]

    def save_row(self, row: Event) -> None:
        """Single save row to database."""
        self.save_rows([row])

    def save_rows(self, rows: list[Event]) -> None:
        """Bulk save rows to database."""
        # NOTE: Insert order must match Event model
        sql = (
            "INSERT INTO events (id, type, public, created_at, repo_name, repo_url) "
            "VALUES (?,?,?,?,?,?)"
        )

        with self._cursor() as cursor:
            for row in rows:
                cursor.execute(sql, tuple(row.asdict().values()))
            self._db.commit()

    def get_rows(self) -> list[Event]:
        """Fetch all rows from database."""
        with self._cursor() as cursor:
            cursor.execute("SELECT * FROM events")
            results = cursor.fetchall()

        return [Event.build_from_row(*result) for result in results]

    @contextmanager
    def _cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        """Context manager to ensure cursors are closed."""
        try:
            cursor = self._db.cursor()
            yield cursor
        finally:
            cursor.close()
