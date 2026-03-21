# ADA Auditor — iOS + Web PWA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the existing ADA Compliance Auditor into a cross-platform PWA + iOS app with 3-pass Gemini analysis, California CBC Title 24 enrichment, PDF report generation, and on-device report history.

**Architecture:** Enhance the existing FastAPI monolith. Add multi-pass Gemini pipeline (`gemini_client.py`), California enrichment layer (`violations.py` + new `california_codes.json`), server-side PDF generation (`pdf_generator.py` via reportlab), and SSE progress streaming. Frontend rewritten as mobile-first PWA with camera flow, IndexedDB history, and service worker. Thin Swift WebView wrapper for iOS.

**Tech Stack:** Python 3.12+, FastAPI, Gemini 2.0 Flash (Vertex AI), reportlab, vanilla JS, Tailwind CSS (CDN), IndexedDB, Swift/WKWebView

**Spec:** `docs/superpowers/specs/2026-03-21-ada-auditor-mobile-web-design.md`

---

## File Structure

### New Files

| File | Responsibility |
|------|---------------|
| `backend/gemini_pipeline.py` | 3-pass Gemini analysis: scene classification, scoped violation detection, consistency check |
| `backend/prompts.py` | All Gemini prompts (scene classification, per-space-type violation detection, consistency check) |
| `backend/pdf_generator.py` | Server-side PDF report generation using reportlab |
| `backend/data/california_codes.json` | CBC Title 24 mappings for all 18 violation types |
| `backend/data/space_violations.json` | Maps each space type to its relevant subset of violation types |
| `frontend/app.js` | Complete rewrite: camera flow, SSE progress, IndexedDB history, PDF download |
| `frontend/index.html` | Rewrite: mobile-first layout with bottom nav (Scan / History) |
| `frontend/sw.js` | Service worker for PWA offline history |
| `frontend/manifest.json` | Web app manifest for Add to Home Screen |
| `frontend/db.js` | IndexedDB wrapper for report storage |
| `ios/ADAauditor/ADAauditorApp.swift` | SwiftUI app entry point |
| `ios/ADAauditor/WebView.swift` | WKWebView + navigation delegate |
| `ios/ADAauditor/ShareHandler.swift` | PDF save + native share sheet bridge |
| `ios/ADAauditor/Info.plist` | Camera permission description |
| `tests/test_prompts.py` | Tests for prompt construction |
| `tests/test_gemini_pipeline.py` | Tests for 3-pass pipeline logic (mocked Gemini) |
| `tests/test_violations.py` | Tests for California enrichment |
| `tests/test_pdf_generator.py` | Tests for PDF output |

### Modified Files

| File | Change |
|------|--------|
| `backend/gemini_client.py` | Keep `analyze_image_direct` as low-level helper called by `gemini_pipeline.py`. Remove `ANALYSIS_PROMPT` (moved to `prompts.py`) |
| `backend/violations.py` | Add California enrichment: load `california_codes.json`, return both ADA + CBC references, track confirmed vs potential |
| `backend/main.py` | Replace `/api/analyze` with SSE endpoint using 3-pass pipeline. Add `/api/reports/<id>/pdf` for PDF download. Remove RocketRide import. |
| `backend/pipeline_client.py` | Delete: RocketRide replaced by 3-pass Gemini pipeline |
| `frontend/style.css` | Add mobile nav styles, camera overlay, history card styles |
| `pyproject.toml` | Add `reportlab` dependency, add `pytest` dev dependency |

---

## Task 1: Add California Building Codes Data

**Files:**
- Create: `backend/data/california_codes.json`
- Create: `backend/data/space_violations.json`

- [ ] **Step 1: Create `california_codes.json`**

This file maps each of the 18 violation types to CBC Title 24 equivalents:

