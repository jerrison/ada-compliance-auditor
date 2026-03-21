"""
RocketRide pipeline client.

Connects to the RocketRide engine (localhost:5565) and sends images
through the ADA auditor pipeline for analysis.

Setup:
1. Install RocketRide VS Code extension
2. Open the RocketRide panel and start the local engine
3. Open pipeline/ada_auditor.pipe.json in the visual builder
4. This client will connect and send images through the pipeline
"""

import json
import base64
import asyncio
import logging

logger = logging.getLogger(__name__)

PIPELINE_PATH = "../pipeline/ada_auditor.pipe.json"
ENGINE_URI = "http://localhost:5565"


async def analyze_via_pipeline(image_bytes: bytes, mime_type: str) -> dict:
    """Send image through the RocketRide pipeline for ADA analysis."""
    try:
        from rocketride import RocketRideClient

        async with RocketRideClient(uri=ENGINE_URI) as client:
            result = await client.use(filepath=PIPELINE_PATH)
            token = result.get("token") or result

            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            payload = json.dumps({
                "image": image_b64,
                "mime_type": mime_type,
            })

            response = await client.send(token, payload)
            if isinstance(response, str):
                return json.loads(response)
            return response

    except ImportError:
        logger.warning("rocketride SDK not installed, falling back to direct Gemini call")
        return None
    except Exception as e:
        logger.warning(f"RocketRide engine not available ({e}), falling back to direct Gemini call")
        return None
