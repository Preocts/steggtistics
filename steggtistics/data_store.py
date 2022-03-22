"""Database storage for steggtistics."""
from __future__ import annotations

import sqlite3
from pathlib import Path


class DataStore:
    """Database storage for steggtistics."""

    def __init__(self, store_path: str | Path) -> None:
        """Open datastore at path."""
        self._path = store_path
        self._db = sqlite3.connect(store_path)

        self._build_table()

    def _build_table(self) -> None:
        """Build table if doesn't exist."""
        cursor = self._db.cursor()
        try:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS events(id_ TEXT, type_ TEXT, "
                "public TEXT, created_at TEXT, repo_name TEXT, repo_url TEXT)"
            )
            self._db.commit()
        finally:
            cursor.close()
