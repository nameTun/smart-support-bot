import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
import sys

# Ensure src is in sys.path if not running through pytest module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from scraper import fetch_articles

@patch("scraper.requests.get")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
@patch("scraper.ZENDESK_API_URL", "https://mock.zendesk.com/api/v2/articles.json")
def test_fetch_articles_success(mock_makedirs, mock_file, mock_get):
    # Prepare mock API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "articles": [
            {
                "id": 12345,
                "title": "How to create an account",
                "body": "<p>Click <strong>Sign Up</strong> button.</p>",
                "updated_at": "2023-10-01T12:00:00Z"
            }
        ],
        "next_page": None
    }
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    # Execute
    result = fetch_articles()

    # Assert API was called
    mock_get.assert_called_once_with("https://mock.zendesk.com/api/v2/articles.json")

    # Assert os.makedirs was called to ensure articles dir exists
    mock_makedirs.assert_called()

    # Assert file was written correctly
    mock_file.assert_called()
    
    # Assert the file content
    handle = mock_file()
    written_content = "".join(call.args[0] for call in handle.write.mock_calls)
    
    assert "# How to create an account" in written_content
    assert "Click **Sign Up** button" in written_content
    
    # Check the return value
    assert result is not None
    assert len(result) == 1
    assert result[0] == {
        "id": "12345",
        "updated_at": "2023-10-01T12:00:00Z"
    }

@patch("scraper.ZENDESK_API_URL", None)
def test_fetch_articles_missing_url():
    # If ZENDESK_API_URL is missing, it should return None
    result = fetch_articles()
    assert result is None
