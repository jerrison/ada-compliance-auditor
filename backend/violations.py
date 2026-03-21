import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

_kb = None

CONFIRMED_THRESHOLD = 0.7


def _load_kb():
    global _kb
    if _kb is None:
        with open(DATA_DIR / "ada_knowledge_base.json") as f:
            _kb = json.load(f)
    return _kb


SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}

TAX_CREDITS = [
    {
        "name": "Federal Disabled Access Credit",
        "form": "IRS 8826",
        "max_amount": 5000,
        "eligibility": "Small businesses with <$1M revenue or <30 employees",
    },
    {
        "name": "Federal Barrier Removal Deduction",
        "section": "IRC 190",
        "max_amount": 15000,
        "eligibility": "Any business",
    },
    {
        "name": "CA CASp Inspection Tax Credit",
        "max_amount": 250,
        "eligibility": "After qualified CASp inspection",
    },
]

NEXT_STEPS = [
    "Schedule a CASp inspection for legal protection under SB 1608",
    "Address high-severity violations first — highest legal exposure",
    "Contact SF Mayor's Office on Disability for technical assistance",
    "Small businesses: file IRS Form 8826 for up to $5,000 in access credits",
]

DISCLAIMER = (
    "This is an AI-powered pre-screening tool. A Certified Access Specialist (CASp) "
    "or ADA consultant should verify findings before remediation. This report does not "
    "constitute legal advice. Cost estimates reflect SF market rates and are approximate."
)


def _compute_overall_risk(violations):
    severities = {v.get("severity") for v in violations}
    if "high" in severities:
        return "high"
    if "medium" in severities:
        return "medium"
    if "low" in severities:
        return "low"
    return "none"


def _generate_headline(violations):
    if not violations:
        return "No accessibility violations detected"
    by_sev = {}
    categories = set()
    for v in violations:
        sev = v.get("severity", "low")
        by_sev[sev] = by_sev.get(sev, 0) + 1
        categories.add(v.get("category", "general"))
    top_sev = "critical" if "high" in by_sev else "moderate" if "medium" in by_sev else "minor"
    count = by_sev.get("high", by_sev.get("medium", by_sev.get("low", 0)))
    cat_str = " and ".join(sorted(categories)[:2])
    barrier = "barrier" if count == 1 else "barriers"
    return f"{count} {top_sev} access {barrier} found — {cat_str} require attention"


def _sort_key(violation):
    sev = SEVERITY_ORDER.get(violation.get("severity", "low"), 2)
    conf = -(violation.get("confidence", 0))
    cost = violation.get("estimated_cost", 0)
    return (sev, conf, cost)


def _is_california(state: str) -> bool:
    return state.strip().lower() in ("california", "ca")


def enrich_violations(analysis, address="", location_type="", state=""):
    """Take raw Gemini analysis and enrich with KB data, produce flat report payload.

    Returns a flat dict compatible with the frontend, PDF generator, and SSE streaming.
    When state is California, includes CBC Title 24 codes. Otherwise federal ADA only.
    """
    include_california = _is_california(state)
    kb = _load_kb()
    enriched_violations = []
    total_cost = 0
    confirmed_count = 0
    potential_count = 0

    for violation in analysis.get("violations", []):
        vtype = violation["violation_type"]
        entry = kb.get(vtype, {})

        # Extract codes for flat field access (frontend/PDF compatibility)
        federal = entry.get("codes", {}).get("federal_ada") or {}
        cbc = entry.get("codes", {}).get("cbc_title24") or {}

        enriched = {
            **violation,
            "category": entry.get("category", "general"),
            "title": entry.get("title", violation.get("description", vtype)),
            # Structured codes
            "codes": entry.get("codes", {"federal_ada": None, "cbc_title24": None, "sf_local": None}),
            # Federal ADA (always included)
            "ada_section": federal.get("section", "N/A"),
            "ada_title": federal.get("title", "N/A"),
            "ada_requirement": federal.get("requirement", ""),
            # Cost fields
            "legal_risk": entry.get("legal_risk", ""),
            "estimated_cost": entry.get("estimated_cost", 0),
            "cost_low": entry.get("estimated_cost", 0),
            "cost_high": entry.get("estimated_cost", 0),
            "cost_unit": entry.get("cost_unit", ""),
            "cost_note": entry.get("cost_note", ""),
            "remediation": entry.get("remediation", {}).get("summary", ""),
            "remediation_detail": entry.get("remediation", {}),
            "cost_factors": [],
            "priority": 0,
        }

        # California CBC fields (only when in California)
        if include_california:
            cbc_req = cbc.get("requirement", "")
            fed_req = federal.get("requirement", "")
            stricter = (cbc_req != fed_req) if cbc_req else False
            enriched["cbc_section"] = cbc.get("section", "N/A")
            enriched["cbc_title"] = cbc.get("title", "N/A")
            enriched["cbc_requirement"] = cbc_req
            enriched["stricter_than_federal"] = stricter
            enriched["stricter_note"] = ""

        enriched_violations.append(enriched)
        total_cost += entry.get("estimated_cost", 0)

        confidence = violation.get("confidence", 0)
        if confidence >= CONFIRMED_THRESHOLD:
            confirmed_count += 1
        else:
            potential_count += 1

    # Sort and assign priority
    enriched_violations.sort(key=_sort_key)
    for i, v in enumerate(enriched_violations, 1):
        v["priority"] = i

    by_severity = {"high": 0, "medium": 0, "low": 0}
    for v in enriched_violations:
        sev = v.get("severity", "low")
        if sev in by_severity:
            by_severity[sev] += 1

    overall_risk = _compute_overall_risk(enriched_violations)
    headline = _generate_headline(enriched_violations)

    return {
        "violations": enriched_violations,
        "positive_features": analysis.get("positive_features", []),
        "overall_risk": overall_risk,
        "summary": analysis.get("summary", ""),
        "total_estimated_cost": {
            "low": total_cost,
            "high": total_cost,
        },
        "violation_count": len(enriched_violations),
        "confirmed_count": confirmed_count,
        "potential_count": potential_count,
        "by_severity": by_severity,
        "headline": headline,
        "standard_applied": "Federal ADA + CA CBC Title 24" if include_california else "Federal ADA",
        "state": state,
        "tax_credits": TAX_CREDITS if include_california else [c for c in TAX_CREDITS if "CA" not in c.get("name", "")],
        "next_steps": NEXT_STEPS if include_california else [s for s in NEXT_STEPS if "CASp" not in s and "SF" not in s],
        "disclaimer": DISCLAIMER if include_california else (
            "This is an AI-powered pre-screening tool. An ADA consultant should verify "
            "findings before remediation. This report does not constitute legal advice."
        ),
    }
