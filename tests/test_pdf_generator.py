from backend.pdf_generator import generate_pdf_report

SAMPLE_REPORT = {
    "violations": [
        {
            "violation_type": "missing_ramp",
            "description": "No ramp at entrance",
            "severity": "high",
            "confidence": 0.9,
            "location_in_image": "front steps",
            "reasoning": "Three steps with no ramp",
            "needs_measurement": False,
            "ada_section": "405",
            "ada_title": "Ramps",
            "ada_requirement": "Ramp required where level change > 1/2 inch",
            "cbc_section": "11B-405.2",
            "cbc_title": "Ramps - California",
            "cbc_requirement": "48-inch minimum width",
            "stricter_than_federal": True,
            "stricter_note": "California requires 48-inch minimum width",
            "cost_low": 5000,
            "cost_high": 20000,
            "cost_unit": "per ramp",
            "remediation": "Install wheelchair ramp",
            "cost_factors": ["Height", "Material"],
        }
    ],
    "positive_features": ["Wide doorway"],
    "overall_risk": "high",
    "summary": "Missing ramp at main entrance creates a barrier to access.",
    "total_estimated_cost": {"low": 5000, "high": 20000},
    "violation_count": 1,
    "confirmed_count": 1,
    "potential_count": 0,
    "disclaimer": "This is an AI-generated report.",
}

def test_generate_pdf_returns_bytes():
    pdf_bytes = generate_pdf_report(
        report=SAMPLE_REPORT, location_label="123 Main St, Oakland",
        space_type="entrance", image_bytes=None,
    )
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0

def test_pdf_starts_with_pdf_header():
    pdf_bytes = generate_pdf_report(
        report=SAMPLE_REPORT, location_label="Test Location",
        space_type="entrance", image_bytes=None,
    )
    assert pdf_bytes[:5] == b"%PDF-"
