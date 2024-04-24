import pytest
from click.testing import CliRunner
from unittest.mock import patch
import requests_mock
from topics_explorer.main import fetch_top_cited_works


@pytest.fixture
def mock_response():
    with requests_mock.Mocker() as m:
        yield m


def test_fetch_top_cited_works(mock_response):
    # Mock the API response
    mock_response.get(
        "https://api.openalex.org/works?search=example&per_page=200",
        json={
            "results": [
                {
                    "display_name": "Paper 1",
                    "publication_year": 2021,
                    "cited_by_count": 100,
                },
                {
                    "display_name": "Paper 2",
                    "publication_year": 2022,
                    "cited_by_count": 150,
                },
            ]
        },
    )

    runner = CliRunner()
    result = runner.invoke(
        fetch_top_cited_works, ["--keyword", "example", "--year", 2020]
    )

    # Check outputs
    assert "Paper 1" in result.output
    assert "Paper 2" in result.output
    assert "Citations/Year" in result.output
    assert result.exit_code == 0


def test_http_error_handling(mock_response):
    # Mock an HTTP error
    mock_response.get(
        "https://api.openalex.org/works?search=example&per_page=200", status_code=500
    )

    runner = CliRunner()
    result = runner.invoke(
        fetch_top_cited_works, ["--keyword", "example", "--year", 2020]
    )

    # Check error handling
    assert "HTTP Error" in result.output
    assert result.exit_code != 0
