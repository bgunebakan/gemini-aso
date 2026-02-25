"""
ASO scoring module for App Store Optimization.
Calculates comprehensive ASO health score across multiple dimensions.
"""

from typing import Dict, List, Any, Optional


class ASOScorer:
    """Calculates overall ASO health score and provides recommendations."""

    # Default Score weights for different components (total = 100)
    DEFAULT_WEIGHTS = {
        "metadata_quality": 20,
        "ratings_reviews": 25,
        "keyword_performance": 25,
        "conversion_metrics": 20,
        "visual_assets": 10,
    }

    def __init__(self, category_context: str = "default", platform: str = "apple"):
        """
        Initialize ASO scorer.

        Args:
            category_context: 'competitive', 'niche', 'utility', or 'default'
            platform: 'apple' or 'google'
        """
        import json

        self.category_context = category_context.lower()
        self.platform = platform.lower()
        self.score_breakdown = {}

        # Load external config
        config = self._load_config()
        self.all_benchmarks = config.get("benchmarks", {})

        # Initialize weights and benchmarks
        self.weights = self.DEFAULT_WEIGHTS.copy()

        # Start with default benchmarks
        self.active_benchmarks = json.loads(
            json.dumps(self.all_benchmarks.get("default", {}))
        )

        self._apply_contextual_adjustments()

    def _load_config(self) -> Dict[str, Any]:
        """Load external benchmarks from config.json."""
        import os
        import json

        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "references",
            "config.json",
        )
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
            return {"benchmarks": {"default": {}}}

    def _apply_contextual_adjustments(self):
        """Apply platform and category specific adjustments to weights and benchmarks."""
        # Platform adjustments
        if self.platform == "google":
            # Google Play: Description is indexed for SEO
            self.weights["metadata_quality"] += 5
            self.weights["visual_assets"] += 5
            self.weights["conversion_metrics"] -= 10
        elif self.platform == "apple":
            # Apple: Visuals and Keywords are paramount
            self.weights["visual_assets"] += 5
            self.weights["metadata_quality"] -= 5

        # Category adjustments - Deep update from config
        if self.category_context in self.all_benchmarks:
            overrides = self.all_benchmarks[self.category_context]
            for key, values in overrides.items():
                if key in self.active_benchmarks:
                    for subkey, subvalue in values.items():
                        self.active_benchmarks[key][subkey] = subvalue

    def calculate_overall_score(
        self,
        metadata: Dict[str, Any],
        ratings: Dict[str, Any],
        keyword_performance: Dict[str, Any],
        conversion: Dict[str, Any],
        visuals: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive ASO score (0-100).

        Args:
            metadata: Title, description quality metrics
            ratings: Rating average and count
            keyword_performance: Keyword ranking data
            conversion: Impression-to-install metrics
            visuals: Screenshots count, video presence

        Returns:
            Overall score with detailed breakdown
        """
        if visuals is None:
            visuals = {}

        # Calculate component scores
        metadata_score = self.score_metadata_quality(metadata)
        ratings_score = self.score_ratings_reviews(ratings)
        keyword_score = self.score_keyword_performance(keyword_performance)
        conversion_score = self.score_conversion_metrics(conversion)
        visual_score = self.score_visual_assets(visuals)

        # Calculate weighted overall score
        total_weight = sum(self.weights.values())
        weighted_sum = (
            metadata_score * (self.weights["metadata_quality"])
            + ratings_score * (self.weights["ratings_reviews"])
            + keyword_score * (self.weights["keyword_performance"])
            + conversion_score * (self.weights["conversion_metrics"])
            + visual_score * (self.weights["visual_assets"])
        )

        overall_score = min(weighted_sum / total_weight, 100.0)

        # Store breakdown
        self.score_breakdown = {
            "metadata_quality": {
                "score": metadata_score,
                "weight": self.weights["metadata_quality"],
                "contribution": round(
                    metadata_score * (self.weights["metadata_quality"] / total_weight),
                    1,
                ),
            },
            "ratings_reviews": {
                "score": ratings_score,
                "weight": self.weights["ratings_reviews"],
                "contribution": round(
                    ratings_score * (self.weights["ratings_reviews"] / total_weight), 1
                ),
            },
            "keyword_performance": {
                "score": keyword_score,
                "weight": self.weights["keyword_performance"],
                "contribution": round(
                    keyword_score
                    * (self.weights["keyword_performance"] / total_weight),
                    1,
                ),
            },
            "conversion_metrics": {
                "score": conversion_score,
                "weight": self.weights["conversion_metrics"],
                "contribution": round(
                    conversion_score
                    * (self.weights["conversion_metrics"] / total_weight),
                    1,
                ),
            },
            "visual_assets": {
                "score": visual_score,
                "weight": self.weights["visual_assets"],
                "contribution": round(
                    visual_score * (self.weights["visual_assets"] / total_weight), 1
                ),
            },
        }

        # Generate recommendations
        recommendations = self.generate_recommendations(
            metadata_score, ratings_score, keyword_score, conversion_score, visual_score
        )

        # Assess overall health
        health_status = self._assess_health_status(overall_score)

        return {
            "overall_score": round(overall_score, 1),
            "health_status": health_status,
            "platform": self.platform,
            "category_context": self.category_context,
            "score_breakdown": self.score_breakdown,
            "recommendations": recommendations,
            "priority_actions": self._prioritize_actions(recommendations),
            "strengths": self._identify_strengths(self.score_breakdown),
            "weaknesses": self._identify_weaknesses(self.score_breakdown),
        }

    def score_metadata_quality(self, metadata: Dict[str, Any]) -> float:
        """
        Score metadata quality (0-100).

        Evaluates:
        - Title optimization
        - Description quality
        - Keyword usage
        """
        scores = []

        # Title score (0-35 points)
        title_keywords = metadata.get("title_keyword_count", 0)
        title_length = metadata.get("title_length", 0)

        title_score = 0
        if title_keywords >= self.active_benchmarks["title_keyword_usage"]["target"]:
            title_score = 35
        elif title_keywords >= self.active_benchmarks["title_keyword_usage"]["min"]:
            title_score = 25
        else:
            title_score = 10

        # Adjust for title length usage
        if title_length > 10:  # Reasonable title length
            title_score += 0
        else:
            title_score -= 10

        scores.append(min(title_score, 35))

        # Description score (0-35 points)
        desc_length = metadata.get("description_length", 0)
        desc_quality = metadata.get("description_quality", 0.0)  # 0-1 scale

        # Platform specific description weighting
        desc_base_weight = 25
        if self.platform == "google":
            desc_base_weight = 30  # Google cares more about description length/content

        desc_score = 0
        if desc_length >= self.active_benchmarks["description_length"]["target"]:
            desc_score = desc_base_weight
        elif desc_length >= self.active_benchmarks["description_length"]["min"]:
            desc_score = desc_base_weight - 10
        else:
            desc_score = 5

        # Add quality bonus
        desc_score += desc_quality * 10
        scores.append(min(desc_score, 35))

        # Keyword density score (0-30 points)
        keyword_density = metadata.get("keyword_density", 0.0)

        if (
            self.active_benchmarks["keyword_density"]["min"]
            <= keyword_density
            <= self.active_benchmarks["keyword_density"]["optimal"]
        ):
            density_score = 30
        elif keyword_density < self.active_benchmarks["keyword_density"]["min"]:
            # Too low - proportional scoring
            density_score = (
                keyword_density / self.active_benchmarks["keyword_density"]["min"]
            ) * 20
        else:
            # Too high (keyword stuffing) - penalty
            excess = (
                keyword_density - self.active_benchmarks["keyword_density"]["optimal"]
            )
            density_score = max(30 - (excess * 5), 0)

        scores.append(density_score)

        return round(sum(scores), 1)

    def score_ratings_reviews(self, ratings: Dict[str, Any]) -> float:
        """
        Score ratings and reviews (0-100).

        Evaluates:
        - Average rating
        - Total ratings count
        - Review velocity
        """
        average_rating = ratings.get("average_rating", 0.0)
        total_ratings = ratings.get("total_ratings", 0)
        recent_ratings = ratings.get("recent_ratings_30d", 0)

        # Rating quality score (0-50 points)
        if average_rating >= self.active_benchmarks["average_rating"]["target"]:
            rating_quality_score = 50
        elif average_rating >= self.active_benchmarks["average_rating"]["min"]:
            # Proportional scoring between min and target
            proportion = (
                average_rating - self.active_benchmarks["average_rating"]["min"]
            ) / (
                self.active_benchmarks["average_rating"]["target"]
                - self.active_benchmarks["average_rating"]["min"]
            )
            rating_quality_score = 30 + (proportion * 20)
        elif average_rating >= 3.0:
            rating_quality_score = 20
        else:
            rating_quality_score = 10

        # Rating volume score (0-30 points)
        if total_ratings >= self.active_benchmarks["ratings_count"]["target"]:
            rating_volume_score = 30
        elif total_ratings >= self.active_benchmarks["ratings_count"]["min"]:
            # Proportional scoring
            proportion = (
                total_ratings - self.active_benchmarks["ratings_count"]["min"]
            ) / (
                self.active_benchmarks["ratings_count"]["target"]
                - self.active_benchmarks["ratings_count"]["min"]
            )
            rating_volume_score = 15 + (proportion * 15)
        else:
            # Very low volume
            rating_volume_score = (
                total_ratings / self.active_benchmarks["ratings_count"]["min"]
            ) * 15

        # Rating velocity score (0-20 points)
        if recent_ratings > 100:
            velocity_score = 20
        elif recent_ratings > 50:
            velocity_score = 15
        elif recent_ratings > 10:
            velocity_score = 10
        else:
            velocity_score = 5

        total_score = rating_quality_score + rating_volume_score + velocity_score

        return round(total_score, 1)

    def score_keyword_performance(self, keyword_performance: Dict[str, Any]) -> float:
        """
        Score keyword ranking performance (0-100).

        Evaluates:
        - Top 10 rankings
        - Top 50 rankings
        - Ranking trends
        """
        top_10_count = keyword_performance.get("top_10", 0)
        top_50_count = keyword_performance.get("top_50", 0)
        top_100_count = keyword_performance.get("top_100", 0)
        improving_keywords = keyword_performance.get("improving_keywords", 0)

        # Top 10 score (0-50 points) - most valuable rankings
        if top_10_count >= self.active_benchmarks["keywords_top_10"]["target"]:
            top_10_score = 50
        elif top_10_count >= self.active_benchmarks["keywords_top_10"]["min"]:
            proportion = (
                top_10_count - self.active_benchmarks["keywords_top_10"]["min"]
            ) / (
                self.active_benchmarks["keywords_top_10"]["target"]
                - self.active_benchmarks["keywords_top_10"]["min"]
            )
            top_10_score = 25 + (proportion * 25)
        else:
            top_10_score = (
                top_10_count / self.active_benchmarks["keywords_top_10"]["min"]
            ) * 25

        # Top 50 score (0-30 points)
        if top_50_count >= self.active_benchmarks["keywords_top_50"]["target"]:
            top_50_score = 30
        elif top_50_count >= self.active_benchmarks["keywords_top_50"]["min"]:
            proportion = (
                top_50_count - self.active_benchmarks["keywords_top_50"]["min"]
            ) / (
                self.active_benchmarks["keywords_top_50"]["target"]
                - self.active_benchmarks["keywords_top_50"]["min"]
            )
            top_50_score = 15 + (proportion * 15)
        else:
            top_50_score = (
                top_50_count / self.active_benchmarks["keywords_top_50"]["min"]
            ) * 15

        # Coverage score (0-10 points) - based on top 100
        coverage_score = min((top_100_count / 30) * 10, 10)

        # Trend score (0-10 points) - are rankings improving?
        if improving_keywords > 5:
            trend_score = 10
        elif improving_keywords > 0:
            trend_score = 5
        else:
            trend_score = 0

        total_score = top_10_score + top_50_score + coverage_score + trend_score

        return round(total_score, 1)

    def score_conversion_metrics(self, conversion: Dict[str, Any]) -> float:
        """
        Score conversion performance (0-100).

        Evaluates:
        - Impression-to-install conversion rate
        - Download velocity
        """
        conversion_rate = conversion.get("impression_to_install", 0.0)
        downloads_30d = conversion.get("downloads_last_30_days", 0)
        downloads_trend = conversion.get(
            "downloads_trend", "stable"
        )  # 'up', 'stable', 'down'

        # Conversion rate score (0-70 points)
        if conversion_rate >= self.active_benchmarks["conversion_rate"]["target"]:
            conversion_score = 70
        elif conversion_rate >= self.active_benchmarks["conversion_rate"]["min"]:
            proportion = (
                conversion_rate - self.active_benchmarks["conversion_rate"]["min"]
            ) / (
                self.active_benchmarks["conversion_rate"]["target"]
                - self.active_benchmarks["conversion_rate"]["min"]
            )
            conversion_score = 35 + (proportion * 35)
        else:
            conversion_score = (
                conversion_rate / self.active_benchmarks["conversion_rate"]["min"]
            ) * 35

        # Download velocity score (0-20 points)
        if downloads_30d > 10000:
            velocity_score = 20
        elif downloads_30d > 1000:
            velocity_score = 15
        elif downloads_30d > 100:
            velocity_score = 10
        else:
            velocity_score = 5

        # Trend bonus (0-10 points)
        if downloads_trend == "up":
            trend_score = 10
        elif downloads_trend == "stable":
            trend_score = 5
        else:
            trend_score = 0

        total_score = conversion_score + velocity_score + trend_score

        return round(total_score, 1)

    def score_visual_assets(self, visuals: Dict[str, Any]) -> float:
        """
        Score visual assets quality (0-100).

        Evaluates:
        - Screenshot count
        - Video presence
        """
        screenshot_count = visuals.get("screenshot_count", 0)
        has_video = visuals.get("has_video", False)

        # Screenshot score (0-70 points)
        target = self.active_benchmarks.get("screenshots", {}).get("target", 5)
        min_count = self.active_benchmarks.get("screenshots", {}).get("min", 3)

        if screenshot_count >= target:
            screenshot_score = 70
        elif screenshot_count >= min_count:
            screenshot_score = (
                40 + ((screenshot_count - min_count) / (target - min_count)) * 30
            )
        else:
            screenshot_score = (
                (screenshot_count / min_count) * 40 if min_count > 0 else 0
            )

        # Video bonus (0-30 points)
        video_score = 30 if has_video else 0

        return round(screenshot_score + video_score, 1)

    def generate_recommendations(
        self,
        metadata_score: float,
        ratings_score: float,
        keyword_score: float,
        conversion_score: float,
        visual_score: float = 100.0,
    ) -> List[Dict[str, Any]]:
        """Generate prioritized recommendations based on scores."""
        recommendations = []

        # Metadata recommendations
        if metadata_score < 60:
            recommendations.append(
                {
                    "category": "metadata_quality",
                    "priority": "high",
                    "action": "Optimize app title and description",
                    "details": "Add more keywords to title, expand description to 1500-2000 characters, improve keyword density to 3-5%",
                    "expected_impact": "Improve discoverability and ranking potential",
                }
            )
        elif metadata_score < 80:
            recommendations.append(
                {
                    "category": "metadata_quality",
                    "priority": "medium",
                    "action": "Refine metadata for better keyword targeting",
                    "details": "Test variations of title/subtitle, optimize keyword field for Apple",
                    "expected_impact": "Incremental ranking improvements",
                }
            )

        # Ratings recommendations
        if ratings_score < 60:
            recommendations.append(
                {
                    "category": "ratings_reviews",
                    "priority": "high",
                    "action": "Improve rating quality and volume",
                    "details": "Address top user complaints, implement in-app rating prompts, respond to negative reviews",
                    "expected_impact": "Better conversion rates and trust signals",
                }
            )
        elif ratings_score < 80:
            recommendations.append(
                {
                    "category": "ratings_reviews",
                    "priority": "medium",
                    "action": "Increase rating velocity",
                    "details": "Optimize timing of rating requests, encourage satisfied users to rate",
                    "expected_impact": "Sustained rating quality",
                }
            )

        # Keyword performance recommendations
        if keyword_score < 60:
            recommendations.append(
                {
                    "category": "keyword_performance",
                    "priority": "high",
                    "action": "Improve keyword rankings",
                    "details": "Target long-tail keywords with lower competition, update metadata with high-potential keywords, build backlinks",
                    "expected_impact": "Significant improvement in organic visibility",
                }
            )
        elif keyword_score < 80:
            recommendations.append(
                {
                    "category": "keyword_performance",
                    "priority": "medium",
                    "action": "Expand keyword coverage",
                    "details": "Target additional related keywords, test seasonal keywords, localize for new markets",
                    "expected_impact": "Broader reach and more discovery opportunities",
                }
            )

        # Conversion recommendations
        if conversion_score < 60:
            recommendations.append(
                {
                    "category": "conversion_metrics",
                    "priority": "high",
                    "action": "Optimize store listing for conversions",
                    "details": "Improve screenshots and icon, strengthen value proposition in description, add video preview",
                    "expected_impact": "Higher impression-to-install conversion",
                }
            )
        elif conversion_score < 80:
            recommendations.append(
                {
                    "category": "conversion_metrics",
                    "priority": "medium",
                    "action": "Test visual asset variations",
                    "details": "A/B test different icon designs and screenshot sequences",
                    "expected_impact": "Incremental conversion improvements",
                }
            )

        # Visual asset recommendations
        if visual_score < 60:
            recommendations.append(
                {
                    "category": "visual_assets",
                    "priority": "high",
                    "action": "Enhance visual presentation",
                    "details": f"Increase screenshot count to at least {self.active_benchmarks.get('screenshots', {}).get('target', 5)}, add a video preview",
                    "expected_impact": "Drastic improvement in conversion rate",
                }
            )

        return recommendations

    def _assess_health_status(self, overall_score: float) -> str:
        """Assess overall ASO health status."""
        if overall_score >= 80:
            return "Excellent - Top-tier ASO performance"
        elif overall_score >= 65:
            return "Good - Competitive ASO with room for improvement"
        elif overall_score >= 50:
            return "Fair - Needs strategic improvements"
        else:
            return "Poor - Requires immediate ASO overhaul"

    def _prioritize_actions(
        self, recommendations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Prioritize actions by impact and urgency."""
        # Sort by priority (high first) and expected impact
        priority_order = {"high": 0, "medium": 1, "low": 2}

        sorted_recommendations = sorted(
            recommendations, key=lambda x: priority_order[x["priority"]]
        )

        return sorted_recommendations[:3]  # Top 3 priority actions

    def _identify_strengths(self, score_breakdown: Dict[str, Any]) -> List[str]:
        """Identify areas of strength (scores >= 75)."""
        strengths = []

        for category, data in score_breakdown.items():
            if data["score"] >= 75:
                strengths.append(
                    f"{category.replace('_', ' ').title()}: {data['score']}/100"
                )

        return (
            strengths if strengths else ["Focus on building strengths across all areas"]
        )

    def _identify_weaknesses(self, score_breakdown: Dict[str, Any]) -> List[str]:
        """Identify areas needing improvement (scores < 60)."""
        weaknesses = []

        for category, data in score_breakdown.items():
            if data["score"] < 60:
                weaknesses.append(
                    f"{category.replace('_', ' ').title()}: {data['score']}/100 - needs improvement"
                )

        return weaknesses if weaknesses else ["All areas performing adequately"]


def calculate_aso_score(
    metadata: Dict[str, Any],
    ratings: Dict[str, Any],
    keyword_performance: Dict[str, Any],
    conversion: Dict[str, Any],
    visuals: Optional[Dict[str, Any]] = None,
    category_context: str = "default",
    platform: str = "apple",
) -> Dict[str, Any]:
    """
    Convenience function to calculate ASO score.

    Args:
        metadata: Metadata quality metrics
        ratings: Ratings data
        keyword_performance: Keyword ranking data
        conversion: Conversion metrics
        visuals: Screenshots and video data
        category_context: 'competitive', 'niche', 'utility', or 'default'
        platform: 'apple' or 'google'

    Returns:
        Complete ASO score report
    """
    scorer = ASOScorer(category_context=category_context, platform=platform)
    return scorer.calculate_overall_score(
        metadata, ratings, keyword_performance, conversion, visuals=visuals
    )


if __name__ == "__main__":
    import sys
    import json
    import argparse
    import os

    # Add parent directory to path to allow importing from scripts.lib
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scripts.lib.reporter import format_aso_report

    parser = argparse.ArgumentParser(description="Calculate ASO Health Score")
    parser.add_argument(
        "--format", choices=["json", "markdown"], default="json", help="Output format"
    )

    # Argparse and sys.stdin.read() don't mix perfectly if we want to support both
    # We'll use a simple check
    args, unknown = parser.parse_known_args()

    try:
        input_data = json.load(sys.stdin)
        metadata = input_data.get("metadata", {})
        ratings = input_data.get("ratings", {})
        keyword_perf = input_data.get("keyword_performance", {})
        conversion = input_data.get("conversion", {})
        visuals = input_data.get("visuals", {})

        # New parameters from JSON input
        category_context = input_data.get("category_context", "default")
        platform = input_data.get("platform", "apple")

        results = calculate_aso_score(
            metadata,
            ratings,
            keyword_perf,
            conversion,
            visuals=visuals,
            category_context=category_context,
            platform=platform,
        )

        if args.format == "markdown":
            print(format_aso_report(results))
        else:
            print(json.dumps(results, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
