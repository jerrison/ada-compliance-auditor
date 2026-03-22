from backend.prompts import (
    build_scene_classification_prompt,
    build_violation_detection_prompt,
    build_consistency_check_prompt,
    SPACE_TYPES,
    VIOLATION_TYPES,
)


def test_scene_classification_prompt_contains_all_space_types():
    prompt = build_scene_classification_prompt()
    for space_type in SPACE_TYPES:
        assert space_type in prompt


def test_violation_detection_prompt_scoped_to_entrance():
    prompt = build_violation_detection_prompt("entrance")
    assert "missing_ramp" in prompt
    assert "missing_grab_bars" not in prompt  # restroom-only


def test_violation_detection_prompt_scoped_to_restroom():
    prompt = build_violation_detection_prompt("restroom")
    assert "missing_grab_bars" in prompt
    assert "missing_accessible_parking_sign" not in prompt  # parking-only


def test_violation_detection_prompt_includes_california_when_in_ca():
    prompt = build_violation_detection_prompt("entrance", state="California")
    assert "California Building Code" in prompt or "CBC" in prompt
    assert "Title 24" in prompt


def test_violation_detection_prompt_no_cbc_when_other_state():
    prompt = build_violation_detection_prompt("entrance", state="Texas")
    assert "California Building Code" not in prompt
    assert "CBC Section" not in prompt


def test_violation_detection_prompt_federal_always():
    prompt = build_violation_detection_prompt("entrance", state="New York")
    assert "ADA" in prompt


def test_consistency_check_prompt_includes_violations_json():
    sample_violations = [{"violation_type": "missing_ramp", "severity": "high"}]
    prompt = build_consistency_check_prompt(sample_violations)
    assert "missing_ramp" in prompt
    assert "follow_up_suggestions" in prompt


def test_unknown_space_type_uses_all_violations():
    prompt = build_violation_detection_prompt("unknown_type")
    for vtype in VIOLATION_TYPES:
        assert vtype in prompt
