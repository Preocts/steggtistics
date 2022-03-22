from __future__ import annotations

import os
from sqlite3 import Connection
from tempfile import mkstemp
from typing import Generator

import pytest

from steggtistics.data_store import DataStore
from steggtistics.model.event import Event

NUMBER_OF_ROWS = 100  # For mock fill
EXPECTED_COLUMNS = [
    "id",
    "type",
    "public",
    "created_at",
    "repo_name",
    "repo_url",
]


@pytest.fixture
def store() -> Generator[DataStore, None, None]:
    try:
        fp, path = mkstemp()
        os.close(fp)

        datastore = DataStore(path)
        yield datastore

    finally:
        datastore._db.close()
        os.remove(path)


@pytest.fixture
def mock_rows() -> list[Event]:
    rows: list[Event] = []
    for idx in range(NUMBER_OF_ROWS):
        row = Event()
        row.id_ = str(idx)
        row.type_ = "mock"
        row.public = True
        row.created_at = "mock"
        row.repo_name = "mock"
        row.repo_url = "mock"
        rows.append(row)
    return rows


def test_init(store: DataStore) -> None:
    assert os.path.isfile(store._path)
    assert isinstance(store._db, Connection)


def test_get_size_empty(store: DataStore) -> None:
    size = store.row_count()

    assert size == 0


def test_create_table(store: DataStore) -> None:
    cursor = store._db.cursor()
    cursor.execute("SELECT * FROM events LIMIT 1")
    names = [desc[0] for desc in cursor.description]

    result = set(names) - set(EXPECTED_COLUMNS)

    assert len(result) == 0


def test_add_rows(store: DataStore, mock_rows: list[Event]) -> None:
    store.save_rows(mock_rows)

    assert store.row_count() == NUMBER_OF_ROWS


def test_add_row(store: DataStore, mock_rows: list[Event]) -> None:
    store.save_row(mock_rows[0])

    assert store.row_count() == 1


def test_get_rows(store: DataStore, mock_rows: list[Event]) -> None:
    store.save_rows(mock_rows)

    results = store.get_rows()

    assert len(results) == NUMBER_OF_ROWS
