import os
from sqlite3 import Connection
from tempfile import mkstemp
from typing import Generator

import pytest

from steggtistics.data_store import DataStore

EXPECTED_COLUMNS = [
    "id_",
    "type_",
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
        os.remove(path)


def test_init(store: DataStore) -> None:
    assert os.path.isfile(store._path)
    assert isinstance(store._db, Connection)


def test_create_table(store: DataStore) -> None:
    cursor = store._db.cursor()
    cursor.execute("SELECT * FROM events LIMIT 1")
    names = [desc[0] for desc in cursor.description]

    result = set(names) - set(EXPECTED_COLUMNS)

    assert len(result) == 0
