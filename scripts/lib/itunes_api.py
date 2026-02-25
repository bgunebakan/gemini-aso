"""
iTunes Search API wrapper for fetching App Store data.
Free API - no authentication required.

Documentation: https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/
"""

import json
import urllib.parse
import urllib.request
from typing import Dict, List, Any, Optional


class iTunesAPI:
    """Wrapper for iTunes Search API to fetch app store data."""

    BASE_URL = "https://itunes.apple.com/search"

    def __init__(self, country: str = "us"):
        """
        Initialize iTunes API wrapper.

        Args:
            country: Two-letter country code (default: "us")
        """
        self.country = country.lower()
        self.genre_map = self._load_genre_map()

    def _load_genre_map(self) -> Dict[str, int]:
        """Load genre mapping from external config."""
        import os

        config_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "references",
            "config.json",
        )
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                return config.get("genre_map", {})
        except Exception as e:
            print(f"Warning: Could not load genre map from {config_path}: {e}")
            return {}

    def search_apps(
        self,
        term: str,
        limit: int = 10,
        entity: str = "software",
        genre_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Search for apps by keyword or genre.

        Args:
            term: Search keyword
            limit: Number of results (max 200)
            entity: Type of content ("software" for apps)
            genre_id: Optional App Store Genre ID

        Returns:
            Dictionary with search results
        """
        params = {
            "term": term,
            "country": self.country,
            "entity": entity,
            "limit": limit,
        }

        if genre_id:
            params["genreId"] = genre_id

        url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"

        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
                return data
        except urllib.error.URLError as e:
            return {
                "resultCount": 0,
                "results": [],
                "error": f"API request failed: {str(e)}",
            }
        except Exception as e:
            return {
                "resultCount": 0,
                "results": [],
                "error": f"Unexpected error: {str(e)}",
            }

    def get_app_by_id(self, app_id: str) -> Optional[Dict[str, Any]]:
        """
        Get app details by App Store ID.

        Args:
            app_id: Apple App Store ID

        Returns:
            App details dictionary or None if not found

        Example:
            >>> api = iTunesAPI()
            >>> app = api.get_app_by_id("572688855")  # Todoist
            >>> print(app['trackName'], app['description'])
        """
        params = {"id": app_id, "country": self.country, "entity": "software"}

        url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"

        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
                if data["resultCount"] > 0:
                    return data["results"][0]
                return None
        except Exception as e:
            print(f"Error fetching app {app_id}: {str(e)}")
            return None

    def get_app_by_name(self, app_name: str) -> Optional[Dict[str, Any]]:
        """
        Get app details by name (searches and returns first match).

        Args:
            app_name: App name to search for

        Returns:
            App details dictionary or None if not found

        Example:
            >>> api = iTunesAPI()
            >>> app = api.get_app_by_name("Todoist")
            >>> print(app['trackName'], app['averageUserRating'])
        """
        results = self.search_apps(app_name, limit=1)

        if results["resultCount"] > 0:
            return results["results"][0]
        return None

    def get_competitors(
        self, category: str, limit: int = 10, genre_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get top apps in a category or genre.

        Args:
            category: Category keyword (e.g., "productivity")
            limit: Number of competitors to fetch
            genre_id: Optional explicit Genre ID

        Returns:
            List of app dictionaries
        """
        # If no explicit genre_id, try to map the category string
        if not genre_id:
            normalized_cat = category.lower().replace(" ", "_").replace("&", "")
            genre_id = self.genre_map.get(normalized_cat)

        # If we have a genre_id, we can search with it
        # Note: term is still required by iTunes API, so we use category as term
        results = self.search_apps(category, limit=limit, genre_id=genre_id)
        return results.get("results", [])

    def extract_metadata(self, app_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant metadata for ASO analysis.

        Args:
            app_data: Raw app data from iTunes API

        Returns:
            Cleaned metadata dictionary
        """
        return {
            "app_id": app_data.get("trackId"),
            "app_name": app_data.get("trackName"),
            "bundle_id": app_data.get("bundleId"),
            "developer": app_data.get("artistName"),
            "category": app_data.get("primaryGenreName"),
            "genres": app_data.get("genres", []),
            "description": app_data.get("description", ""),
            "rating": app_data.get("averageUserRating", 0),
            "ratings_count": app_data.get("userRatingCount", 0),
            "price": app_data.get("formattedPrice", "Free"),
            "release_date": app_data.get("releaseDate"),
            "current_version": app_data.get("version"),
            "file_size": app_data.get("fileSizeBytes"),
            "content_rating": app_data.get("contentAdvisoryRating"),
            "screenshots": app_data.get("screenshotUrls", []),
            "ipad_screenshots": app_data.get("ipadScreenshotUrls", []),
            "screenshot_count": len(app_data.get("screenshotUrls", []))
            + len(app_data.get("ipadScreenshotUrls", [])),
            "has_video": bool(app_data.get("previewUrl") or app_data.get("videoUrl")),
            "icon_url": app_data.get("artworkUrl512") or app_data.get("artworkUrl100"),
            "app_store_url": app_data.get("trackViewUrl"),
        }

    def compare_competitors(self, competitor_names: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch and compare multiple competitors.

        Args:
            competitor_names: List of competitor app names

        Returns:
            List of extracted metadata for each competitor

        Example:
            >>> api = iTunesAPI()
            >>> competitors = api.compare_competitors([
            ...     "Todoist",
            ...     "Any.do",
            ...     "Microsoft To Do"
            ... ])
            >>> for comp in competitors:
            ...     print(f"{comp['app_name']}: {comp['rating']} ({comp['ratings_count']} ratings)")
        """
        results = []

        for name in competitor_names:
            app = self.get_app_by_name(name)
            if app:
                metadata = self.extract_metadata(app)
                results.append(metadata)
            else:
                print(f"Warning: Could not find app '{name}'")

        return results


def fetch_competitor_data(
    competitor_names: List[str], country: str = "us"
) -> List[Dict[str, Any]]:
    """
    Convenience function to fetch competitor data.

    Args:
        competitor_names: List of app names
        country: Country code

    Returns:
        List of competitor metadata dictionaries
    """
    api = iTunesAPI(country=country)
    return api.compare_competitors(competitor_names)


def main():
    """Test the iTunes API wrapper."""
    api = iTunesAPI()

    # Test 1: Search for apps
    print("Test 1: Searching for 'todoist'...")
    results = api.search_apps("todoist", limit=3)
    print(f"Found {results['resultCount']} results")

    if results["resultCount"] > 0:
        first_app = results["results"][0]
        print(
            f"  - {first_app['trackName']}: {first_app['averageUserRating']}★ ({first_app['userRatingCount']} ratings)"
        )

    # Test 2: Get specific app
    print("\nTest 2: Getting app by name...")
    app = api.get_app_by_name("Todoist")
    if app:
        metadata = api.extract_metadata(app)
        print(f"  App: {metadata['app_name']}")
        print(f"  Developer: {metadata['developer']}")
        print(f"  Rating: {metadata['rating']}★")
        print(f"  Ratings Count: {metadata['ratings_count']}")
        print(f"  Category: {metadata['category']}")

    # Test 3: Get competitors
    print("\nTest 3: Fetching top productivity apps...")
    competitors = api.get_competitors("productivity", limit=5)
    print(f"Found {len(competitors)} competitors:")
    for comp in competitors:
        print(f"  - {comp['trackName']}: {comp.get('averageUserRating', 'N/A')}★")

    # Test 4: Compare specific competitors
    print("\nTest 4: Comparing specific competitors...")
    comparison = api.compare_competitors(["Todoist", "Any.do", "Microsoft To Do"])
    print(f"Compared {len(comparison)} apps:")
    for comp in comparison:
        print(
            f"  - {comp['app_name']}: {comp['rating']}★ ({comp['ratings_count']:,} ratings)"
        )


if __name__ == "__main__":
    main()
