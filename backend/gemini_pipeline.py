"""3-pass Gemini analysis pipeline for ADA compliance."""
import json
import os
import logging
from dataclasses import dataclass
from typing import AsyncGenerator

from google import genai
from google.genai.types import GenerateContentConfig, Part

from prompts import (
    build_scene_classification_prompt,
    build_violation_detection_prompt,
    build_consistency_check_prompt,
)

logger = logging.getLogger(__name__)

MODEL = "gemini-2.5-flash"

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client


@dataclass
class PassResult:
    pass_name: str
    data: dict


def _call_gemini(image_bytes: bytes, mime_type: str, prompt: str) -> dict:
    client = _get_client()
    image_part = Part.from_bytes(data=image_bytes, mime_type=mime_type)
    response = client.models.generate_content(
        model=MODEL,
        contents=[image_part, prompt],
        config=GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=8192,
            response_mime_type="application/json",
        ),
    )
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        logger.warning("JSON parse failed, retrying with higher token limit")
        response = client.models.generate_content(
            model=MODEL,
            contents=[image_part, prompt],
            config=GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=16384,
                response_mime_type="application/json",
            ),
        )
        return json.loads(response.text)


async def run_analysis_pipeline(image_bytes: bytes, mime_type: str, state: str = "") -> AsyncGenerator[PassResult, None]:
    # Pass 1: Scene Classification
    logger.info("Pass 1: Scene classification")
    scene_result = _call_gemini(image_bytes, mime_type, build_scene_classification_prompt())
    space_type = scene_result.get("space_type", "entrance")
    yield PassResult(pass_name="scene_classification", data=scene_result)

    # Pass 2: Violation Detection (scoped)
    logger.info("Pass 2: Violation detection for %s", space_type)
    detection_result = _call_gemini(image_bytes, mime_type, build_violation_detection_prompt(space_type, state=state))
    yield PassResult(pass_name="violation_detection", data=detection_result)

    # Pass 3: Consistency Check
    logger.info("Pass 3: Consistency check")
    violations = detection_result.get("violations", [])
    consistency_result = _call_gemini(image_bytes, mime_type, build_consistency_check_prompt(violations))
    yield PassResult(pass_name="consistency_check", data=consistency_result)
