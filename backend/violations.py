import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def _load_json(filename: str) -> dict:
    with open(DATA_DIR / filename) as f:
        return json.load(f)


def enrich_violations(analysis: dict) -> dict:
    """Take raw Gemini analysis and enrich with ADA codes and cost estimates."""
    ada_codes = _load_json("ada_codes.json")
    cost_estimates = _load_json("cost_estimates.json")

    enriched_violations = []
    total_cost_low = 0
    total_cost_high = 0

    for violation in analysis.get("violations", []):
        vtype = violation["violation_type"]

        code_info = ada_codes.get(vtype, {})
        cost_info = cost_estimates.get(vtype, {})

        enriched = {
            **violation,
            "ada_section": code_info.get("ada_section", "N/A"),
            "ada_title": code_info.get("title", "N/A"),
            "ada_requirement": code_info.get("requirement", ""),
            "cost_low": cost_info.get("low", 0),
            "cost_high": cost_info.get("high", 0),
            "cost_unit": cost_info.get("unit", ""),
            "remediation": cost_info.get("description", ""),
            "cost_factors": cost_info.get("factors", []),
        }
        enriched_violations.append(enriched)

        total_cost_low += cost_info.get("low", 0)
        total_cost_high += cost_info.get("high", 0)

    return {
        "violations": enriched_violations,
        "positive_features": analysis.get("positive_features", []),
        "overall_risk": analysis.get("overall_risk", "unknown"),
        "summary": analysis.get("summary", ""),
        "total_estimated_cost": {
            "low": total_cost_low,
            "high": total_cost_high,
        },
        "violation_count": len(enriched_violations),
        "disclaimer": "This is an automated pre-screening tool. A professional CASp inspector or ADA consultant should verify findings before remediation. Small businesses may qualify for up to $5,000 in tax credits for accessibility improvements (IRS Form 8826).",
    }
