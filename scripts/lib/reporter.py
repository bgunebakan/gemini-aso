"""
Utility for generating Markdown reports for ASO analysis.
"""

from typing import List, Dict, Any


def generate_markdown_table(headers: List[str], rows: List[List[Any]]) -> str:
    """Generate a formatted Markdown table."""
    if not headers or not rows:
        return ""

    # Header
    table = "| " + " | ".join(headers) + " |\n"
    # Separator
    table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    # Rows
    for row in rows:
        table += "| " + " | ".join(map(str, row)) + " |\n"

    return table


def generate_progress_bar(value: float, total: float = 100, length: int = 20) -> str:
    """Generate a visual progress bar using ASCII characters."""
    filled_length = int(length * value // total)
    bar = "█" * filled_length + "░" * (length - filled_length)
    return f"|{bar}| {value}/{total}"


def format_aso_report(results: Dict[str, Any]) -> str:
    """Format the ASO Health Score results as a Markdown dashboard."""
    report = f"# ASO Health Report: {results.get('overall_score', 0)}/100\n\n"

    report += f"**Status:** {results.get('health_status', 'N/A')}\n"
    report += f"**Platform:** {results.get('platform', 'N/A').title()}\n"
    report += (
        f"**Category Context:** {results.get('category_context', 'N/A').title()}\n\n"
    )

    report += "## Score Breakdown\n"
    breakdown_headers = ["Category", "Score", "Weight", "Visual"]
    breakdown_rows = []

    # Sort categories to ensure consistent output
    categories = [
        "metadata_quality",
        "ratings_reviews",
        "keyword_performance",
        "conversion_metrics",
        "visual_assets",
    ]
    for cat in categories:
        if cat in results.get("score_breakdown", {}):
            data = results["score_breakdown"][cat]
            name = cat.replace("_", " ").title()
            score = data.get("score", 0)
            weight = f"{data.get('weight', 0)}%"
            bar = generate_progress_bar(score)
            breakdown_rows.append([name, score, weight, bar])

    report += generate_markdown_table(breakdown_headers, breakdown_rows)
    report += "\n"

    report += "## Priority Actions\n"
    for action in results.get("priority_actions", []):
        report += (
            f"### 🔴 {action['action']} (Priority: {action['priority'].upper()})\n"
        )
        report += f"- **Details:** {action['details']}\n"
        report += f"- **Expected Impact:** {action['expected_impact']}\n\n"

    report += "## Strengths & Weaknesses\n"
    report += "### ✅ Strengths\n"
    for strength in results.get("strengths", []):
        report += f"- {strength}\n"

    report += "\n### ⚠️ Weaknesses\n"
    for weakness in results.get("weaknesses", []):
        report += f"- {weakness}\n"

    return report


def format_competitor_report(results: Dict[str, Any]) -> str:
    """Format the Competitor Analysis results as a Markdown dashboard."""
    report = f"# Competitor Analysis: {results.get('category', 'N/A')}\n\n"

    report += "## Market Overview\n"
    stats = results.get("rating_analysis", {})
    report += f"- **Average Rating:** {stats.get('average_rating')}★\n"
    report += f"- **Total Ratings in Sample:** {stats.get('total_ratings_in_category', 0):,}\n\n"

    report += "## Competitor Rankings\n"
    rank_headers = ["Rank", "App Name", "Rating", "Reviews", "Strength"]
    rank_rows = []

    for i, comp in enumerate(results.get("ranked_competitors", []), 1):
        name = comp.get("app_name")
        rating = f"{comp.get('rating_metrics', {}).get('rating')}★"
        reviews = f"{comp.get('rating_metrics', {}).get('ratings_count', 0):,}"
        strength = comp.get("competitive_strength", 0)
        rank_rows.append([i, name, rating, reviews, f"{strength}/100"])

    report += generate_markdown_table(rank_headers, rank_rows)
    report += "\n"

    report += "## Common Keywords & Gaps\n"
    report += f"**Top Shared Keywords:** {', '.join(results.get('common_keywords', [])[:10])}\n\n"

    report += "### Keyword Opportunities (Gaps)\n"
    gap_headers = ["Keyword", "Used By", "Usage %"]
    gap_rows = []
    for gap in results.get("keyword_gaps", []):
        gap_rows.append(
            [gap["keyword"], len(gap["used_by"]), f"{gap['usage_percentage']}%"]
        )

    report += generate_markdown_table(gap_headers, gap_rows)
    report += "\n"

    report += "## Actionable Opportunities\n"
    for opp in results.get("opportunities", []):
        report += f"- {opp}\n"

    return report
