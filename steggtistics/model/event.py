"""Model common data from GitHub Events"""
from __future__ import annotations

from typing import Any


class Event:
    """Creates an empty Event model"""

    id: str
    type: str
    public: bool
    created_at: str
    repo_name: str
    repo_url: str

    @classmethod
    def build_from(cls, event_data: dict[str, Any]) -> Event:
        """Build model using event object from Events API"""

        newobj = cls()
        newobj.id = event_data["id"]
        newobj.type = event_data["type"]
        newobj.public = event_data["public"]
        newobj.created_at = event_data["created_at"]
        newobj.repo_name = event_data["repo"]["name"]
        newobj.repo_url = event_data["repo"]["url"]

        return newobj
