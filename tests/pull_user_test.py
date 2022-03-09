import pytest

from steggtistics.model.header_details import HeaderDetails
from steggtistics.pull_user import PullUser
from tests.header_details_test import MOCK_HEADER


@pytest.fixture
def mock_client() -> PullUser:
    client = PullUser()
    client._last_headers = HeaderDetails.build_from(MOCK_HEADER)
    return client


def test_is_rate_limited_true(mock_client: PullUser) -> None:
    mock_client._last_headers.remaining = 0

    assert mock_client.is_rate_limited() is True


def test_is_rate_limited_false(mock_client: PullUser) -> None:
    mock_client._last_headers.remaining = 10

    assert mock_client.is_rate_limited() is False
