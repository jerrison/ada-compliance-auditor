import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

_kb = None


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
    return f"{count} {top_sev} access barrier(s) found — {cat_str} require attention"


def _sort_key(violation):
    sev = SEVERITY_ORDER.get(violation.get("severity", "low"), 2)
    conf = -(violation.get("confidence", 0))
    cost = violation.get("estimated_cost", 0)
    return (sev, conf, cost)


def enrich_violations(analysis, address="", location_type=""):
    """Take raw Gemini analysis and enrich with KB data, produce report payload."""
    kb = _load_kb()
    enriched_violations = []
    total_cost = 0

    for violation in analysis.get("violations", []):
        vtype = violation["violation_type"]
        entry = kb.get(vtype, {})

        enriched = {
            **violation,
            "category": entry.get("category", "general"),
            "title": entry.get("title", violation.get("description", vtype)),
            "codes": entry.get("codes", {"federal_ada": None, "cbc_title24": None, "sf_local": None}),
            "legal_risk": entry.get("legal_risk", ""),
            "estimated_cost": entry.get("estimated_cost", 0),
            "cost_unit": entry.get("cost_unit", ""),
            "remediation": entry.get("remediation", {"summary": "", "steps": []}),
        }
        enriched_violations.append(enriched)
        total_cost += entry.get("estimated_cost", 0)

    # Sort AFTER enrichment — _sort_key reads estimated_cost which is set during enrichment above
    enriched_violations.sort(key=_sort_key)
    for i, v in enumerate(enriched_violations, 1):
        v["priority"] = i

    by_severity = {"high": 0, "medium": 0, "low": 0}
    for v in enriched_violations:
        sev = v.get("severity", "low")
        if sev in by_severity:
            by_severity[sev] += 1

    return {
        "report": {
            "id": str(uuid.uuid4()),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "location": {
                "address": address,
                "type": location_type,
            },
            "summary": {
                "total_violations": len(enriched_violations),
                "by_severity": by_severity,
                "total_estimated_cost": total_cost,
                "overall_risk": _compute_overall_risk(enriched_violations),
                "headline": _generate_headline(enriched_violations),
            },
            "violations": enriched_violations,
            "tax_credits": TAX_CREDITS,
            "next_steps": NEXT_STEPS,
            "disclaimer": DISCLAIMER,
        }
    }
