# Gemini ASO Skill

A comprehensive App Store Optimization (ASO) toolkit for the Gemini CLI. This skill transforms Gemini into a specialized ASO expert capable of researching keywords, optimizing metadata, and analyzing competitors for both the Apple App Store and Google Play Store.

## Overview

The **Gemini ASO Skill** bridges the gap between manual store optimization and expensive ASO tools. It leverages official APIs (iTunes Search API) and agentic web scraping (WebFetch) to provide data-driven insights and automated metadata generation.

## Folder Structure

The skill follows the standard Gemini CLI skill architecture:

```text
gemini-aso/
├── SKILL.md              # Core instructions and triggering logic for Gemini
├── gemini-aso.skill      # Distributable package (generated)
├── install.sh            # Verified installer with test validation
├── scripts/              # Executable Python logic
│   ├── aso_scorer.py           # Health scoring engine (context-aware)
│   ├── competitor_analyzer.py  # Market gap & discovery engine
│   ├── ...
│   └── lib/                    # Shared utilities
│       ├── discovery.py        # Concurrent discovery logic
│       ├── reporter.py         # Markdown dashboard generator
│       ├── itunes_api.py       # Global Apple API wrapper
│       └── scraper.py          # WebFetch extraction utilities
├── tests/                # Comprehensive unit and E2E tests
├── references/           # Documentation, config and data schemas
│   ├── config.json             # EXTERNALIZED benchmarks and genre maps
│   ├── agents.md               # Agent coordination guide
│   ├── sample_input.json       # Input templates
│   └── expected_output.json    # Response schemas
└── assets/               # Placeholders for future visual templates
```

## Features

### 1. Context-Aware Performance Scoring
- **Dynamic Benchmarks**: Automatically adjusts targets for `Competitive`, `Niche`, or `Utility` apps.
- **Platform-Aware**: Differential weighting for Apple App Store vs. Google Play Store logic.
- **Visual Analysis**: Evaluates screenshot density and video presence as conversion factors.

### 2. Concurrent Competitor Discovery
- **Multi-Stage Engine**: Combines Genre-based (top charts) and Keyword-based discovery.
- **High Speed**: Leverages parallel execution to reduce market audit latency by up to 70%.
- **Global Reach**: Full support for localized analysis via `country` parameters (e.g., `us`, `jp`, `gb`).

### 3. Visual Dashboards
- **Markdown Reporting**: Generates professional dashboards with progress bars and comparison tables.
- **Actionable Insights**: Prioritizes ASO "Quick Wins" and long-term strategic improvements.

### 4. Metadata Optimization & Keyword Intelligence
- **Platform Limits**: Handles Apple (30/30/170/4000) and Google (50/80/4000) character limits.
- **Difficulty Scoring**: Quantitative 0-100 scores to prioritize keyword targeting.

## Installation

1. **Run Verified Installer**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
   *Note: The installer automatically runs the test suite before proceeding.*

2. **Reload Gemini Session**:
   ```bash
   /skills reload
   ```

## Usage Examples

Once installed, you can interact with the skill using natural language:

### Global Market Audit
> "Analyze the **Fitness** market in **Japan**. Show me a formatted report with competitor rankings and keyword gaps."

### Localized Metadata Generation
> "Optimize my app 'ZenMode' for the **UK market**. 
> Name: ZenMode
> Features: Guided meditation, ambient noise.
> Target: Stressed professionals."

### Visual Health Check
> "Run a performance audit for my app. I have **2 screenshots** and **no video**. 
> Rating: 4.2. Category: Competitive Productivity."

## Technical Details

- **Language**: Python 3.8+
- **Dependencies**: Zero external dependencies (Standard Library only).
- **Architecture**: CLI Wrapper with parallel execution and externalized configuration (`config.json`).

## Contributors

- Bilal Tonga (bilaltonga@gmail.com)

## License

MIT License. See `LICENSE.md` in the root repository.
