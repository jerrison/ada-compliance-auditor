from backend.violations import enrich_violations

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


def test_enrichment_includes_california_codes():
    result = enrich_violations(SAMPLE_ANALYSIS)
    violation = result["violations"][0]
    assert "cbc_section" in violation
    assert "cbc_title" in violation


def test_enrichment_includes_federal_and_california():
    result = enrich_violations(SAMPLE_ANALYSIS)
    violation = result["violations"][0]
    assert "ada_section" in violation
    assert "cbc_section" in violation


def test_enrichment_tracks_confirmed_vs_potential():
    result = enrich_violations(SAMPLE_ANALYSIS)
    assert "confirmed_count" in result
    assert "potential_count" in result
    assert result["confirmed_count"] == 1  # missing_ramp at 0.9
    assert result["potential_count"] == 1  # round_door_knob at 0.6


def test_enrichment_includes_stricter_note():
    result = enrich_violations(SAMPLE_ANALYSIS)
    ramp = result["violations"][0]
    assert ramp.get("stricter_than_federal") is True
    assert "stricter_note" in ramp


def test_enrichment_cost_totals():
    result = enrich_violations(SAMPLE_ANALYSIS)
    assert result["total_estimated_cost"]["low"] > 0
    assert result["total_estimated_cost"]["high"] > 0