```json
{
  "missing_ramp": {
    "cbc_section": "11B-405.2",
    "title": "Ramps — California",
    "description": "CBC requires running slope no steeper than 1:12 for new construction. Existing buildings: maximum 1:10 for rises up to 3 inches, 1:8 for rises up to 6 inches where space is limited.",
    "requirement": "Ramp width minimum 48 inches (vs federal 36 inches). Landings minimum 60x60 inches.",
    "stricter_than_federal": true,
    "stricter_note": "California requires 48-inch minimum width vs federal 36-inch"
  },
  "missing_handrail": {
    "cbc_section": "11B-405.8",
    "title": "Handrails — California",
    "description": "Handrails required on both sides of ramps with rise greater than 6 inches.",
    "requirement": "Height 34-38 inches. Extensions 12 inches minimum at top and bottom. Must return to wall, guard, or landing surface.",
    "stricter_than_federal": false,
    "stricter_note": ""
  },
  "narrow_doorway": {
    "cbc_section": "11B-404.2.3",
    "title": "Door Clear Width — California",
    "description": "Minimum 32-inch clear opening measured with door open 90 degrees.",
    "requirement": "When approach is not straight, 36-inch minimum may apply per CBC path-of-travel requirements.",
    "stricter_than_federal": true,
    "stricter_note": "CBC path-of-travel triggers may require 36-inch clear width in some configurations"
  },
  "round_door_knob": {
    "cbc_section": "11B-404.2.7",
    "title": "Door Hardware — California",
    "description": "Hardware must be operable with one hand, without tight grasping, pinching, or twisting.",
    "requirement": "Lever handles, push/pull, or U-shaped handles required. Round knobs prohibited on accessible routes.",
    "stricter_than_federal": false,
    "stricter_note": ""
  },
  "missing_accessible_parking_sign": {
    "cbc_section": "11B-502.6",
    "title": "Accessible Parking Signage — California",
    "description": "California requires specific sign dimensions, fine amount displayed ($250 minimum), and tow-away warning.",
    "requirement": "Sign bottom minimum 80 inches above ground (vs federal 60 inches). Must display ISA, fine amount, and CVC 22511.56 reference.",
    "stricter_than_federal": true,
    "stricter_note": "California requires 80-inch sign height (vs 60-inch federal) and must display fine amount"
  },
  "missing_parking_striping": {
    "cbc_section": "11B-502.3",
    "title": "Accessible Parking Striping — California",
    "description": "California requires blue-painted striping for accessible spaces and cross-hatching for access aisles.",
    "requirement": "Access aisle minimum 60 inches. Van spaces require 96-inch aisle. Blue border and ISA painted on pavement required.",
    "stricter_than_federal": true,
    "stricter_note": "California requires specific blue paint color and pavement ISA marking"
  },
  "missing_curb_cut": {
    "cbc_section": "11B-406",
    "title": "Curb Ramps — California",
    "description": "Curb ramps required wherever accessible route crosses a curb.",
    "requirement": "Maximum slope 1:12. Must have detectable warning surface. Flared sides maximum slope 1:10.",
    "stricter_than_federal": false,
    "stricter_note": ""
  },
  "missing_tactile_signage": {
    "cbc_section": "11B-703.2",
    "title": "Tactile Signage — California",
    "description": "California adds specific contrast requirements and geometric tactile symbols.",
    "requirement": "Raised characters 1/32 inch minimum. Grade 2 Braille. Geometric symbols required for specific room types (triangle for men, circle for women).",
    "stricter_than_federal": true,
    "stricter_note": "California requires geometric tactile symbols for restroom identification"
  },
  "missing_grab_bars": {
    "cbc_section": "11B-604.5",
    "title": "Grab Bars — California",
    "description": "Grab bars required on side and rear walls closest to toilet.",
    "requirement": "Side bar: 42 inches minimum. Rear bar: 36 inches minimum. Mounted 33-36 inches above floor.",
    "stricter_than_federal": false,
    "stricter_note": ""
  },
  "blocked_accessible_route": {
    "cbc_section": "11B-402",
    "title": "Accessible Routes — California",
    "description": "California path-of-travel requirements: when alterations exceed a threshold, the path of travel to the altered area must also be made accessible.",
    "requirement": "Path-of-travel spending requirement: up to 20% of the overall alteration cost must be spent on accessibility. Minimum 48-inch width preferred.",
    "stricter_than_federal": true,
    "stricter_note": "CBC 20% path-of-travel spending trigger on alterations"
  },
  "no_accessible_entrance": {
    "cbc_section": "11B-206.4",
    "title": "Accessible Entrances — California",
    "description": "At least 60% of public entrances must be accessible. California requires CASp inspection for compliance certification.",
    "requirement": "Accessible entrances on accessible route. ISA signage if not all entrances are accessible. CASp inspection recommended.",
    "stricter_than_federal": false,
    "stricter_note": ""
  },
  "step_only_entrance": {
    "cbc_section": "11B-404.2.5",
    "title": "Thresholds — California",
    "description": "Thresholds maximum 1/2 inch (3/4 inch for sliding doors). California adds requirements for existing buildings during alterations.",
    "requirement": "When alterations trigger path-of-travel requirements, step-only entrances must be addressed as part of the 20% spending obligation.",
    "stricter_than_federal": true,
    "stricter_note": "Path-of-travel trigger may require ramp/lift installation during building alterations"
  },
  "protruding_objects": {
    "cbc_section": "11B-307",
    "title": "Protruding Objects — California",
    "description": "Objects must not protrude more than 4 inches into circulation paths between 27-80 inches above floor.",
    "requirement": "Same as federal standard. Cane-detectable barrier required below protruding objects.",
    "stricter_than_federal": false,
    "stricter_note": ""
  },
  "inaccessible_counter": {
    "cbc_section": "11B-904.4",
    "title": "Service Counters — California",
    "description": "Accessible counter section required: 36 inches max height, 36 inches min length.",
    "requirement": "Counter must be on accessible route. California requires knee and toe clearance for forward approach.",
    "stricter_than_federal": true,
    "stricter_note": "California explicitly requires knee/toe clearance at counters"
  },
  "missing_directional_signage": {
    "cbc_section": "11B-703.5",
    "title": "Directional Signage — California",
    "description": "Directional signs with ISA required at decision points along accessible routes.",
    "requirement": "Must include ISA symbol. California adds contrast and character proportion requirements.",
    "stricter_than_federal": false,
    "stricter_note": ""
  },
  "steep_ramp": {
    "cbc_section": "11B-405.2",
    "title": "Ramp Slope — California",
    "description": "Maximum running slope 1:12 for new construction. Existing buildings may use 1:10 for short rises.",
    "requirement": "Cross slope maximum 1:48. Maximum rise 30 inches per run. Landings at top and bottom.",
    "stricter_than_federal": false,
    "stricter_note": ""
  },
  "missing_detectable_warnings": {
    "cbc_section": "11B-705",
    "title": "Detectable Warnings — California",
    "description": "Truncated domes required at curb ramps, transit platforms, and hazardous vehicular areas.",
    "requirement": "Yellow color required in California (vs federal which allows any contrasting color). 36 inches deep in direction of travel.",
    "stricter_than_federal": true,
    "stricter_note": "California requires yellow detectable warnings specifically"
  },
  "inaccessible_restroom": {
    "cbc_section": "11B-603",
    "title": "Toilet Rooms — California",
    "description": "At least one of each toilet type must be accessible. California adds geometric symbol requirement on doors.",
    "requirement": "60-inch turning space. Accessible fixtures. California requires triangle (men) and circle (women) geometric symbols on restroom doors.",
    "stricter_than_federal": true,
    "stricter_note": "California requires geometric symbols (triangle/circle) on restroom doors"
  }
}
```

- [ ] **Step 2: Create `space_violations.json`**

Maps each space type to its relevant violation subset for scoped analysis:

