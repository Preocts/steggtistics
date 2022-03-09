from __future__ import annotations

import re
from datetime import datetime


class HeaderDetails:
    next: str | None
    prev: str | None
    last: str | None
    first: str | None
    total: int
    remaining: int
    rate_reset: datetime

    @classmethod
    def build_from(cls, httpdict: dict[str, str]) -> HeaderDetails:
        """Build model from HTTP response"""
        newobj = cls()
        newobj.next = cls._extract_next(httpdict["Link"], "next")
        newobj.prev = cls._extract_next(httpdict["Link"], "prev")
        newobj.last = cls._extract_next(httpdict["Link"], "last")
        newobj.first = cls._extract_next(httpdict["Link"], "first")
        newobj.total = cls._extract_total(newobj.last)
        newobj.remaining = int(httpdict["X-RateLimit-Remaining"])
        newobj.rate_reset = datetime.fromtimestamp(float(httpdict["X-RateLimit-Reset"]))

        return newobj

    @staticmethod
    def _extract_next(link: str, rel: str) -> str | None:
        """internal: extract next url from headers.link"""
        pattern = rf'<(.*?)>; rel="{rel}"'
        for link_seg in link.split(","):
            match = re.match(pattern, link_seg.strip())
            if match:
                return match.group(1)
        return None

    @staticmethod
    def _extract_total(last: str | None) -> int:
        """internal: extract total pages from last link or return 0"""
        pattern = r"(?<!per_)page=(\d+)"
        match = re.search(pattern, last or "")
        return int(match.group(1)) if match else 0
