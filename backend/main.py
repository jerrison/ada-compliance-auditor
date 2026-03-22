"""ADA Compliance Auditor — FastAPI backend.

Primary execution path: RocketRide pipeline (when ROCKETRIDE_URI is set).
Fallback: Direct Gemini API calls via gemini_pipeline.py.
"""
import os
import json
import uuid
import logging

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse, Response

from gemini_pipeline import run_analysis_pipeline
from violations import enrich_violations
from pdf_generator import generate_pdf_report

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Configuration ────────────────────────────────────────────────
ROCKETRIDE_URI = os.getenv("ROCKETRIDE_URI", "")
ROCKETRIDE_APIKEY = os.getenv("ROCKETRIDE_APIKEY", "")
PIPELINE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "pipeline", "ada_auditor.pipe",
)
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

USE_ROCKETRIDE = bool(ROCKETRIDE_URI)

app = FastAPI(title="ADA Compliance Auditor")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory PDF store (hackathon)
_pdf_store: dict[str, bytes] = {}


# ── RocketRide Pipeline Execution ────────────────────────────────
async def _extract_state_via_rocketride(address: str) -> str:
    """Send address through RocketRide pipeline to extract US state.

    Uses the Chat → Prompt → Return Questions pipeline to process
    the address and extract the jurisdiction state code.
    """
    from rocketride import RocketRideClient

    logger.info("Processing address via RocketRide pipeline at %s", ROCKETRIDE_URI)

    with open(PIPELINE_PATH) as f:
        pipeline_config = json.load(f)

    async with RocketRideClient(uri=ROCKETRIDE_URI, auth=ROCKETRIDE_APIKEY) as client:
        result = await client.use(pipeline=pipeline_config)
        token = result["token"]

        response = await client.send(token, address)
        await client.terminate(token)

        # Extract state from the prompt-enhanced response
        if isinstance(response, dict):
            questions = response.get("questions", [])
            if questions:
                # The prompt wraps the address with jurisdiction context
                text = questions[0].get("text", "") if isinstance(questions[0], dict) else str(questions[0])
                logger.info("RocketRide processed address: %s", text[:100])
                # Try to extract 2-letter state code
                import re
                match = re.search(r'\b([A-Z]{2})\b', text)
                if match:
                    return match.group(1)

        return ""


async def _run_via_direct_gemini(image_bytes: bytes, mime_type: str, state: str):
    """Execute the 3-pass analysis via direct Gemini API calls (fallback)."""
    logger.info("Executing via direct Gemini API (fallback)")

    results = {}
    async for pass_result in run_analysis_pipeline(image_bytes, mime_type, state=state):
        results[pass_result.pass_name] = pass_result.data

    consistency = results.get("consistency_check", {})
    verified = (
        consistency.get("verified_violations")
        or consistency.get("violations")
        or []
    )

    raw = {
        "violations": verified,
        "positive_features": consistency.get("positive_features", []),
        "overall_risk": consistency.get("overall_risk", "unknown"),
        "summary": consistency.get("summary", ""),
        "space_type": results.get("scene_classification", {}).get("space_type", "unknown"),
        "follow_up_suggestions": consistency.get("follow_up_suggestions", []),
        "_pipeline_mode": "direct_gemini",
    }
    return raw


# ── API Endpoints ────────────────────────────────────────────────

@app.get("/api/config")
async def get_config():
    """Return client-safe configuration values."""
    return {
        "google_maps_api_key": os.getenv("GOOGLE_MAPS_API_KEY", ""),
        "pipeline_mode": "rocketride" if USE_ROCKETRIDE else "direct_gemini",
    }


@app.get("/api/pipeline/status")
async def pipeline_status():
    """Check pipeline execution mode and RocketRide availability."""
    rr_status = {"connected": False, "error": None}
    if USE_ROCKETRIDE:
        try:
            from rocketride import RocketRideClient
            async with RocketRideClient(uri=ROCKETRIDE_URI, auth=ROCKETRIDE_APIKEY) as client:
                rr_status["connected"] = client.is_connected()
                info = client.get_connection_info()
                rr_status["transport"] = info.get("transport", "unknown")
        except Exception as e:
            rr_status["error"] = str(e)

    return {
        "mode": "rocketride" if USE_ROCKETRIDE else "direct_gemini",
        "rocketride_uri": ROCKETRIDE_URI or None,
        "rocketride_available": USE_ROCKETRIDE,
        "rocketride_status": rr_status,
        "pipeline_file": PIPELINE_PATH,
        "model": "gemini-2.5-flash",
    }


@app.post("/api/analyze")
async def analyze(
    file: UploadFile = File(...),
    location_label: str = Form(""),
    state: str = Form(""),
):
    """Analyze image for ADA compliance violations.

    Routes through RocketRide pipeline when available, falls back to
    direct Gemini API calls otherwise. Streams progress via SSE.
    """
    contents = await file.read()
    mime_type = file.content_type or "image/jpeg"

    # ── Extract state via RocketRide if address provided and engine available ──
    rr_state = state
    if USE_ROCKETRIDE and location_label and not state:
        try:
            rr_state = await _extract_state_via_rocketride(location_label)
            if rr_state:
                logger.info("RocketRide extracted state: %s from address: %s", rr_state, location_label)
                state = rr_state
        except Exception as e:
            logger.warning("RocketRide address processing failed (%s), continuing without state", e)

    async def event_stream():
        # ── Run Gemini analysis pipeline ──
        raw = None
        space_type = "unknown"
        async for pass_result in run_analysis_pipeline(contents, mime_type, state=state):
            if pass_result.pass_name == "scene_classification":
                space_type = pass_result.data.get("space_type", "unknown")
                yield "data: {}\n\n".format(json.dumps({
                    "pass": "scene_classification",
                    "space_type": space_type,
                    "pipeline_mode": "rocketride+gemini" if rr_state else "direct_gemini",
                }))
            elif pass_result.pass_name == "violation_detection":
                count = len(pass_result.data.get("violations", []))
                yield "data: {}\n\n".format(json.dumps({
                    "pass": "violation_detection",
                    "violation_count": count,
                }))
            elif pass_result.pass_name == "consistency_check":
                verified = (
                    pass_result.data.get("verified_violations")
                    or pass_result.data.get("violations")
                    or []
                )
                raw = {
                    "violations": verified,
                    "positive_features": pass_result.data.get("positive_features", []),
                    "overall_risk": pass_result.data.get("overall_risk", "unknown"),
                    "summary": pass_result.data.get("summary", ""),
                    "follow_up_suggestions": pass_result.data.get("follow_up_suggestions", []),
                    "space_type": space_type,
                    "_pipeline_mode": "rocketride+gemini" if rr_state else "direct_gemini",
                }

        if raw is None:
            yield "data: {}\n\n".format(json.dumps({
                "pass": "error",
                "message": "Analysis failed — no result from pipeline",
            }))
            return

        # ── Enrich with knowledge base ──
        space_type = raw.get("space_type", "unknown")
        violations = (
            raw.get("verified_violations")
            or raw.get("violations")
            or []
        )
        merged = {
            "violations": violations,
            "positive_features": raw.get("positive_features", []),
            "overall_risk": raw.get("overall_risk", "unknown"),
            "summary": raw.get("summary", ""),
        }
        enriched = enrich_violations(merged, state=state)
        enriched["follow_up_suggestions"] = raw.get("follow_up_suggestions", [])
        enriched["space_type"] = space_type
        enriched["pipeline_mode"] = raw.get("_pipeline_mode", "unknown")

        # ── Generate PDF ──
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