```json
{
  "entrance": [
    "missing_ramp", "missing_handrail", "narrow_doorway", "round_door_knob",
    "missing_tactile_signage", "no_accessible_entrance", "step_only_entrance",
    "protruding_objects", "blocked_accessible_route", "steep_ramp",
    "missing_directional_signage"
  ],
  "parking_lot": [
    "missing_accessible_parking_sign", "missing_parking_striping",
    "missing_curb_cut", "missing_detectable_warnings", "blocked_accessible_route",
    "missing_directional_signage"
  ],
  "interior": [
    "narrow_doorway", "round_door_knob", "blocked_accessible_route",
    "protruding_objects", "inaccessible_counter", "missing_tactile_signage",
    "missing_directional_signage"
  ],
  "restroom": [
    "missing_grab_bars", "inaccessible_restroom", "narrow_doorway",
    "round_door_knob", "missing_tactile_signage", "blocked_accessible_route"
  ],
  "sidewalk_path": [
    "missing_curb_cut", "missing_detectable_warnings", "blocked_accessible_route",
    "protruding_objects", "steep_ramp", "missing_ramp", "missing_handrail",
    "missing_directional_signage"
  ],
  "counter_service_area": [
    "inaccessible_counter", "narrow_doorway", "blocked_accessible_route",
    "missing_directional_signage", "protruding_objects"
  ]
}
```

- [ ] **Step 3: Commit**

```bash
git add backend/data/california_codes.json backend/data/space_violations.json
git commit -m "feat: add California CBC Title 24 codes and space-violation mappings"
```

---

## Task 2: Build Multi-Pass Gemini Prompts

**Files:**
- Create: `backend/prompts.py`
- Create: `tests/test_prompts.py`

- [ ] **Step 1: Write failing tests for prompt construction**

```python
# tests/test_prompts.py
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


def test_violation_detection_prompt_includes_california():
    prompt = build_violation_detection_prompt("entrance")
    assert "California Building Code" in prompt or "CBC" in prompt
    assert "Title 24" in prompt


def test_consistency_check_prompt_includes_violations_json():
    sample_violations = [{"violation_type": "missing_ramp", "severity": "high"}]
    prompt = build_consistency_check_prompt(sample_violations)
    assert "missing_ramp" in prompt
    assert "follow_up_suggestions" in prompt


def test_unknown_space_type_uses_all_violations():
    prompt = build_violation_detection_prompt("unknown_type")
    for vtype in VIOLATION_TYPES:
        assert vtype in prompt
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/malikharouna/Hackathon1/ada-compliance-auditor && uv run pytest tests/test_prompts.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'backend.prompts'`

- [ ] **Step 3: Implement `backend/prompts.py`**

```python
"""Gemini prompts for the 3-pass ADA compliance analysis pipeline."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

SPACE_TYPES = [
    "entrance", "parking_lot", "interior",
    "restroom", "sidewalk_path", "counter_service_area",
]

VIOLATION_TYPES = [
    "missing_ramp", "missing_handrail", "narrow_doorway", "round_door_knob",
    "missing_accessible_parking_sign", "missing_parking_striping",
    "missing_curb_cut", "missing_tactile_signage", "missing_grab_bars",
    "blocked_accessible_route", "no_accessible_entrance", "step_only_entrance",
    "protruding_objects", "inaccessible_counter", "missing_directional_signage",
    "steep_ramp", "missing_detectable_warnings", "inaccessible_restroom",
]


def _load_space_violations() -> dict:
    with open(DATA_DIR / "space_violations.json") as f:
        return json.load(f)


def _load_california_codes() -> dict:
    with open(DATA_DIR / "california_codes.json") as f:
        return json.load(f)


def build_scene_classification_prompt() -> str:
    types_list = ", ".join(SPACE_TYPES)
    return f"""You are an expert ADA accessibility auditor. Classify this photo into one of these space types:

{types_list}

Look at the primary subject of the image and determine what kind of physical space it shows.

Return ONLY a JSON object:
{{"space_type": "<one of: {types_list}>"}}"""


def build_violation_detection_prompt(space_type: str) -> str:
    space_violations = _load_space_violations()
    california_codes = _load_california_codes()

    relevant_types = space_violations.get(space_type, VIOLATION_TYPES)
    types_str = ", ".join(relevant_types)

    ca_thresholds = []
    for vtype in relevant_types:
        ca = california_codes.get(vtype, {})
        if ca.get("stricter_than_federal"):
            ca_thresholds.append(
                f"- {vtype}: {ca.get('stricter_note', '')} (CBC {ca.get('cbc_section', '')})"
            )

    ca_section = ""
    if ca_thresholds:
        ca_section = (
            "\n\nCALIFORNIA-SPECIFIC THRESHOLDS (CBC Title 24):\n"
            "This property is in California. Apply these stricter standards where they differ from federal ADA:\n"
            + "\n".join(ca_thresholds)
            + "\n"
        )

    return f"""You are an expert ADA compliance auditor analyzing a {space_type} photo.

Check ONLY for these violation types relevant to this space:
{types_str}

MEASUREMENT HEURISTICS:
- A standard single door is approximately 80 inches tall - use as vertical scale reference
- A standard parking space is approximately 8.5 feet wide
- A standard step riser is approximately 7 inches
- A wheelchair is approximately 26 inches wide
{ca_section}
For each violation you identify:
1. Only report issues you can VISUALLY CONFIRM in the image
2. Be specific about what you observe and where in the image
3. Provide explicit reasoning for each finding
4. Note items that would need physical measurement to verify

Return a JSON object:
{{
  "violations": [
    {{
      "violation_type": "<one of: {types_str}>",
      "description": "<what you observe>",
      "severity": "<high, medium, or low>",
      "confidence": <0.0 to 1.0>,
      "location_in_image": "<where in the image>",
      "reasoning": "<why this is a violation>",
      "needs_measurement": <true or false>
    }}
  ],
  "positive_features": ["<accessible features that ARE present>"],
  "overall_risk": "<high, medium, or low>",
  "summary": "<2-3 sentence summary>"
}}

Severity guide:
- high: Prevents access entirely (confidence >= 0.7)
- medium: Creates difficulty or safety risk (confidence >= 0.5)
- low: Minor non-compliance or cosmetic

Return ONLY the JSON object."""


def build_consistency_check_prompt(violations: list) -> str:
    violations_json = json.dumps(violations, indent=2)
    return f"""You are an expert ADA compliance auditor performing a quality check.

Review the image again along with these previously identified violations:

{violations_json}

Your tasks:
1. VERIFY each violation against what you see in the image. Remove any that are contradicted by visual evidence.
2. ADJUST confidence scores if your review changes your certainty.
3. CHECK for contradictions (e.g., a violation says "no ramp" but a ramp is visible).
4. SUGGEST follow-up photos that would help complete the audit.

Return a JSON object:
{{
  "violations": [<same structure as input, with adjustments>],
  "removed": [
    {{
      "violation_type": "<type>",
      "reason": "<why it was removed>"
    }}
  ],
  "follow_up_suggestions": [
    "<specific instruction, e.g., 'Photograph the parking area to check for accessible spaces'>"
  ]
}}

Return ONLY the JSON object."""
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/malikharouna/Hackathon1/ada-compliance-auditor && uv run pytest tests/test_prompts.py -v`
Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/prompts.py tests/test_prompts.py
git commit -m "feat: add 3-pass Gemini prompts with California CBC thresholds"
```

---

## Task 3: Build 3-Pass Gemini Pipeline

**Files:**
- Create: `backend/gemini_pipeline.py`
- Create: `tests/test_gemini_pipeline.py`
- Modify: `backend/gemini_client.py`

- [ ] **Step 1: Write failing tests for the pipeline**

```python
# tests/test_gemini_pipeline.py
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
    "violations": [
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
    "removed": [],
    "follow_up_suggestions": ["Photograph the parking area"],
})


