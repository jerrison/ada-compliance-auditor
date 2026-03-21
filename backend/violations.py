import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

CONFIRMED_THRESHOLD = 0.7


def _load_json(filename: str) -> dict:
    with open(DATA_DIR / filename) as f:
        return json.load(f)


def enrich_violations(analysis: dict) -> dict:
    """Take raw Gemini analysis and enrich with ADA codes, California CBC codes, and cost estimates."""
    ada_codes = _load_json("ada_codes.json")
    california_codes = _load_json("california_codes.json")
    cost_estimates = _load_json("cost_estimates.json")

    enriched_violations = []
    total_cost_low = 0
    total_cost_high = 0
    confirmed_count = 0
    potential_count = 0

    for violation in analysis.get("violations", []):
        vtype = violation["violation_type"]

        code_info = ada_codes.get(vtype, {})
        cbc_info = california_codes.get(vtype, {})
        cost_info = cost_estimates.get(vtype, {})

        enriched = {
            **violation,
            # Federal ADA fields
            "ada_section": code_info.get("ada_section", "N/A"),
            "ada_title": code_info.get("title", "N/A"),
            "ada_requirement": code_info.get("requirement", ""),
            # California CBC fields
            "cbc_section": cbc_info.get("cbc_section", "N/A"),
            "cbc_title": cbc_info.get("title", "N/A"),
            "cbc_requirement": cbc_info.get("requirement", ""),
            "stricter_than_federal": cbc_info.get("stricter_than_federal", False),
            "stricter_note": cbc_info.get("stricter_note"),
            # Cost fields
            "cost_low": cost_info.get("low", 0),
            "cost_high": cost_info.get("high", 0),
            "cost_unit": cost_info.get("unit", ""),
            "remediation": cost_info.get("description", ""),
            "cost_factors": cost_info.get("factors", []),
        }
        enriched_violations.append(enriched)

        total_cost_low += cost_info.get("low", 0)
        total_cost_high += cost_info.get("high", 0)

        # Track confirmed vs potential based on confidence threshold
        confidence = violation.get("confidence", 0)
        if confidence >= CONFIRMED_THRESHOLD:
            confirmed_count += 1
        else:
            potential_count += 1

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
        "confirmed_count": confirmed_count,
        "potential_count": potential_count,
        "disclaimer": "This is an automated pre-screening tool based on federal ADA standards and California CBC Title 24 requirements. A professional CASp (Certified Access Specialist) inspector or ADA consultant should verify findings before remediation. Small businesses may qualify for up to $5,000 in tax credits for accessibility improvements (IRS Form 8826).",
    }
