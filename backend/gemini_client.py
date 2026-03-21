"""
Gemini Vision analysis for ADA compliance.

This module provides two execution paths:
1. Via RocketRide pipeline (primary) - called through the pipeline engine
2. Direct Gemini API (fallback) - for testing without RocketRide running

The prompt is dynamically built from the knowledge base at import time,
so it stays in sync with the violation types defined in ada_knowledge_base.json.
"""

import json
from pathlib import Path
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig

DATA_DIR = Path(__file__).parent / "data"


def _load_kb():
    with open(DATA_DIR / "ada_knowledge_base.json") as f:
        return json.load(f)


def build_prompt():
    """Build the analysis prompt dynamically from the knowledge base."""
    kb = _load_kb()

    # Group violations by category
    categories = {}
    for vtype, entry in kb.items():
        cat = entry.get("category", "general")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((vtype, entry))

    # Build violation reference section
    violation_ref = []
    for cat, entries in sorted(categories.items()):
        cat_title = cat.replace("_", " ").title()
        violation_ref.append(f"\n### {cat_title}")
        for vtype, entry in entries:
            cues = entry.get("detection", {}).get("visual_cues", [])
            cues_str = "; ".join(cues) if cues else "Visual inspection required"
            violation_ref.append(f"- `{vtype}`: {entry.get('title', vtype)} — Look for: {cues_str}")

    violation_section = "\n".join(violation_ref)
    all_types = ", ".join(sorted(kb.keys()))

    return f"""You are an expert ADA (Americans with Disabilities Act) compliance auditor specializing in California and San Francisco requirements. You are analyzing a photo of a building, facility, or public space.

Analyze this image for potential ADA accessibility violations. For each violation you identify:

1. Only report issues you can VISUALLY CONFIRM in the image
2. Be specific about what you observe
3. Note items that would need physical measurement to fully verify
4. Consider both federal ADA and California Building Code (CBC Title 24) requirements

## Violation Types Reference
{violation_section}

## Output Format

Return your analysis as a JSON object with this exact structure:
{{
  "violations": [
    {{
      "violation_type": "<one of: {all_types}>",
      "description": "<what you observe in the image>",
      "severity": "<high, medium, or low>",
      "confidence": <0.0 to 1.0>,
      "location_in_image": "<where in the image this issue appears>",
      "needs_measurement": <true or false>
    }}
  ],
  "positive_features": ["<list any accessibility features that ARE present and compliant>"],
  "summary": "<2-3 sentence summary of findings>"
}}

## Severity Guide
- high: Prevents access entirely (e.g., step-only entrance, no ramp, no accessible restroom)
- medium: Creates difficulty or safety risk (e.g., missing handrails, round knobs, steep ramp)
- low: Minor non-compliance or cosmetic (e.g., faded striping, missing signage, sign mounting height)

IMPORTANT: Return ONLY the JSON object, no markdown formatting or extra text."""


# Build prompt once at module load time
ANALYSIS_PROMPT = build_prompt()


def analyze_image_direct(image_bytes: bytes, mime_type: str) -> dict:
    """Direct Gemini API call (fallback when RocketRide engine is not running)."""
    model = GenerativeModel("gemini-2.0-flash")
    image_part = Part.from_data(data=image_bytes, mime_type=mime_type)

    response = model.generate_content(
        [image_part, ANALYSIS_PROMPT],
        generation_config=GenerationConfig(
            temperature=0.2,
            max_output_tokens=8192,
            response_mime_type="application/json",
        ),
    )

    return json.loads(response.text)