def _mock_gemini_call(responses):
    """Return a mock that yields responses in order."""
    call_count = {"n": 0}

    def side_effect(*args, **kwargs):
        resp = MagicMock()
        resp.text = responses[call_count["n"]]
        call_count["n"] += 1
        return resp

    return side_effect


@pytest.mark.asyncio
@patch("backend.gemini_pipeline.GenerativeModel")
async def test_pipeline_returns_three_passes(mock_model_cls):
    mock_model = MagicMock()
    mock_model.generate_content = _mock_gemini_call([
        MOCK_SCENE_RESPONSE,
        MOCK_VIOLATIONS_RESPONSE,
        MOCK_CONSISTENCY_RESPONSE,
    ])
    mock_model_cls.return_value = mock_model

    results = []
    async for pass_result in run_analysis_pipeline(b"fake_image", "image/jpeg"):
        results.append(pass_result)

    assert len(results) == 3
    assert results[0].pass_name == "scene_classification"
    assert results[1].pass_name == "violation_detection"
    assert results[2].pass_name == "consistency_check"


@pytest.mark.asyncio
@patch("backend.gemini_pipeline.GenerativeModel")
async def test_pipeline_scene_classification(mock_model_cls):
    mock_model = MagicMock()
    mock_model.generate_content = _mock_gemini_call([
        MOCK_SCENE_RESPONSE,
        MOCK_VIOLATIONS_RESPONSE,
        MOCK_CONSISTENCY_RESPONSE,
    ])
    mock_model_cls.return_value = mock_model

    results = []
    async for pass_result in run_analysis_pipeline(b"fake_image", "image/jpeg"):
        results.append(pass_result)

    assert results[0].data["space_type"] == "entrance"


@pytest.mark.asyncio
@patch("backend.gemini_pipeline.GenerativeModel")
async def test_pipeline_final_result_has_follow_up(mock_model_cls):
    mock_model = MagicMock()
    mock_model.generate_content = _mock_gemini_call([
        MOCK_SCENE_RESPONSE,
        MOCK_VIOLATIONS_RESPONSE,
        MOCK_CONSISTENCY_RESPONSE,
    ])
    mock_model_cls.return_value = mock_model

    results = []
    async for pass_result in run_analysis_pipeline(b"fake_image", "image/jpeg"):
        results.append(pass_result)

    final = results[2].data
    assert "follow_up_suggestions" in final
    assert len(final["follow_up_suggestions"]) > 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/malikharouna/Hackathon1/ada-compliance-auditor && uv run pytest tests/test_gemini_pipeline.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'backend.gemini_pipeline'`

- [ ] **Step 3: Implement `backend/gemini_pipeline.py`**

```python
"""3-pass Gemini analysis pipeline for ADA compliance."""

import json
import logging
from dataclasses import dataclass
from typing import AsyncGenerator

from vertexai.generative_models import GenerativeModel, Part, GenerationConfig

from prompts import (
    build_scene_classification_prompt,
    build_violation_detection_prompt,
    build_consistency_check_prompt,
)

logger = logging.getLogger(__name__)


@dataclass
class PassResult:
    pass_name: str
    data: dict


def _call_gemini(model: GenerativeModel, image_part: Part, prompt: str) -> dict:
    response = model.generate_content(
        [image_part, prompt],
        generation_config=GenerationConfig(
            temperature=0.2,
            max_output_tokens=4096,
            response_mime_type="application/json",
        ),
    )
    return json.loads(response.text)


async def run_analysis_pipeline(
    image_bytes: bytes, mime_type: str
) -> AsyncGenerator[PassResult, None]:
    """Run the 3-pass Gemini analysis pipeline, yielding results per pass."""
    model = GenerativeModel("gemini-2.0-flash")
    image_part = Part.from_data(data=image_bytes, mime_type=mime_type)

    # Pass 1: Scene Classification
    logger.info("Pass 1: Scene classification")
    scene_prompt = build_scene_classification_prompt()
    scene_result = _call_gemini(model, image_part, scene_prompt)
    space_type = scene_result.get("space_type", "entrance")
    yield PassResult(pass_name="scene_classification", data=scene_result)

    # Pass 2: Violation Detection (scoped to space type)
    logger.info("Pass 2: Violation detection for %s", space_type)
    detection_prompt = build_violation_detection_prompt(space_type)
    detection_result = _call_gemini(model, image_part, detection_prompt)
    yield PassResult(pass_name="violation_detection", data=detection_result)

    # Pass 3: Consistency Check
    logger.info("Pass 3: Consistency check")
    violations = detection_result.get("violations", [])
    consistency_prompt = build_consistency_check_prompt(violations)
    consistency_result = _call_gemini(model, image_part, consistency_prompt)
    yield PassResult(pass_name="consistency_check", data=consistency_result)
