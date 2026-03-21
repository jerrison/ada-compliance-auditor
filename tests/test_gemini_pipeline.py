import json
import pytest
from unittest.mock import patch, MagicMock
from backend.gemini_pipeline import run_analysis_pipeline, PassResult

MOCK_SCENE_RESPONSE = '{"space_type": "entrance"}'
MOCK_VIOLATIONS_RESPONSE = json.dumps({
    "violations": [
        {
            "violation_type": "missing_ramp",
            "description": "No ramp at entrance",
            "severity": "high",
            "confidence": 0.9,
            "location_in_image": "front steps",
            "reasoning": "Three steps with no adjacent ramp",
            "needs_measurement": False,
        }
    ],
    "positive_features": ["Wide doorway"],
    "overall_risk": "high",
    "summary": "Missing ramp at entrance.",
})
MOCK_CONSISTENCY_RESPONSE = json.dumps({
    "verified_violations": [
        {
            "violation_type": "missing_ramp",
            "description": "No ramp at entrance",
            "severity": "high",
            "confidence": 0.92,
            "location_in_image": "front steps",
            "reasoning": "Three steps with no adjacent ramp",
            "needs_measurement": False,
        }
    ],
    "removed_violations": [],
    "follow_up_suggestions": ["Photograph the parking area"],
})

def _mock_call_gemini(responses):
    """Mock _call_gemini to return responses in sequence."""
    call_count = {"n": 0}
    def side_effect(*args, **kwargs):
        result = json.loads(responses[call_count["n"]])
        call_count["n"] += 1
        return result
    return side_effect

@pytest.mark.asyncio
@patch("backend.gemini_pipeline._call_gemini")
async def test_pipeline_returns_three_passes(mock_call):
    mock_call.side_effect = _mock_call_gemini([MOCK_SCENE_RESPONSE, MOCK_VIOLATIONS_RESPONSE, MOCK_CONSISTENCY_RESPONSE])
    results = []
    async for pass_result in run_analysis_pipeline(b"fake_image", "image/jpeg"):
        results.append(pass_result)
    assert len(results) == 3
    assert results[0].pass_name == "scene_classification"
    assert results[1].pass_name == "violation_detection"
    assert results[2].pass_name == "consistency_check"

@pytest.mark.asyncio
@patch("backend.gemini_pipeline._call_gemini")
async def test_pipeline_scene_classification(mock_call):
    mock_call.side_effect = _mock_call_gemini([MOCK_SCENE_RESPONSE, MOCK_VIOLATIONS_RESPONSE, MOCK_CONSISTENCY_RESPONSE])
    results = []
    async for pass_result in run_analysis_pipeline(b"fake_image", "image/jpeg"):
        results.append(pass_result)
    assert results[0].data["space_type"] == "entrance"

@pytest.mark.asyncio
@patch("backend.gemini_pipeline._call_gemini")
async def test_pipeline_final_result_has_follow_up(mock_call):
    mock_call.side_effect = _mock_call_gemini([MOCK_SCENE_RESPONSE, MOCK_VIOLATIONS_RESPONSE, MOCK_CONSISTENCY_RESPONSE])
    results = []
    async for pass_result in run_analysis_pipeline(b"fake_image", "image/jpeg"):
        results.append(pass_result)
    final = results[2].data
    assert "follow_up_suggestions" in final
    assert len(final["follow_up_suggestions"]) > 0
