"""
Pull public data from user
"""
from __future__ import annotations

import logging
from typing import Any

from http_overeasy.http_client import HTTPClient

from steggtistics.model.header_details import HeaderDetails


class PullUser:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.http = HTTPClient(headers={"Accept": "application/vnd.github.v3+json"})

    def pull(self, username: str) -> Any:
        fullpull: list[dict[str, Any]] = []
        url = f"https://api.github.com/users/{username}/events?per_page=100&page=1"

        while "The world burns":
            self.log.info("Pulling %s, url: '%s'", username, url)
            resp = self.http.get(url)
            details = HeaderDetails.build_from(resp.get_headers())

            if not resp.has_success():
                self.log.error("Failed pull: %s", resp.get_body())
                break

            fullpull.extend(resp.get_json())
            url = details.next or ""
            if not url:
                break

        return fullpull


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    from pathlib import Path
    import json

    pulluser = PullUser()

    json.dump(pulluser.pull("Preocts"), Path("output.json").open("w"), indent=4)
