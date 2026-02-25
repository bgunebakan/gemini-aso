---
name: gemini-aso
description: Complete App Store Optimization (ASO) toolkit for mobile app performance on Apple App Store and Google Play Store. Use to research keywords, optimize metadata, analyze competitors, and calculate ASO health scores.
---

# Gemini ASO

This skill provides specialized tools and workflows for optimizing mobile applications for discoverability and conversion on major app stores.

## Core Capabilities

### 1. Keyword Research & Analysis
Analyze search volume, competition, and relevance to identify high-potential keywords.
- **Tool**: `scripts/keyword_analyzer.py`
- **Output**: Ranked keywords, difficulty scores, and long-tail opportunities.

### 2. Metadata Optimization
Generate and validate store listings (Title, Description, Keywords) against platform-specific constraints.
- **Tool**: `scripts/metadata_optimizer.py`
- **Constraints**: Automatically handles Apple (30/30/170/4000) and Google (50/80/4000) limits.

### 3. Competitor Intelligence
Deep-dive into top-performing apps to identify gaps and strategy overlaps.
- **Tool**: `scripts/competitor_analyzer.py`
- **Integration**: Uses `scripts/lib/itunes_api.py` for real-time Apple data.

### 4. Performance Scoring
Calculate an overall ASO health score (0-100) based on metadata quality, ratings, and keyword performance.
- **Tool**: `scripts/aso_scorer.py`
- **Context**: Supports `competitive`, `niche`, and `utility` benchmarks.
- **Platform**: Platform-aware weighting for `apple` vs `google`.

### 5. Reporting & Dashboards
Generate human-readable ASO audits and market overviews.
- **Formats**: Supports `--format markdown` for visual dashboards.
- **Logic**: Automated recommendation prioritization.

## Specialized Workflows
- **Review Analysis**: Extract sentiment and feature requests from user feedback via `scripts/review_analyzer.py`.
- **A/B Testing**: Design metadata experiments with `scripts/ab_test_planner.py`.
- **Global Reach**: Plan localization strategies using `scripts/localization_helper.py`.

## Quick Start

### Perform a Formatted ASO Audit
```json
{
  "metadata": {"title_length": 30, "description_length": 2500},
  "ratings": {"average_rating": 4.5, "total_ratings": 1000},
  "keyword_performance": {"top_10": 5},
  "conversion": {"impression_to_install": 0.05},
  "platform": "apple",
  "category_context": "competitive"
}
```
Run `python3 scripts/aso_scorer.py --format markdown < input.json` to get a visual health dashboard.

### Competitive Market Analysis
Ask Gemini: "Analyze the **Productivity** market on the **App Store**. Show me a formatted report with competitor rankings and keyword gaps."
Gemini will use `scripts/competitor_analyzer.py --format markdown` to generate the report.

## Resources

### scripts/
- `keyword_analyzer.py`: Main keyword engine.
- `metadata_optimizer.py`: Field-specific optimization and validation.
- `aso_scorer.py`: Comprehensive health scoring.
- `competitor_analyzer.py`: Market analysis tool.
- `lib/`: Contains `itunes_api.py` (official API wrapper) and `scraper.py` (WebFetch utilities).

### references/
- `config.json`: **Master Configuration**. Contains all genre mappings and category-specific benchmarks (Competitive, Niche, Utility).
- `sample_input.json`: Template for tool inputs.
- `expected_output.json`: Schema for tool responses.
- `agents.md`: Documentation on agent-coordinated workflows.

## Best Practices

1. **API First**: Always use the `iTunesAPI` for Apple data before falling back to scraping.
2. **Context Matters**: Specify a `category_context` (e.g., `competitive`) for more accurate scoring and tailored recommendations.
3. **Go Global**: Use the `country` parameter for international market research (supports all ISO codes).
4. **Markdown for Humans**: Use the `--format markdown` flag when you need a visual summary for the user.
5. **Validate**: Always run character count validation before proposing metadata changes.
6. **Singular Only**: Use singular forms in Apple's 100-character keyword field; plurals are auto-indexed.
