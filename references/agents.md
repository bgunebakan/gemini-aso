# ASO Agent Coordination Guide

This guide explains how specialized agents can coordinate using the Gemini ASO toolkit to perform complex, multi-stage App Store Optimization tasks.

## Agent Roles & Script Mapping

The toolkit is designed for modularity, allowing different agents to handle specific parts of the ASO lifecycle:

| Agent Role | Responsibility | Primary Scripts |
| :--- | :--- | :--- |
| **ASO Researcher** | Market and keyword discovery | `scripts/keyword_analyzer.py`, `scripts/lib/discovery.py` |
| **ASO Optimizer** | Metadata generation and validation | `scripts/metadata_optimizer.py`, `scripts/lib/itunes_api.py` |
| **ASO Strategist** | Health scoring and action planning | `scripts/aso_scorer.py`, `scripts/lib/reporter.py` |

---

## Coordinated Workflows

### 1. The Full Market Audit Workflow
An agent (e.g., "ASO Master") can orchestrate a full audit by chaining these tools:

1.  **Phase 1 (Discovery):** Use `DiscoveryEngine` to find the top 10 competitors in a category (e.g., "Productivity").
2.  **Phase 2 (Analysis):** Pass the discovered data to `scripts/competitor_analyzer.py` to identify keyword gaps.
3.  **Phase 3 (Strategy):** Use `scripts/aso_scorer.py --format markdown` to generate a visual dashboard with prioritized actions.

### 2. The International Expansion Workflow
1.  **Phase 1:** Use `DiscoveryEngine(country="jp")` to understand the local Japanese market.
2.  **Phase 2:** Pass findings to `scripts/localization_helper.py` to plan the translation and cultural adaptation strategy.

---

## Technical Handoff Examples

Agents should pass data between themselves using the standardized JSON format defined in `references/sample_input.json`.

**Example: Researcher to Optimizer Handoff**
```json
{
  "discovered_keywords": ["task manager", "todo list", "productivity"],
  "competitor_metadata": [...],
  "target_platform": "apple"
}
```

## Best Practices for Agent Developers

1.  **Stateless Execution:** Each script is a "pure function" (JSON in → JSON out). Agents should maintain the session state and pass only what's needed.
2.  **Format Selection:**
    *   Use **JSON** for internal agent-to-agent communication.
    *   Use **Markdown** (via `--format markdown`) only when the agent is presenting the final results to the user.
3.  **Validation First:** Agents should always run `scripts/metadata_optimizer.py` to validate metadata against store limits before suggesting it to a user.

---

## Summary
The Gemini ASO toolkit is optimized for **Agentic Workflows**. By treating each script as a specialized "skill," agents can solve complex optimization problems that would be difficult for a general-purpose LLM alone.
