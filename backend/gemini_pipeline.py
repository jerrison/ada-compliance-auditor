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
            temperature=0.2, max_output_tokens=4096,
            response_mime_type="application/json",
        ),
    )
    return json.loads(response.text)

async def run_analysis_pipeline(image_bytes: bytes, mime_type: str, state: str = "") -> AsyncGenerator[PassResult, None]:
    model = GenerativeModel("gemini-2.0-flash")
    image_part = Part.from_data(data=image_bytes, mime_type=mime_type)

    # Pass 1: Scene Classification
    logger.info("Pass 1: Scene classification")
    scene_result = _call_gemini(model, image_part, build_scene_classification_prompt())
    space_type = scene_result.get("space_type", "entrance")
    yield PassResult(pass_name="scene_classification", data=scene_result)

    # Pass 2: Violation Detection (scoped)
    logger.info("Pass 2: Violation detection for %s", space_type)
    detection_result = _call_gemini(model, image_part, build_violation_detection_prompt(space_type, state=state))
    yield PassResult(pass_name="violation_detection", data=detection_result)

    # Pass 3: Consistency Check
    logger.info("Pass 3: Consistency check")
    violations = detection_result.get("violations", [])
    consistency_result = _call_gemini(model, image_part, build_consistency_check_prompt(violations))
    yield PassResult(pass_name="consistency_check", data=consistency_result)
