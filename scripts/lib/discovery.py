"""
Advanced competitor discovery logic for ASO analysis.
Combines Genre-based and Keyword-based discovery for a comprehensive market view.
"""

from typing import List, Dict, Any, Optional
import concurrent.futures
from scripts.lib.itunes_api import iTunesAPI


class DiscoveryEngine:
    """Orchestrates competitor discovery across multiple strategies."""

    def __init__(self, country: str = "us"):
        self.country = country.lower()
        self.api = iTunesAPI(country=self.country)

    def discover_competitors(
        self, category: str, keywords: Optional[List[str]] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Discover competitors using a multi-stage approach.

        1. Try mapping category to Genre ID for top apps in category.
        2. Supplement with keyword-based searches in parallel.
        3. Deduplicate and return top results.
        """
        all_competitors = {}

        # Stage 1: Genre-based discovery (Broader market view)
        normalized_cat = category.lower().replace(" ", "_").replace("&", "")
        genre_id = self.api.genre_map.get(normalized_cat)

        if genre_id:
            genre_results = self.api.get_competitors(
                category, limit=limit, genre_id=genre_id
            )
            for app in genre_results:
                track_id = app.get("trackId")
                if track_id:
                    all_competitors[track_id] = self.api.extract_metadata(app)

        # Stage 2: Keyword-based discovery (Specific niches) in parallel
        search_terms = [category]
        if keywords:
            search_terms.extend(keywords[:5])  # Take up to 5 keywords

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_term = {
                executor.submit(self.api.search_apps, term, limit=limit): term
                for term in search_terms
            }
            for future in concurrent.futures.as_completed(future_to_term):
                try:
                    keyword_results = future.result()
                    for app in keyword_results.get("results", []):
                        track_id = app.get("trackId")
                        if track_id and track_id not in all_competitors:
                            all_competitors[track_id] = self.api.extract_metadata(app)
                except Exception as exc:
                    print(
                        f"Search for {future_to_term[future]} generated an exception: {exc}"
                    )

        # Convert back to list and sort by ratings count (popularity proxy)
        results = list(all_competitors.values())
        results.sort(key=lambda x: x.get("ratings_count", 0), reverse=True)

        return results[:limit]
