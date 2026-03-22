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
async def _run_via_rocketride(image_bytes: bytes, mime_type: str, state: str):
    """Execute the 3-pass analysis through the RocketRide pipeline engine."""
    from rocketride import RocketRideClient

    logger.info("Executing via RocketRide pipeline at %s", ROCKETRIDE_URI)

    async with RocketRideClient(uri=ROCKETRIDE_URI, auth=ROCKETRIDE_APIKEY) as client:
        result = await client.use(filepath=PIPELINE_PATH)
        token = result["token"]

        response = await client.send(
            token,
            image_bytes,
            objinfo={"name": "building_photo.jpg"},
            mimetype=mime_type,
        )

        status = await client.get_task_status(token)
        await client.terminate(token)

        raw = response if isinstance(response, dict) else json.loads(response)
        raw["_pipeline_mode"] = "rocketride"
        raw["_pipeline_status"] = status.get("state", "unknown")
        return raw


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
    return {
        "mode": "rocketride" if USE_ROCKETRIDE else "direct_gemini",
        "rocketride_uri": ROCKETRIDE_URI or None,
        "rocketride_available": USE_ROCKETRIDE,
        "pipeline_file": PIPELINE_PATH,
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

    async def event_stream():
        # ── Try RocketRide first, fall back to direct Gemini ──
        raw = None
        try:
            if USE_ROCKETRIDE:
                yield "data: {}\n\n".format(json.dumps({
                    "pass": "scene_classification",
                    "space_type": "analyzing",
                    "pipeline_mode": "rocketride",
                }))
                raw = await _run_via_rocketride(contents, mime_type, state)
                space_type = raw.get("space_type", "unknown")
                violations = (
                    raw.get("verified_violations")
                    or raw.get("violations")
                    or []
                )
                yield "data: {}\n\n".format(json.dumps({
                    "pass": "violation_detection",
                    "violation_count": len(violations),
                }))
        except Exception as e:
            logger.warning("RocketRide failed (%s), falling back to direct Gemini", e)

        # ── Fallback: stream each pass individually ──
        if raw is None:
            space_type = "unknown"
            async for pass_result in run_analysis_pipeline(contents, mime_type, state=state):
                if pass_result.pass_name == "scene_classification":
                    space_type = pass_result.data.get("space_type", "unknown")
                    yield "data: {}\n\n".format(json.dumps({
                        "pass": "scene_classification",
                        "space_type": space_type,
                        "pipeline_mode": "direct_gemini",
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
                        "_pipeline_mode": "direct_gemini",
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
