from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from steggtistics.model.header_details import HeaderDetails
from steggtistics.pull_user import PullUser
from tests.event_test import SAMPLE as EVENT_SAMPLE
from tests.header_details_test import MOCK_HEADER


@pytest.fixture
def mock_client() -> PullUser:
    client = PullUser()
    client._last_headers = HeaderDetails.build_from(MOCK_HEADER)
    return client


class MockResponse:
    def __init__(
        self,
        headers: dict[str, str] = MOCK_HEADER,
        success: bool = True,
    ) -> None:
        self.headers = headers
        self.success = success

    def get_headers(self) -> dict[str, str]:
        return self.headers

    def has_success(self) -> bool:
        return self.success

    def get_json(self) -> dict[str, str]:
        return {"mock": "mock"}

    def get_body(self) -> str:
        return "mock"


def test_is_rate_limited_true(mock_client: PullUser) -> None:
    mock_client._last_headers.remaining = 0

    assert mock_client.is_rate_limited() is True


def test_is_rate_limited_false(mock_client: PullUser) -> None:
    mock_client._last_headers.remaining = 10

    assert mock_client.is_rate_limited() is False


def test_pull_user_pagination(mock_client: PullUser) -> None:
    responses = [MockResponse() for _ in range(10)]

    stop_resp = MOCK_HEADER.copy()
    stop_resp["Link"] = ""
    responses.append(MockResponse(stop_resp))
    with patch.object(mock_client.http, "get", side_effect=responses) as mocker:
        mock_client.pull("mock")

        assert mocker.call_count == 11


def test_pull_user_rate_limited(mock_client: PullUser, caplog: Any) -> None:
    stop_resp = MOCK_HEADER.copy()
    stop_resp["X-RateLimit-Remaining"] = "0"
    with patch.object(
        mock_client.http, "get", return_value=MockResponse(stop_resp)
    ) as mocker:
        mock_client.pull("mock")
        assert mocker.call_count == 1

    assert "Rate limit" in caplog.text


def test_pull_user_rate_failed(mock_client: PullUser, caplog: Any) -> None:
    return_error = MockResponse(success=False)
    with patch.object(mock_client.http, "get", return_value=return_error) as mocker:
        mock_client.pull("mock")
        assert mocker.call_count == 1

    assert "Failed" in caplog.text


def test_pull_events(mock_client: PullUser) -> None:
    return_size = 100
    return_body = [EVENT_SAMPLE for _ in range(return_size)]

    with patch.object(mock_client, "pull", return_value=return_body):
        results = mock_client.pull_events("mock_user")

    assert len(results) == return_size
    for result in results:
        assert result.id == EVENT_SAMPLE["id"]
