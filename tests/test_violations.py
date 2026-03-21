import json
from pathlib import Path


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


class TestEnrichViolations:
    def test_empty_violations_returns_report_structure(self):
        """enrich_violations with no violations returns valid report with zero cost."""
        from backend.violations import enrich_violations
        result = enrich_violations(_make_raw_analysis())
        report = result["report"]
        assert report["summary"]["total_violations"] == 0
        assert report["summary"]["total_estimated_cost"] == 0
        assert report["summary"]["overall_risk"] == "none"
        assert "tax_credits" in report
        assert "disclaimer" in report
        assert "next_steps" in report

    def test_single_violation_enriched_with_kb_data(self):
        """A known violation type gets codes, cost, remediation from KB."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([_make_violation("missing_ramp")])
        report = enrich_violations(raw)["report"]
        v = report["violations"][0]
        assert v["violation_type"] == "missing_ramp"
        assert v["codes"]["federal_ada"] is not None
        assert "section" in v["codes"]["federal_ada"]
        assert v["estimated_cost"] > 0
        assert "steps" in v["remediation"]
        assert v["category"] == "entrances"

    def test_unknown_violation_type_handled_gracefully(self):
        """Unknown violation types get default/empty enrichment, not errors."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([_make_violation("unknown_type_xyz")])
        report = enrich_violations(raw)["report"]
        v = report["violations"][0]
        assert v["violation_type"] == "unknown_type_xyz"
        assert v["estimated_cost"] == 0

    def test_priority_sorting_high_before_medium(self):
        """High severity violations get lower priority numbers than medium."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([
            _make_violation("round_door_knob", severity="medium", confidence=0.9),
            _make_violation("missing_ramp", severity="high", confidence=0.9),
        ])
        report = enrich_violations(raw)["report"]
        assert report["violations"][0]["severity"] == "high"
        assert report["violations"][0]["priority"] < report["violations"][1]["priority"]

    def test_priority_tiebreak_by_confidence(self):
        """Same severity: higher confidence gets lower priority number."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([
            _make_violation("missing_ramp", severity="high", confidence=0.7),
            _make_violation("no_accessible_entrance", severity="high", confidence=0.95),
        ])
        report = enrich_violations(raw)["report"]
        assert report["violations"][0]["confidence"] > report["violations"][1]["confidence"]

    def test_overall_risk_high_when_any_high_severity(self):
        """overall_risk is 'high' if any violation is high severity."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([
            _make_violation("round_door_knob", severity="low"),
            _make_violation("missing_ramp", severity="high"),
        ])
        report = enrich_violations(raw)["report"]
        assert report["summary"]["overall_risk"] == "high"

    def test_overall_risk_medium_when_no_high(self):
        """overall_risk is 'medium' when no high but some medium."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([
            _make_violation("round_door_knob", severity="medium"),
        ])
        report = enrich_violations(raw)["report"]
        assert report["summary"]["overall_risk"] == "medium"

    def test_overall_risk_none_when_no_violations(self):
        from backend.violations import enrich_violations
        report = enrich_violations(_make_raw_analysis())["report"]
        assert report["summary"]["overall_risk"] == "none"

    def test_total_cost_sums_all_violations(self):
        """total_estimated_cost is sum of all violation estimated_costs."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([
            _make_violation("missing_ramp"),
            _make_violation("round_door_knob"),
        ])
        report = enrich_violations(raw)["report"]
        expected = sum(v["estimated_cost"] for v in report["violations"])
        assert report["summary"]["total_estimated_cost"] == expected

    def test_headline_generated(self):
        """headline is a non-empty template-generated string."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([_make_violation("missing_ramp")])
        report = enrich_violations(raw)["report"]
        assert len(report["summary"]["headline"]) > 0
        assert "access barrier" in report["summary"]["headline"].lower()

    def test_by_severity_counts(self):
        """by_severity correctly counts violations per severity level."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([
            _make_violation("missing_ramp", severity="high"),
            _make_violation("round_door_knob", severity="medium"),
            _make_violation("missing_tactile_signage", severity="low"),
        ])
        report = enrich_violations(raw)["report"]
        assert report["summary"]["by_severity"] == {"high": 1, "medium": 1, "low": 1}

    def test_location_defaults_to_empty(self):
        """location fields default to empty strings when not provided."""
        from backend.violations import enrich_violations
        report = enrich_violations(_make_raw_analysis())["report"]
        assert report["location"]["address"] == ""
        assert report["location"]["type"] == ""

    def test_location_populated_when_provided(self):
        """location is populated when caller passes it."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis()
        report = enrich_violations(raw, address="123 Market St", location_type="commercial")["report"]
        assert report["location"]["address"] == "123 Market St"
        assert report["location"]["type"] == "commercial"
