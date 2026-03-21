"""Gemini prompts for the 3-pass ADA compliance analysis pipeline."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

SPACE_TYPES = [
    "entrance",
    "parking_lot",
    "interior",
    "restroom",
    "sidewalk_path",
    "counter_service_area",
]

VIOLATION_TYPES = [
    "missing_ramp",
    "missing_handrail",
    "narrow_doorway",
    "round_door_knob",
    "missing_accessible_parking_sign",
    "missing_parking_striping",
    "missing_curb_cut",
    "missing_tactile_signage",
    "missing_grab_bars",
    "blocked_accessible_route",
    "no_accessible_entrance",
    "step_only_entrance",
    "protruding_objects",
    "inaccessible_counter",
    "missing_directional_signage",
    "steep_ramp",
    "missing_detectable_warnings",
    "inaccessible_restroom",
]


def _load_space_violations() -> dict:
    """Load the space-to-violation mapping from backend/data/space_violations.json."""
    with open(DATA_DIR / "space_violations.json") as f:
        return json.load(f)


def _load_california_codes() -> dict:
    """Load California Building Code references from backend/data/california_codes.json."""
    with open(DATA_DIR / "california_codes.json") as f:
        return json.load(f)


def build_scene_classification_prompt() -> str:
    """Build prompt for Pass 1: classify a photo into one of the SPACE_TYPES.

    Returns:
        A prompt string that asks Gemini to classify the image and return JSON.
    """
    space_list = "\n".join(f"  - {st}" for st in SPACE_TYPES)
    return (
        "You are an ADA compliance expert. Analyze the provided photograph and "
        "classify it into exactly one of the following space types:\n\n"
        f"{space_list}\n\n"
        "Consider the primary function and physical characteristics of the space shown. "
        "Respond ONLY with valid JSON in this exact format:\n\n"
        '{"space_type": "<type>"}\n\n'
        "where <type> is one of the space types listed above."
    )


def build_violation_detection_prompt(space_type: str) -> str:
    """Build prompt for Pass 2: detect ADA violations scoped to the given space type.

    Loads space_violations.json to determine relevant violation types for the space,
    and california_codes.json to include stricter California (CBC / Title 24) thresholds.

    If the space_type is not recognized, all violation types are used.

    Args:
        space_type: One of SPACE_TYPES, or any string (unknown falls back to all).

    Returns:
        A prompt string scoped to the relevant violations for the space type.
    """
    space_violations = _load_space_violations()
    california_codes = _load_california_codes()

    # Determine which violations to check
    if space_type in space_violations:
        relevant_violations = space_violations[space_type]
    else:
        relevant_violations = VIOLATION_TYPES

    # Build violation descriptions with California code references
    violation_details = []
    for vtype in relevant_violations:
        code_info = california_codes.get(vtype, {})
        section = code_info.get("cbc_section", "N/A")
        title = code_info.get("title", vtype)
        description = code_info.get("description", "")
        requirement = code_info.get("requirement", "")
        stricter = code_info.get("stricter_than_federal", False)
        stricter_note = code_info.get("stricter_note", "")

        detail = (
            f"- {vtype} (CBC Section {section} — {title})\n"
            f"  Description: {description}\n"
            f"  Requirement: {requirement}"
        )
        if stricter and stricter_note:
            detail += f"\n  ** STRICTER THAN FEDERAL: {stricter_note}"
        violation_details.append(detail)

    violations_text = "\n\n".join(violation_details)

    return (
        "You are an ADA compliance expert specializing in the California Building Code "
        "(CBC) and Title 24 accessibility standards. Analyze the provided photograph of "
        f"a {space_type} space for the following potential violations:\n\n"
        f"{violations_text}\n\n"
        "MEASUREMENT HEURISTICS — Use these reference sizes to estimate dimensions:\n"
        "  - Standard door height: ~80 inches (6 ft 8 in)\n"
        "  - Parking space width: ~8.5 feet (102 inches)\n"
        "  - Step riser height: ~7 inches\n"
        "  - Wheelchair width: ~26 inches\n\n"
        "For each violation detected, provide:\n"
        "  - violation_type: the violation identifier\n"
        "  - severity: low, medium, or high\n"
        "  - confidence: 0.0 to 1.0\n"
        "  - description: what you observed\n"
        "  - cbc_section: the applicable California Building Code section\n"
        "  - estimated_measurement: your best estimate of the relevant dimension\n\n"
        "Respond ONLY with valid JSON in this format:\n"
        '{"violations": [...]}'
    )


def build_consistency_check_prompt(violations: list) -> str:
    """Build prompt for Pass 3: verify and refine the violations found in Pass 2.

    Takes prior violations as JSON, asks Gemini to verify each one, remove
    contradictions, adjust confidence scores, and suggest follow-up photos.

    Args:
        violations: List of violation dicts from Pass 2.

    Returns:
        A prompt string for the consistency-check pass.
    """
    violations_json = json.dumps(violations, indent=2)

    return (
        "You are an ADA compliance expert performing a consistency review. "
        "A previous analysis pass detected the following potential violations:\n\n"
        f"{violations_json}\n\n"
        "Please perform the following checks:\n"
        "1. VERIFY each violation — does it appear consistent with the image?\n"
        "2. REMOVE any contradictory or duplicate violations.\n"
        "3. ADJUST confidence scores based on image clarity and evidence strength.\n"
        "4. FLAG any violations that need additional evidence or a different angle.\n\n"
        "Respond ONLY with valid JSON in this format:\n"
        "{\n"
        '  "verified_violations": [\n'
        "    {\n"
        '      "violation_type": "...",\n'
        '      "severity": "...",\n'
        '      "confidence": 0.0,\n'
        '      "description": "...",\n'
        '      "verification_note": "..."\n'
        "    }\n"
        "  ],\n"
        '  "removed_violations": [\n'
        "    {\n"
        '      "violation_type": "...",\n'
        '      "reason": "..."\n'
        "    }\n"
        "  ],\n"
        '  "follow_up_suggestions": [\n'
        "    {\n"
        '      "description": "...",\n'
        '      "reason": "..."\n'
        "    }\n"
        "  ]\n"
        "}"
    )
