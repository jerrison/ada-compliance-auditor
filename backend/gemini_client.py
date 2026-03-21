"""Low-level Gemini API helper. Used by gemini_pipeline.py."""
import json
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig

def call_gemini_direct(image_bytes: bytes, mime_type: str, prompt: str) -> dict:
    model = GenerativeModel("gemini-2.0-flash")
    image_part = Part.from_data(data=image_bytes, mime_type=mime_type)
    response = model.generate_content(
        [image_part, prompt],
        generation_config=GenerationConfig(
            temperature=0.2, max_output_tokens=4096,
            response_mime_type="application/json",
        ),
    )
    return json.loads(response.text)
