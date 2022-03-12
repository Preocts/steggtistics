"""Pull public data from user."""
from __future__ import annotations

import logging
from typing import Any

from http_overeasy.http_client import HTTPClient

from steggtistics.model.event import Event
from steggtistics.model.header_details import HeaderDetails


class PullUser:
    """Pull public data from user."""

    def __init__(self, api_url: str = "https://api.github.com") -> None:
        """Provide optional alternative GitHub URL for GHE or GHC."""
        self.log = logging.getLogger(__name__)
        self.http = HTTPClient(headers={"Accept": "application/vnd.github.v3+json"})
        self.api_url = api_url
        self._last_headers = HeaderDetails()

    def pull_events(self, username: str) -> list[Event]:
        """Pull like of Events for given user."""
        results = self.pull(username)

        return [Event.build_from(result) for result in results]

    def pull(self, username: str) -> list[dict[str, Any]]:
        """Pull raw Event results for given user."""
        fullpull: list[dict[str, Any]] = []
        url = f"{self.api_url}/users/{username}/events?per_page=100&page=1"

        while "The world burns":
            self.log.info("Pulling %s, url: '%s'", username, url)
            resp = self.http.get(url)
            self._last_headers = HeaderDetails.build_from(resp.get_headers())

            if not resp.has_success():
                self.log.error("Failed pull: %s", resp.get_body())
                break

            fullpull.extend(resp.get_json())
            url = self._last_headers.next or ""
            if not url or self.is_rate_limited():
                break
        return fullpull

    def is_rate_limited(self) -> bool:
        """Is True when no additional requests can be made until rate_reset."""
        if not self._last_headers.remaining:
            self.log.warning("Rate limit reached.")
        return not self._last_headers.remaining
