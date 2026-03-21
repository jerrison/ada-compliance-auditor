"""
Gemini Vision analysis for ADA compliance.

This module provides two execution paths:
1. Via RocketRide pipeline (primary) - called through the pipeline engine
2. Direct Gemini API (fallback) - for testing without RocketRide running

The RocketRide pipeline in pipeline/ada_auditor.pipe.json wires:
  Source (webhook) → Image → LLM (Gemini) → Output

This module contains the prompt and direct-call fallback.
"""

import json
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig


ANALYSIS_PROMPT = """You are an expert ADA (Americans with Disabilities Act) compliance auditor analyzing a photo of a building, facility, or public space.

Analyze this image for potential ADA accessibility violations. For each violation you identify:

1. Only report issues you can VISUALLY CONFIRM in the image
2. Be specific about what you observe
3. Note items that would need physical measurement to fully verify

Return your analysis as a JSON object with this exact structure:
{
  "violations": [
    {
      "violation_type": "<one of: missing_ramp, missing_handrail, narrow_doorway, round_door_knob, missing_accessible_parking_sign, missing_parking_striping, missing_curb_cut, missing_tactile_signage, missing_grab_bars, blocked_accessible_route, no_accessible_entrance, step_only_entrance, protruding_objects, inaccessible_counter, missing_directional_signage, steep_ramp, missing_detectable_warnings, inaccessible_restroom>",
      "description": "<what you observe in the image>",
      "severity": "<high, medium, or low>",
      "confidence": <0.0 to 1.0>,
      "location_in_image": "<where in the image this issue appears>",
      "needs_measurement": <true or false>
    }
  ],
  "positive_features": ["<list any accessibility features that ARE present and compliant>"],
  "overall_risk": "<high, medium, or low>",
  "summary": "<2-3 sentence summary of findings>"
}

Severity guide:
- high: Prevents access entirely (e.g., step-only entrance, no ramp)
- medium: Creates difficulty or safety risk (e.g., missing handrails, round knobs)
- low: Minor non-compliance or cosmetic (e.g., faded striping, missing signage)

IMPORTANT: Return ONLY the JSON object, no markdown formatting or extra text."""


def analyze_image_direct(image_bytes: bytes, mime_type: str) -> dict:
    """Direct Gemini API call (fallback when RocketRide engine is not running)."""
    model = GenerativeModel("gemini-2.0-flash")
    image_part = Part.from_data(data=image_bytes, mime_type=mime_type)

    response = model.generate_content(
        [image_part, ANALYSIS_PROMPT],
        generation_config=GenerationConfig(
            temperature=0.2,
            max_output_tokens=4096,
            response_mime_type="application/json",
        ),
    )

    return json.loads(response.text)
