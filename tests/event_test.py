from __future__ import annotations

from typing import Any

import pytest

from steggtistics.model.event import Event

SAMPLE: dict[str, Any] = {
    "type": "WatchEvent",
    "public": False,
    "payload": {},
    "repo": {
        "id": 3,
        "name": "octocat/Hello-World",
        "url": "https://api.github.com/repos/octocat/Hello-World",
    },
    "actor": {
        "id": 1,
        "login": "octocat",
        "gravatar_id": "",
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "url": "https://api.github.com/users/octocat",
    },
    "org": {
        "id": 1,
        "login": "github",
        "gravatar_id": "",
        "url": "https://api.github.com/orgs/github",
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
    },
    "created_at": "2011-09-06T17:26:27Z",
    "id": "12345",
}


@pytest.mark.parametrize(
    ("attr", "expected"),
    (
        ("id", SAMPLE["id"]),
        ("type", SAMPLE["type"]),
        ("public", SAMPLE["public"]),
        ("created_at", SAMPLE["created_at"]),
        ("repo_name", SAMPLE["repo"]["name"]),
        ("repo_url", SAMPLE["repo"]["url"]),
    ),
)
def test_build_from(attr: str, expected: str) -> None:
    model = Event.build_from(SAMPLE)

    assert getattr(model, attr) == expected
