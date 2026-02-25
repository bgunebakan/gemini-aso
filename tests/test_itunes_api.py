import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from scripts.lib.itunes_api import iTunesAPI


class TestiTunesAPI(unittest.TestCase):
    def setUp(self):
        self.api = iTunesAPI(country="us")

    @patch("urllib.request.urlopen")
    def test_search_apps_success(self, mock_urlopen):
        # Mock response
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(
            {"resultCount": 1, "results": [{"trackName": "Test App", "trackId": 12345}]}
        ).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        results = self.api.search_apps("test")

        self.assertEqual(results["resultCount"], 1)
        self.assertEqual(results["results"][0]["trackName"], "Test App")
        mock_urlopen.assert_called_once()

    @patch("urllib.request.urlopen")
    def test_search_apps_with_genre(self, mock_urlopen):
        # Mock response
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(
            {"resultCount": 0, "results": []}
        ).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        self.api.search_apps("test", genre_id=6007)

        # Check if genreId was in the URL
        args, kwargs = mock_urlopen.call_args
        url = args[0]
        self.assertIn("genreId=6007", url)

    @patch("urllib.request.urlopen")
    def test_get_app_by_id_found(self, mock_urlopen):
        # Mock response
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(
            {
                "resultCount": 1,
                "results": [{"trackName": "Specific App", "trackId": 54321}],
            }
        ).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        app = self.api.get_app_by_id("54321")

        self.assertIsNotNone(app)
        self.assertEqual(app["trackName"], "Specific App")

    def test_extract_metadata(self):
        raw_data = {
            "trackId": 123,
            "trackName": "My App",
            "description": "Awesome app description",
            "averageUserRating": 4.5,
            "userRatingCount": 1000,
        }

        metadata = self.api.extract_metadata(raw_data)

        self.assertEqual(metadata["app_name"], "My App")
        self.assertEqual(metadata["rating"], 4.5)
        self.assertEqual(metadata["ratings_count"], 1000)


if __name__ == "__main__":
    unittest.main()
