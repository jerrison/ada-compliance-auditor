import json
from pathlib import Path

from backend.violations import enrich_violations


# --- Our test helpers ---

def _make_raw_analysis(violations=None):
    """Helper to create a raw Gemini analysis dict."""
    return {
        "violations": violations or [],
        "positive_features": ["Automatic door at main entrance"],
        "overall_risk": "medium",
        "summary": "Some issues found.",
    }


def _make_violation(vtype="missing_ramp", severity="high", confidence=0.9):
    return {
        "violation_type": vtype,
        "description": "Test violation",
        "severity": severity,
        "confidence": confidence,
        "location_in_image": "center",
        "needs_measurement": False,
    }


# --- Our 13 tests (updated for flat output format) ---

class TestEnrichViolations:
    def test_empty_violations_returns_flat_structure(self):
        """enrich_violations with no violations returns valid flat dict with zero cost."""
        result = enrich_violations(_make_raw_analysis())
        assert result["violation_count"] == 0
        assert result["total_estimated_cost"]["low"] == 0
        assert result["total_estimated_cost"]["high"] == 0
        assert result["overall_risk"] == "none"
        assert "tax_credits" in result
        assert "disclaimer" in result
        assert "next_steps" in result

    def test_single_violation_enriched_with_kb_data(self):
        """A known violation type gets codes, cost, remediation from KB."""
        raw = _make_raw_analysis([_make_violation("missing_ramp")])
        result = enrich_violations(raw)
        v = result["violations"][0]
        assert v["violation_type"] == "missing_ramp"
        assert v["codes"]["federal_ada"] is not None
        assert "section" in v["codes"]["federal_ada"]
        assert v["estimated_cost"] > 0
        assert len(v["remediation"]) > 0
        assert v["category"] == "entrances"

    def test_unknown_violation_type_handled_gracefully(self):
        """Unknown violation types get default/empty enrichment, not errors."""
        raw = _make_raw_analysis([_make_violation("unknown_type_xyz")])
        result = enrich_violations(raw)
        v = result["violations"][0]
        assert v["violation_type"] == "unknown_type_xyz"
        assert v["estimated_cost"] == 0

    def test_priority_sorting_high_before_medium(self):
        """High severity violations get lower priority numbers than medium."""
        raw = _make_raw_analysis([
            _make_violation("round_door_knob", severity="medium", confidence=0.9),
            _make_violation("missing_ramp", severity="high", confidence=0.9),
        ])
        result = enrich_violations(raw)
        assert result["violations"][0]["severity"] == "high"
        assert result["violations"][0]["priority"] < result["violations"][1]["priority"]

    def test_priority_tiebreak_by_confidence(self):
        """Same severity: higher confidence gets lower priority number."""
        raw = _make_raw_analysis([
            _make_violation("missing_ramp", severity="high", confidence=0.7),
            _make_violation("no_accessible_entrance", severity="high", confidence=0.95),
        ])
        result = enrich_violations(raw)
        assert result["violations"][0]["confidence"] > result["violations"][1]["confidence"]

    def test_overall_risk_high_when_any_high_severity(self):
        """overall_risk is 'high' if any violation is high severity."""
        raw = _make_raw_analysis([
            _make_violation("round_door_knob", severity="low"),
            _make_violation("missing_ramp", severity="high"),
        ])
        result = enrich_violations(raw)
        assert result["overall_risk"] == "high"

    def test_overall_risk_medium_when_no_high(self):
        """overall_risk is 'medium' when no high but some medium."""
        raw = _make_raw_analysis([
            _make_violation("round_door_knob", severity="medium"),
        ])
        result = enrich_violations(raw)
        assert result["overall_risk"] == "medium"

    def test_overall_risk_none_when_no_violations(self):
        result = enrich_violations(_make_raw_analysis())
        assert result["overall_risk"] == "none"

    def test_total_cost_sums_all_violations(self):
        """total_estimated_cost is sum of all violation estimated_costs."""
        raw = _make_raw_analysis([
            _make_violation("missing_ramp"),
            _make_violation("round_door_knob"),
        ])
        result = enrich_violations(raw)
        expected = sum(v["estimated_cost"] for v in result["violations"])
        assert result["total_estimated_cost"]["low"] == expected
        assert result["total_estimated_cost"]["high"] == expected

    def test_headline_generated(self):
        """headline is a non-empty template-generated string."""
        raw = _make_raw_analysis([_make_violation("missing_ramp")])
        result = enrich_violations(raw)
        assert len(result["headline"]) > 0
        assert "access barrier" in result["headline"].lower()

    def test_by_severity_counts(self):
        """by_severity correctly counts violations per severity level."""
        raw = _make_raw_analysis([
            _make_violation("missing_ramp", severity="high"),
            _make_violation("round_door_knob", severity="medium"),
            _make_violation("missing_tactile_signage", severity="low"),
        ])
        result = enrich_violations(raw)
        assert result["by_severity"] == {"high": 1, "medium": 1, "low": 1}

    def test_positive_features_preserved(self):
        """positive_features from analysis are preserved in output."""
        result = enrich_violations(_make_raw_analysis())
        assert "Automatic door at main entrance" in result["positive_features"]

    def test_disclaimer_present(self):
        """disclaimer is included in enriched output."""
        result = enrich_violations(_make_raw_analysis(), state="California")
        assert "CASp" in result["disclaimer"]

    def test_disclaimer_no_casp_for_other_states(self):
        result = enrich_violations(_make_raw_analysis(), state="Oregon")
        assert "CASp" not in result["disclaimer"]


