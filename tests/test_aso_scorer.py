import unittest
import sys
import os

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.aso_scorer import ASOScorer

class TestASOScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = ASOScorer()

    def test_score_metadata_quality_perfect(self):
        metadata = {
            "title_keyword_count": 2,
            "title_length": 30,
            "description_length": 2000,
            "description_quality": 1.0,
            "keyword_density": 5.0
        }
        score = self.scorer.score_metadata_quality(metadata)
        self.assertEqual(score, 100.0)

    def test_score_metadata_quality_poor(self):
        metadata = {
            "title_keyword_count": 0,
            "title_length": 10,
            "description_length": 100,
            "description_quality": 0.1,
            "keyword_density": 0.5
        }
        score = self.scorer.score_metadata_quality(metadata)
        self.assertLess(score, 50.0)

    def test_score_ratings_reviews_high(self):
        ratings = {
            "average_rating": 4.5,
            "total_ratings": 10000,
            "recent_ratings_30d": 500
        }
        score = self.scorer.score_ratings_reviews(ratings)
        # 4.5 is target, 10000 > 5000 target, 500 > 100 target -> 50 + 30 + 20 = 100
        self.assertEqual(score, 100.0)

    def test_score_keyword_performance_excellent(self):
        keyword_perf = {
            "top_10": 10,
            "top_50": 20,
            "top_100": 30,
            "improving_keywords": 6
        }
        score = self.scorer.score_keyword_performance(keyword_perf)
        # Meets all targets (10, 20, 30, 6) -> 50 + 30 + 10 + 10 = 100
        self.assertEqual(score, 100.0)

    def test_score_visual_assets(self):
        # Default target: 5 screenshots, has_video: True
        visuals = {"screenshot_count": 5, "has_video": True}
        score = self.scorer.score_visual_assets(visuals)
        self.assertEqual(score, 100.0)
        
        visuals_poor = {"screenshot_count": 0, "has_video": False}
        score_poor = self.scorer.score_visual_assets(visuals_poor)
        self.assertEqual(score_poor, 0.0)

    def test_config_loading(self):
        # Verify that benchmarks are loaded from config.json
        self.assertIn("competitive", self.scorer.all_benchmarks)
        self.assertEqual(self.scorer.active_benchmarks["screenshots"]["target"], 5)

    def test_calculate_overall_score(self):
        metadata = {"title_keyword_count": 2, "title_length": 30, "description_length": 2000, "description_quality": 1.0, "keyword_density": 5.0}
        ratings = {"average_rating": 4.5, "total_ratings": 5000, "recent_ratings_30d": 101}
        keyword_perf = {"top_10": 10, "top_50": 20, "top_100": 30, "improving_keywords": 6}
        conversion = {"impression_to_install": 0.10, "downloads_last_30_days": 10001, "downloads_trend": "up"}
        visuals = {"screenshot_count": 5, "has_video": True}
        
        result = self.scorer.calculate_overall_score(metadata, ratings, keyword_perf, conversion, visuals=visuals)
        
        self.assertEqual(result["overall_score"], 100.0)
        self.assertEqual(result["health_status"], "Excellent - Top-tier ASO performance")
        self.assertIn("visual_assets", result["score_breakdown"])

    def test_platform_aware_google(self):
        scorer_google = ASOScorer(platform="google")
        # Google Play weights metadata_quality higher (20 base + 5 adjustment = 25)
        self.assertEqual(scorer_google.weights["metadata_quality"], 25)
        self.assertEqual(scorer_google.weights["visual_assets"], 15)

    def test_dynamic_benchmarking_competitive(self):
        # Default target rating is 4.5
        # Competitive target rating is 4.7
        scorer_comp = ASOScorer(category_context="competitive")
        
        ratings = {
            "average_rating": 4.6, # Above default target (4.5) but below competitive target (4.7)
            "total_ratings": 60000, # > 50000 target for competitive
            "recent_ratings_30d": 200
        }
        
        score_comp = scorer_comp.score_ratings_reviews(ratings)
        
        scorer_default = ASOScorer(category_context="default")
        score_default = scorer_default.score_ratings_reviews(ratings)
        
        # Default should be 100 because 4.6 > 4.5
        self.assertEqual(score_default, 100.0)
        # Competitive should be < 100 because 4.6 < 4.7
        self.assertLess(score_comp, 100.0)

if __name__ == '__main__':
    unittest.main()
