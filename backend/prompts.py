"""Gemini prompts for the 3-pass ADA compliance analysis pipeline.

Loads violation types and California CBC code references from the knowledge base
(ada_knowledge_base.json) instead of separate data files.
"""

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

_kb = None


def _load_kb():
    global _kb
    if _kb is None:
        with open(DATA_DIR / "ada_knowledge_base.json") as f:
            _kb = json.load(f)
    return _kb


# Build VIOLATION_TYPES from KB keys (loaded lazily, but the list is set at import time)
def _get_violation_types():
    kb = _load_kb()
    return sorted(kb.keys())


VIOLATION_TYPES = _get_violation_types()


def _load_space_violations() -> dict:
    """Load the space-to-violation mapping from backend/data/space_violations.json."""
    with open(DATA_DIR / "space_violations.json") as f:
        return json.load(f)


def _load_california_codes() -> dict:
    """Extract California Building Code references from the knowledge base.

    Returns a dict keyed by violation type with CBC data in the same format
    that the old california_codes.json had.
    """
    kb = _load_kb()
    codes = {}
    for vtype, entry in kb.items():
        cbc = entry.get("codes", {}).get("cbc_title24")
        if cbc:
            codes[vtype] = {
                "cbc_section": cbc.get("section", "N/A"),
                "title": cbc.get("title", vtype),
                "description": entry.get("description", ""),
                "requirement": cbc.get("requirement", ""),
                "stricter_than_federal": (
                    cbc.get("requirement", "") !=
                    (entry.get("codes", {}).get("federal_ada", {}) or {}).get("requirement", "")
                ) if cbc.get("requirement") else False,
                "stricter_note": "",
            }
        else:
            codes[vtype] = {
                "cbc_section": "N/A",
                "title": entry.get("title", vtype),
                "description": entry.get("description", ""),
                "requirement": "",
                "stricter_than_federal": False,
                "stricter_note": None,
            }
    return codes


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


def _is_california(state: str) -> bool:
    return state.strip().lower() in ("california", "ca")


def build_violation_detection_prompt(space_type: str, state: str = "") -> str:
    """Build prompt for Pass 2: detect ADA violations scoped to the given space type.

    Loads space_violations.json to determine relevant violation types.
    If state is California, includes CBC Title 24 data from knowledge base.

    Args:
        space_type: One of SPACE_TYPES, or any string (unknown falls back to all).
        state: US state name. California triggers CBC codes.

    Returns:
        A prompt string scoped to the relevant violations for the space type.
    """
    space_violations = _load_space_violations()
    include_california = _is_california(state)

    if space_type in space_violations:
        relevant_violations = space_violations[space_type]
    else:
        relevant_violations = VIOLATION_TYPES

    violation_details = []
    if include_california:
        california_codes = _load_california_codes()
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
    else:
        kb = _load_kb()
        for vtype in relevant_violations:
            entry = kb.get(vtype, {})
            federal = entry.get("codes", {}).get("federal_ada") or {}
            detail = f"- {vtype}"
            if federal.get("section"):
                detail += f" (ADA Section {federal['section']})"
            if entry.get("description"):
                detail += f"\n  {entry['description']}"
            violation_details.append(detail)

    violations_text = "\n\n".join(violation_details)

    if include_california:
        intro = (
            "You are an ADA compliance expert specializing in the California Building Code "
            "(CBC) and Title 24 accessibility standards. This property is in California. "
            f"Analyze the provided photograph of a {space_type} space for the following "
            "potential violations:"
        )
        code_field = "  - cbc_section: the applicable California Building Code section\n"
    else:
        state_note = f" This property is in {state}." if state else ""
        intro = (
            f"You are an ADA (Americans with Disabilities Act) compliance expert.{state_note} "
            f"Analyze the provided photograph of a {space_type} space for the following "
            "potential violations:"
        )
        code_field = ""

    return (
        f"{intro}\n\n"
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
        f"{code_field}"
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