```

- [ ] **Step 4: Update `backend/gemini_client.py`**

Keep the direct call function as a low-level utility but move the prompt to `prompts.py`:

```python
"""Low-level Gemini API helper. Used by gemini_pipeline.py."""

import json
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig


def call_gemini_direct(image_bytes: bytes, mime_type: str, prompt: str) -> dict:
    """Direct Gemini API call with a given prompt."""
    model = GenerativeModel("gemini-2.0-flash")
    image_part = Part.from_data(data=image_bytes, mime_type=mime_type)

    response = model.generate_content(
        [image_part, prompt],
        generation_config=GenerationConfig(
            temperature=0.2,
            max_output_tokens=4096,
            response_mime_type="application/json",
        ),
    )

    return json.loads(response.text)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd /Users/malikharouna/Hackathon1/ada-compliance-auditor && uv run pytest tests/test_gemini_pipeline.py -v`
Expected: All 3 tests PASS

- [ ] **Step 6: Commit**

```bash
git add backend/gemini_pipeline.py backend/gemini_client.py tests/test_gemini_pipeline.py
git commit -m "feat: implement 3-pass Gemini analysis pipeline"
```

---

## Task 4: Update Violations Enrichment with California Codes

**Files:**
- Modify: `backend/violations.py`
- Create: `tests/test_violations.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_violations.py
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
    # confidence >= 0.7 is confirmed, < 0.7 is potential
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/malikharouna/Hackathon1/ada-compliance-auditor && uv run pytest tests/test_violations.py -v`
Expected: FAIL on `cbc_section`, `confirmed_count`, `stricter_than_federal` fields

- [ ] **Step 3: Update `backend/violations.py`**

```python
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

CONFIRMED_THRESHOLD = 0.7


def _load_json(filename: str) -> dict:
    with open(DATA_DIR / filename) as f:
        return json.load(f)


