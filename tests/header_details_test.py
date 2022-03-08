from __future__ import annotations

from datetime import datetime

from steggtistics.model.header_details import LastResponse

MOCK_HEADER: dict[str, str] = {
    "Server": "GitHub.com",
    "Date": "Tue, 08 Mar 2022 02:25:47 GMT",
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "public, max-age=60, s-maxage=60",
    "Vary": "Accept, Accept-Encoding, Accept, X-Requested-With",
    "ETag": 'W/"mock"',
    "Last-Modified": "Tue, 08 Mar 2022 01:44:40 GMT",
    "X-Poll-Interval": "60",
    "X-GitHub-Media-Type": "github.v3; format=json",
    "Link": '<https://api.github.com/user/13407322/events?per_page=10&page=3>; rel="next", <https://api.github.com/user/13407322/events?per_page=10&page=30>; rel="last", <https://api.github.com/user/13407322/events?per_page=10&page=1>; rel="prev"',  # noqa
    "Access-Control-Expose-Headers": "ETag, Link, Location, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Used, X-RateLimit-Resource, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval, X-GitHub-Media-Type, X-GitHub-SSO, X-GitHub-Request-Id, Deprecation, Sunset",  # noqa
    "Access-Control-Allow-Origin": "*",
    "Strict-Transport-Security": "max-age=31536000; includeSubdomains; preload",
    "X-Frame-Options": "deny",
    "X-Content-Type-Options": "nosniff",
    "X-XSS-Protection": "0",
    "Referrer-Policy": "origin-when-cross-origin, strict-origin-when-cross-origin",
    "Content-Security-Policy": "default-src 'none'",
    "X-RateLimit-Limit": "60",
    "X-RateLimit-Remaining": "52",
    "X-RateLimit-Reset": "1646708508",
    "X-RateLimit-Resource": "core",
    "X-RateLimit-Used": "8",
    "Accept-Ranges": "bytes",
    "Content-Length": "13539",
    "X-GitHub-Request-Id": "EC3A:1D27:67065F:1234BC8:6226BEAB",
}

EXPECTED = {
    "next": "https://api.github.com/user/13407322/events?per_page=10&page=3",
    "prev": "https://api.github.com/user/13407322/events?per_page=10&page=1",
    "last": "https://api.github.com/user/13407322/events?per_page=10&page=30",
    "first": None,
    "remaining": 52,
    "rate_reset": datetime.fromtimestamp(1646708508),
}


class NotFound:
    ...


def test_build_from_response() -> None:
    lresp = LastResponse.build_from(MOCK_HEADER)

    for key, value in EXPECTED.items():
        assert getattr(lresp, key, NotFound) == value, f"{key}, {value}"
