import unittest
from unittest.mock import patch
import sys
import os

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from scripts.lib.discovery import DiscoveryEngine


class TestDiscoveryEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DiscoveryEngine(country="jp")

    def test_country_initialization(self):
        self.assertEqual(self.engine.country, "jp")
        self.assertEqual(self.engine.api.country, "jp")

    @patch("scripts.lib.itunes_api.iTunesAPI.get_competitors")
    @patch("scripts.lib.itunes_api.iTunesAPI.search_apps")
    def test_discover_competitors_combined(self, mock_search, mock_get_comp):
        # Mock genre results
        mock_get_comp.return_value = [
            {"trackId": 1, "trackName": "Genre App", "userRatingCount": 100}
        ]

        # Mock search results
        mock_search.return_value = {
            "resultCount": 1,
            "results": [
                {"trackId": 2, "trackName": "Keyword App", "userRatingCount": 50}
            ],
        }

        results = self.engine.discover_competitors("productivity", limit=5)

        self.assertEqual(len(results), 2)
        # Verify deduplication or addition logic
        ids = [r["app_id"] for r in results]
        self.assertIn(1, ids)
        self.assertIn(2, ids)


if __name__ == "__main__":
    unittest.main()