def enrich_violations(analysis: dict) -> dict:
    """Enrich raw Gemini analysis with ADA codes, California CBC codes, and costs."""
    ada_codes = _load_json("ada_codes.json")
    cost_estimates = _load_json("cost_estimates.json")
    california_codes = _load_json("california_codes.json")

    enriched_violations = []
    total_cost_low = 0
    total_cost_high = 0
    confirmed_count = 0
    potential_count = 0

    for violation in analysis.get("violations", []):
        vtype = violation["violation_type"]
        confidence = violation.get("confidence", 0)

        code_info = ada_codes.get(vtype, {})
        cost_info = cost_estimates.get(vtype, {})
        ca_info = california_codes.get(vtype, {})

        if confidence >= CONFIRMED_THRESHOLD:
            confirmed_count += 1
        else:
            potential_count += 1

        enriched = {
            **violation,
            # Federal ADA
            "ada_section": code_info.get("ada_section", "N/A"),
            "ada_title": code_info.get("title", "N/A"),
            "ada_requirement": code_info.get("requirement", ""),
            # California CBC
            "cbc_section": ca_info.get("cbc_section", "N/A"),
            "cbc_title": ca_info.get("title", "N/A"),
            "cbc_requirement": ca_info.get("requirement", ""),
            "stricter_than_federal": ca_info.get("stricter_than_federal", False),
            "stricter_note": ca_info.get("stricter_note", ""),
            # Cost
            "cost_low": cost_info.get("low", 0),
            "cost_high": cost_info.get("high", 0),
            "cost_unit": cost_info.get("unit", ""),
            "remediation": cost_info.get("description", ""),
            "cost_factors": cost_info.get("factors", []),
        }
        enriched_violations.append(enriched)

        total_cost_low += cost_info.get("low", 0)
        total_cost_high += cost_info.get("high", 0)

    return {
        "violations": enriched_violations,
        "positive_features": analysis.get("positive_features", []),
        "overall_risk": analysis.get("overall_risk", "unknown"),
        "summary": analysis.get("summary", ""),
        "total_estimated_cost": {
            "low": total_cost_low,
            "high": total_cost_high,
        },
        "violation_count": len(enriched_violations),
        "confirmed_count": confirmed_count,
        "potential_count": potential_count,
        "disclaimer": "This AI-generated report is not a substitute for a certified CASp (Certified Access Specialist) inspection. Evaluated against California Building Code Title 24 and federal ADA standards. Small businesses may qualify for up to $5,000 in tax credits for accessibility improvements (IRS Form 8826).",
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/malikharouna/Hackathon1/ada-compliance-auditor && uv run pytest tests/test_violations.py -v`
Expected: All 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/violations.py tests/test_violations.py
git commit -m "feat: add California CBC Title 24 enrichment to violations"
```

---

## Task 5: Build PDF Report Generator

**Files:**
- Create: `backend/pdf_generator.py`
- Create: `tests/test_pdf_generator.py`
- Modify: `pyproject.toml`

- [ ] **Step 1: Add reportlab dependency**

```bash
cd /Users/malikharouna/Hackathon1/ada-compliance-auditor && uv add reportlab
```

- [ ] **Step 2: Write failing tests**

```python
# tests/test_pdf_generator.py
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
        report=SAMPLE_REPORT,
        location_label="123 Main St, Oakland",
        space_type="entrance",
        image_bytes=None,
    )
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0


def test_pdf_starts_with_pdf_header():
    pdf_bytes = generate_pdf_report(
        report=SAMPLE_REPORT,
        location_label="Test Location",
        space_type="entrance",
        image_bytes=None,
    )
    assert pdf_bytes[:5] == b"%PDF-"
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd /Users/malikharouna/Hackathon1/ada-compliance-auditor && uv run pytest tests/test_pdf_generator.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'backend.pdf_generator'`

- [ ] **Step 4: Implement `backend/pdf_generator.py`**

```python
"""PDF report generator for ADA compliance audits using reportlab."""

import io
from datetime import datetime, timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image as RLImage,
)


SEVERITY_COLORS = {
    "high": colors.HexColor("#DC2626"),
    "medium": colors.HexColor("#F59E0B"),
    "low": colors.HexColor("#3B82F6"),
}


def generate_pdf_report(
    report: dict,
    location_label: str,
    space_type: str,
    image_bytes: bytes | None = None,
) -> bytes:
    """Generate a styled PDF audit report. Returns PDF as bytes."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "ReportTitle", parent=styles["Title"], fontSize=24,
        spaceAfter=6, textColor=colors.HexColor("#1E293B"),
    ))
    styles.add(ParagraphStyle(
        "SectionHeader", parent=styles["Heading2"], fontSize=14,
        spaceAfter=8, textColor=colors.HexColor("#1E293B"),
        borderWidth=0, borderPadding=0,
    ))
    styles.add(ParagraphStyle(
        "ViolationTitle", parent=styles["Heading3"], fontSize=12,
        spaceAfter=4, textColor=colors.HexColor("#1E293B"),
    ))
    styles.add(ParagraphStyle(
        "BodyGray", parent=styles["Normal"], fontSize=10,
        textColor=colors.HexColor("#475569"),
    ))
    styles.add(ParagraphStyle(
        "Disclaimer", parent=styles["Normal"], fontSize=8,
        textColor=colors.HexColor("#94A3B8"), spaceAfter=4,
    ))

    story = []
    now = datetime.now(timezone.utc).strftime("%B %d, %Y")
    risk = (report.get("overall_risk") or "unknown").upper()

    # --- Cover Page ---
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("ADA Compliance Audit Report", styles["ReportTitle"]))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("<b>Location:</b> " + location_label, styles["Normal"]))
    story.append(Paragraph("<b>Date:</b> " + now, styles["Normal"]))
    story.append(Paragraph("<b>Space Type:</b> " + space_type.replace("_", " ").title(), styles["Normal"]))
    story.append(Paragraph("<b>Overall Risk:</b> " + risk, styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    if image_bytes:
        try:
            img_buf = io.BytesIO(image_bytes)
            img = RLImage(img_buf, width=4 * inch, height=3 * inch, kind="proportional")
            story.append(img)
        except Exception:
            pass  # Skip image if it cannot be rendered

    story.append(PageBreak())

    # --- Executive Summary ---
    story.append(Paragraph("Executive Summary", styles["SectionHeader"]))
    story.append(Paragraph(report.get("summary", ""), styles["Normal"]))
    story.append(Spacer(1, 0.2 * inch))

    confirmed = report.get("confirmed_count", 0)
    potential = report.get("potential_count", 0)
    cost_low = report.get("total_estimated_cost", {}).get("low", 0)
    cost_high = report.get("total_estimated_cost", {}).get("high", 0)

    summary_data = [
        ["Metric", "Value"],
        ["Total Violations", str(report.get("violation_count", 0))],
        ["Confirmed (high confidence)", str(confirmed)],
        ["Potential (needs verification)", str(potential)],
        ["Estimated Remediation Cost", "${:,} - ${:,}".format(cost_low, cost_high)],
        ["Standard", "California Building Code Title 24 + Federal ADA"],
    ]
    summary_table = Table(summary_data, colWidths=[2.5 * inch, 4 * inch])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.3 * inch))

    # Positive features
    positives = report.get("positive_features", [])
    if positives:
        story.append(Paragraph("Compliant Features Detected", styles["SectionHeader"]))
        for feat in positives:
            story.append(Paragraph("&#8226; " + feat, styles["BodyGray"]))
        story.append(Spacer(1, 0.3 * inch))

    # --- Violation Details ---
    violations = report.get("violations", [])
    if violations:
        story.append(PageBreak())
        story.append(Paragraph("Violation Details", styles["SectionHeader"]))

        for v in violations:
            sev = v.get("severity", "low")
            sev_color = SEVERITY_COLORS.get(sev, colors.gray)
            conf = v.get("confidence", 0)
            conf_label = "Confirmed" if conf >= 0.7 else "Potential"

            vtype_display = v["violation_type"].replace("_", " ").title()
            story.append(Paragraph(
                '{} - <font color="{}">{}</font> ({}, {:.0%})'.format(
                    vtype_display, sev_color.hexval(), sev.upper(), conf_label, conf
                ),
                styles["ViolationTitle"],
            ))
            story.append(Paragraph(v.get("description", ""), styles["Normal"]))

            if v.get("reasoning"):
                story.append(Paragraph("<i>Reasoning: {}</i>".format(v["reasoning"]), styles["BodyGray"]))

            story.append(Paragraph(
                "<b>Location in image:</b> {}".format(v.get("location_in_image", "N/A")),
                styles["BodyGray"],
            ))

            # Code references table
            code_data = [
                ["Standard", "Section", "Requirement"],
                ["Federal ADA", v.get("ada_section", "N/A"), v.get("ada_requirement", "")],
                ["CA CBC Title 24", v.get("cbc_section", "N/A"), v.get("cbc_requirement", "")],
            ]
            code_table = Table(code_data, colWidths=[1.3 * inch, 1.2 * inch, 4 * inch])
            code_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#334155")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(Spacer(1, 0.1 * inch))
            story.append(code_table)

            if v.get("stricter_than_federal"):
                story.append(Paragraph(
                    '<font color="#DC2626"><b>California is stricter:</b> {}</font>'.format(
                        v.get("stricter_note", "")
                    ),
                    styles["BodyGray"],
                ))

            story.append(Paragraph(
                "<b>Est. Remediation:</b> ${:,} - ${:,} {}".format(
                    v.get("cost_low", 0), v.get("cost_high", 0), v.get("cost_unit", "")
                ),
                styles["Normal"],
            ))
            story.append(Paragraph(v.get("remediation", ""), styles["BodyGray"]))
            story.append(Spacer(1, 0.3 * inch))

    # --- Cost Matrix ---
    if violations:
        story.append(PageBreak())
        story.append(Paragraph("Remediation Cost Summary", styles["SectionHeader"]))

        cost_data = [["Violation", "Severity", "Low Est.", "High Est."]]
        for v in violations:
            vtype_display = v["violation_type"].replace("_", " ").title()
            cost_data.append([
                vtype_display,
                v.get("severity", "").upper(),
                "${:,}".format(v.get("cost_low", 0)),
                "${:,}".format(v.get("cost_high", 0)),
            ])
        cost_data.append(["TOTAL", "", "${:,}".format(cost_low), "${:,}".format(cost_high)])

        cost_table = Table(cost_data, colWidths=[2.8 * inch, 1.2 * inch, 1.2 * inch, 1.3 * inch])
        cost_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#F1F5F9")),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ]))
        story.append(cost_table)

    # --- Disclaimer ---
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(report.get("disclaimer", ""), styles["Disclaimer"]))

    doc.build(story)
    return buf.getvalue()
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd /Users/malikharouna/Hackathon1/ada-compliance-auditor && uv run pytest tests/test_pdf_generator.py -v`
Expected: All 2 tests PASS

- [ ] **Step 6: Commit**

```bash
git add backend/pdf_generator.py tests/test_pdf_generator.py pyproject.toml uv.lock
git commit -m "feat: add PDF report generator with reportlab"
```

---

## Task 6: Update Backend API with SSE Streaming

**Files:**
- Modify: `backend/main.py`
- Delete: `backend/pipeline_client.py`

- [ ] **Step 1: Rewrite `backend/main.py`**

```python
import os
import json
import uuid
import logging

from dotenv import load_dotenv

load_dotenv()

import vertexai
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse, Response

from gemini_pipeline import run_analysis_pipeline
from violations import enrich_violations
from pdf_generator import generate_pdf_report

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
)

app = FastAPI(title="ADA Compliance Auditor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

# Temporary PDF storage (in-memory for hackathon)
_pdf_store: dict[str, bytes] = {}


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...), location_label: str = Form("")):
    """Analyze image via 3-pass Gemini pipeline with SSE progress streaming."""
    contents = await file.read()
    mime_type = file.content_type or "image/jpeg"

    async def event_stream():
        space_type = "unknown"

        async for pass_result in run_analysis_pipeline(contents, mime_type):
            if pass_result.pass_name == "scene_classification":
                space_type = pass_result.data.get("space_type", "unknown")
                yield "data: {}\n\n".format(json.dumps({
                    "pass": "scene_classification",
                    "space_type": space_type,
                }))

            elif pass_result.pass_name == "violation_detection":
                count = len(pass_result.data.get("violations", []))
                yield "data: {}\n\n".format(json.dumps({
                    "pass": "violation_detection",
                    "violation_count": count,
                }))

            elif pass_result.pass_name == "consistency_check":
                # Merge consistency results with detection data
                merged = {
                    "violations": pass_result.data.get("violations", []),
                    "positive_features": pass_result.data.get("positive_features", []),
                    "overall_risk": pass_result.data.get("overall_risk", "unknown"),
                    "summary": pass_result.data.get("summary", ""),
                }

                # Enrich with ADA + California codes + costs
                enriched = enrich_violations(merged)
                enriched["follow_up_suggestions"] = pass_result.data.get(
                    "follow_up_suggestions", []
                )
                enriched["space_type"] = space_type

                # Generate PDF
                pdf_bytes = generate_pdf_report(
                    report=enriched,
                    location_label=location_label or "Unknown Location",
                    space_type=space_type,
                    image_bytes=contents,
                )
                pdf_id = str(uuid.uuid4())
                _pdf_store[pdf_id] = pdf_bytes

                enriched["pdf_url"] = "/api/reports/{}/pdf".format(pdf_id)

                yield "data: {}\n\n".format(json.dumps({
                    "pass": "complete",
                    "report": enriched,
                }))

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/api/reports/{pdf_id}/pdf")
async def download_pdf(pdf_id: str):
    """Download a generated PDF report."""
    pdf_bytes = _pdf_store.get(pdf_id)
    if not pdf_bytes:
        return Response(status_code=404, content="Report not found")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=ada-audit-{}.pdf".format(pdf_id[:8])
        },
    )


@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
```

- [ ] **Step 2: Delete `backend/pipeline_client.py`**

```bash
rm /Users/malikharouna/Hackathon1/ada-compliance-auditor/backend/pipeline_client.py
```

- [ ] **Step 3: Commit**

```bash
git add backend/main.py
git rm backend/pipeline_client.py
git commit -m "feat: replace RocketRide with SSE streaming 3-pass pipeline + PDF endpoint"
```

---

## Task 7: Rewrite Frontend as Mobile-First PWA

**Files:**
- Modify: `frontend/index.html`
- Create: `frontend/db.js`
- Rewrite: `frontend/app.js`
- Modify: `frontend/style.css`
- Create: `frontend/manifest.json`
- Create: `frontend/sw.js`

- [ ] **Step 1: Create `frontend/manifest.json`**

```json
{
  "name": "ADA Compliance Auditor",
  "short_name": "ADA Auditor",
  "description": "AI-powered ADA accessibility auditor for California buildings",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#030712",
  "theme_color": "#2563EB",
  "orientation": "portrait",
  "icons": [
    {
      "src": "/static/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

- [ ] **Step 2: Create `frontend/sw.js`**

```javascript
const CACHE_NAME = 'ada-auditor-v1';
const STATIC_ASSETS = [
  '/',
  '/static/app.js',
  '/static/db.js',
  '/static/style.css',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (url.pathname.startsWith('/api/')) return;
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});
```

- [ ] **Step 3: Create `frontend/db.js`**

```javascript
/** IndexedDB wrapper for report storage. */
const DB_NAME = 'ada-auditor';
const DB_VERSION = 1;
const STORE_NAME = 'reports';

function openDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        const store = db.createObjectStore(STORE_NAME, { keyPath: 'id' });
        store.createIndex('date', 'date', { unique: false });
        store.createIndex('riskLevel', 'riskLevel', { unique: false });
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function saveReport(report) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    tx.objectStore(STORE_NAME).put(report);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

async function getReport(id) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readonly');
    const req = tx.objectStore(STORE_NAME).get(id);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function getAllReports() {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readonly');
    const req = tx.objectStore(STORE_NAME).index('date').openCursor(null, 'prev');
    const results = [];
    req.onsuccess = (e) => {
      const cursor = e.target.result;
      if (cursor) {
        results.push(cursor.value);
        cursor.continue();
      } else {
        resolve(results);
      }
    };
    req.onerror = () => reject(req.error);
  });
}

async function deleteReport(id) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    tx.objectStore(STORE_NAME).delete(id);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}
```

- [ ] **Step 4: Rewrite `frontend/index.html`**

Complete mobile-first layout with bottom nav (Scan / History), camera upload area, SSE progress steps, results with confirmed/potential split, PDF download button, follow-up suggestions, and history screen with filter buttons. See spec Section 4 for full UI structure.

Key structure:
- `#scan-screen`: camera upload, location input, analyze button, progress steps, results
- `#history-screen`: filter buttons (All/High/Medium/Low), report card list
- Bottom nav: Scan and History tabs
- PWA meta tags and manifest link

