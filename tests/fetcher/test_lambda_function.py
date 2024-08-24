import pytest
import requests

from fetcher.lambda_function import get_public_repositories


class MockResponse:
    """
    A mock response class used to simulate API responses for testing purposes.

    Attributes:
        status_code (int): The HTTP status code of the response.
        json_data (dict or list): The JSON data to be returned when `json()` is called.
        reason (str, optional): The reason phrase associated with the HTTP status code.
    """

    def __init__(self, status_code, json_data, reason=None):
        """
        Initializes a new MockResponse instance.

        Args:
            status_code (int): The HTTP status code of the mock response.
            json_data (dict or list): The JSON data to be returned by the `json()` method.
            reason (str, optional): The reason phrase associated with the status code.
        """
        self.status_code = status_code
        self.json_data = json_data
        self.reason = reason

    def json(self):
        """
        Returns the JSON data of the mock response.

        Returns:
            dict or list: The JSON data set during initialization.
        """
        return self.json_data


def test_get_public_repositories_success(monkeypatch):
    """
    Tests the `get_public_repositories` function for a successful API response.

    This test simulates a successful API response with multiple repositories and verifies
    that `get_public_repositories` correctly returns the list of repository names.

    Args:
        monkeypatch (pytest.MonkeyPatch): The pytest monkeypatch fixture used to replace
        the `requests.get` method with a mock function.

    Expected Outcome:
        The function should return a list of repository names: ['repo1', 'repo2', 'repo3'].
    """

    def mock_get(url):
        return MockResponse(
            200, [{"name": "repo1"}, {"name": "repo2"}, {"name": "repo3"}]
        )

    monkeypatch.setattr(requests, "get", mock_get)
    repos = get_public_repositories("testuser")
    assert repos == ["repo1", "repo2", "repo3"]


def test_get_public_repositories_no_repos(monkeypatch):
    """
    Tests the `get_public_repositories` function when no repositories are found.

    This test simulates an API response with an empty list of repositories and verifies
    that `get_public_repositories` returns an empty list.

    Args:
        monkeypatch (pytest.MonkeyPatch): The pytest monkeypatch fixture used to replace
        the `requests.get` method with a mock function.

    Expected Outcome:
        The function should return an empty list.
    """

    def mock_get(url):
        return MockResponse(200, [])

    monkeypatch.setattr(requests, "get", mock_get)
    repos = get_public_repositories("testuser")
    assert repos == []


def test_get_public_repositories_error(monkeypatch):
    """
    Tests the `get_public_repositories` function when the API returns an error.

    This test simulates an API error response (e.g., 404 Not Found) and verifies that
    `get_public_repositories` handles the error correctly by returning an empty list.

    Args:
        monkeypatch (pytest.MonkeyPatch): The pytest monkeypatch fixture used to replace
        the `requests.get` method with a mock function.

    Expected Outcome:
        The function should return an empty list.
    """

    def mock_get(url):
        return MockResponse(404, {}, reason="Not Found")

    monkeypatch.setattr(requests, "get", mock_get)
    repos = get_public_repositories("nonexistentuser")
    assert repos == []