# --- Teammate's tests (updated for flat output format & KB data) ---

SAMPLE_ANALYSIS = {
    "violations": [
        {
            "violation_type": "missing_ramp",
            "description": "No ramp at entrance",
            "severity": "high",
            "confidence": 0.9,
            "location_in_image": "front steps",
            "reasoning": "Three steps visible",
            "needs_measurement": False,
        },
        {
            "violation_type": "round_door_knob",
            "description": "Round knob on front door",
            "severity": "medium",
            "confidence": 0.6,
            "location_in_image": "front door",
            "reasoning": "Round knob visible",
            "needs_measurement": False,
        },
    ],
    "positive_features": ["Wide doorway"],
    "overall_risk": "high",
    "summary": "Test summary",
}


def test_enrichment_includes_california_codes_when_in_ca():
    result = enrich_violations(SAMPLE_ANALYSIS, state="California")
    violation = result["violations"][0]
    assert "cbc_section" in violation
    assert "cbc_title" in violation


def test_enrichment_excludes_cbc_when_not_in_ca():
    result = enrich_violations(SAMPLE_ANALYSIS, state="Texas")
    violation = result["violations"][0]
    assert "cbc_section" not in violation


def test_enrichment_federal_always_included():
    result = enrich_violations(SAMPLE_ANALYSIS, state="New York")
    violation = result["violations"][0]
    assert "ada_section" in violation
    assert violation["ada_section"] != "N/A"


def test_enrichment_tracks_confirmed_vs_potential():
    result = enrich_violations(SAMPLE_ANALYSIS)
    assert result["confirmed_count"] == 1  # missing_ramp at 0.9
    assert result["potential_count"] == 1  # round_door_knob at 0.6


def test_enrichment_includes_stricter_flag_for_california():
    result = enrich_violations(SAMPLE_ANALYSIS, state="California")
    ramp = result["violations"][0]
    assert "stricter_than_federal" in ramp


def test_enrichment_cost_totals():
    result = enrich_violations(SAMPLE_ANALYSIS)
    assert result["total_estimated_cost"]["low"] > 0
    assert result["total_estimated_cost"]["high"] > 0


def test_enrichment_standard_applied_california():
    result = enrich_violations(SAMPLE_ANALYSIS, state="California")
    assert "CA" in result["standard_applied"] or "California" in result["standard_applied"]


def test_enrichment_standard_applied_federal():
    result = enrich_violations(SAMPLE_ANALYSIS, state="Oregon")
    assert result["standard_applied"] == "Federal ADA"