- [ ] **Step 5: Rewrite `frontend/app.js`**

Complete rewrite handling:
- Navigation between Scan and History screens
- File upload via click (with `capture="environment"` for mobile camera) and drag-drop
- SSE streaming from `/api/analyze` with progress step animation
- Results rendering with confirmed/potential violation split
- PDF download via dynamically created anchor tag
- IndexedDB report saving with compressed thumbnail
- History screen loading, filtering by risk level, and viewing saved reports
- Service worker registration
- Session ID generation via `crypto.randomUUID()` stored in localStorage

All DOM construction uses safe methods (`textContent` for plain text, `createElement` for structure). Violation card rendering uses DOM APIs rather than string interpolation for user-facing content.

- [ ] **Step 6: Update `frontend/style.css`**

Add styles for:
- `.screen` / `.screen.active` show/hide
- `.nav-btn` / `.nav-btn.active` bottom navigation
- `.filter-btn` / `.filter-btn.active` history filter pills
- `.step-indicator` progress animation

- [ ] **Step 7: Commit**

```bash
git add frontend/
git commit -m "feat: rewrite frontend as mobile-first PWA with camera flow and history"
```

---

## Task 8: Add pytest Configuration

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`
- Modify: `pyproject.toml`

- [ ] **Step 1: Create test infrastructure**

Create empty `tests/__init__.py`.

Create `tests/conftest.py`:
```python
import sys
from pathlib import Path

# Add backend to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
```

Add to `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[project.optional-dependencies]
dev = ["pytest", "pytest-asyncio"]
```

- [ ] **Step 2: Install dev dependencies and run all tests**

```bash
cd /Users/malikharouna/Hackathon1/ada-compliance-auditor && uv add --dev pytest pytest-asyncio && uv run pytest tests/ -v
```

Expected: All tests pass

- [ ] **Step 3: Commit**

```bash
git add tests/__init__.py tests/conftest.py pyproject.toml uv.lock
git commit -m "chore: add pytest configuration and test infrastructure"
```

---

## Task 9: iOS Swift WebView Wrapper

**Files:**
- Create: `ios/ADAauditor/ADAauditorApp.swift`
- Create: `ios/ADAauditor/WebView.swift`
- Create: `ios/ADAauditor/ShareHandler.swift`
- Create: `ios/ADAauditor/Info.plist`

- [ ] **Step 1: Create `ios/ADAauditor/ADAauditorApp.swift`**

```swift
import SwiftUI

@main
struct ADAauditorApp: App {
    var body: some Scene {
        WindowGroup {
            WebView(url: URL(string: "http://localhost:8000")!)
                .ignoresSafeArea()
        }
    }
}
```

- [ ] **Step 2: Create `ios/ADAauditor/WebView.swift`**

WKWebView wrapped in UIViewRepresentable. Coordinator as WKNavigationDelegate intercepts PDF download links (`.pdf` extension) and routes them to ShareHandler. Camera access works natively through WKWebView's `getUserMedia` support.

- [ ] **Step 3: Create `ios/ADAauditor/ShareHandler.swift`**

Downloads PDF via URLSession, saves to both temp directory and app Documents directory, presents UIActivityViewController for sharing via AirDrop, email, Messages, or Files.

- [ ] **Step 4: Create `ios/ADAauditor/Info.plist`**

Camera and photo library usage descriptions for iOS permissions.

- [ ] **Step 5: Commit**

```bash
git add ios/
git commit -m "feat: add iOS Swift WebView wrapper with PDF share sheet"
```

---

## Task 10: Integration Test

- [ ] **Step 1: Run all tests**

```bash
cd /Users/malikharouna/Hackathon1/ada-compliance-auditor && uv run pytest tests/ -v
```

Expected: All tests pass

- [ ] **Step 2: Manual verification**

Start server and verify:
1. Bottom nav shows Scan and History tabs
2. Upload area opens file picker with camera option on mobile
3. SSE progress steps animate during analysis
4. Report shows confirmed/potential split with CBC references
5. PDF download produces valid report
6. History tab shows saved reports
7. Filter buttons work

```bash
cd /Users/malikharouna/Hackathon1/ada-compliance-auditor/backend && uv run uvicorn main:app --reload --port 8000
```

- [ ] **Step 3: Final commit**

```bash
git add -A
git commit -m "chore: final integration verification"
```

---

## Execution Order

```
Task 1 (data files) --> Task 2 (prompts) --> Task 3 (pipeline)
                                                    |
Task 4 (violations) <-- Task 1 ----------> Task 5 (PDF gen)
                                                    |
Task 8 (pytest) <------------------------ Task 6 (backend API) <-- Task 3 + 4 + 5
                                                    |
                                            Task 7 (frontend) <-- Task 6
                                                    |
                                            Task 9 (iOS wrapper)
                                                    |
                                            Task 10 (integration)
```

**Parallel opportunities:**
- Task 1 runs first (no deps)
- Tasks 2 + 4 + 8 can run in parallel after Task 1
- Task 5 can run in parallel with Tasks 2-4
- Task 9 can run anytime (no backend deps)
