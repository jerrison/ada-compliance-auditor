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

# RocketRide integration (optional -- used when ROCKETRIDE_URI is set)
ROCKETRIDE_URI = os.getenv("ROCKETRIDE_URI", "")
ROCKETRIDE_APIKEY = os.getenv("ROCKETRIDE_APIKEY", "")
PIPELINE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pipeline", "ada_auditor.pipe.json")
_rr_client = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


@app.get("/api/config")
async def get_config():
    """Return client-safe configuration values."""
    return {"google_maps_api_key": os.getenv("GOOGLE_MAPS_API_KEY", "")}


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...), location_label: str = Form(""), state: str = Form("")):
    """Analyze image via 3-pass Gemini pipeline with SSE progress streaming."""
    contents = await file.read()
    mime_type = file.content_type or "image/jpeg"

    async def event_stream():
        space_type = "unknown"

        async for pass_result in run_analysis_pipeline(contents, mime_type, state=state):
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
                # Pass 3 returns "verified_violations" (not "violations")
                # Fall back to "violations" if the model uses that key instead
                verified = (
                    pass_result.data.get("verified_violations")
                    or pass_result.data.get("violations")
                    or []
                )
                merged = {
                    "violations": verified,
                    "positive_features": pass_result.data.get("positive_features", []),
                    "overall_risk": pass_result.data.get("overall_risk", "unknown"),
                    "summary": pass_result.data.get("summary", ""),
                }

                enriched = enrich_violations(merged, state=state)
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


@app.get("/api/pipeline/status")
async def pipeline_status():
    """Check if RocketRide pipeline is available."""
    return {
        "rocketride_available": bool(ROCKETRIDE_URI),
        "rocketride_uri": ROCKETRIDE_URI or None,
        "pipeline_file": PIPELINE_PATH,
        "mode": "rocketride" if ROCKETRIDE_URI else "direct_gemini",
    }


@app.post("/api/pipeline/run")
async def run_pipeline(file: UploadFile = File(...), location_label: str = Form(""), state: str = Form("")):
    """Run analysis via RocketRide pipeline (requires ROCKETRIDE_URI env var)."""
    global _rr_client
    if not ROCKETRIDE_URI:
        return Response(status_code=400, content=json.dumps({
            "error": "RocketRide not configured. Set ROCKETRIDE_URI env var or use /api/analyze for direct Gemini."
        }), media_type="application/json")

    try:
        from rocketride import RocketRideClient

        contents = await file.read()
        mime_type = file.content_type or "image/jpeg"

        async with RocketRideClient(uri=ROCKETRIDE_URI, auth=ROCKETRIDE_APIKEY) as client:
            # Start the pipeline
            result = await client.use(filepath=PIPELINE_PATH)
            token = result["token"]

            # Send the image into the pipeline
            response = await client.send(
                token,
                contents,
                objinfo={"name": "building_photo.jpg"},
                mimetype=mime_type,
            )

            # Get the pipeline output
            status = await client.get_task_status(token)
            await client.terminate(token)

            # Enrich the raw pipeline output
            raw_report = response if isinstance(response, dict) else json.loads(response)
            verified = raw_report.get("verified_violations") or raw_report.get("violations", [])
            merged = {
                "violations": verified,
                "positive_features": raw_report.get("positive_features", []),
                "overall_risk": raw_report.get("overall_risk", "unknown"),
                "summary": raw_report.get("summary", ""),
            }
            enriched = enrich_violations(merged, state=state)
            enriched["space_type"] = raw_report.get("space_type", "unknown")
            enriched["pipeline_mode"] = "rocketride"
            enriched["pipeline_status"] = status.get("state", "unknown")

            # Generate PDF
            pdf_bytes = generate_pdf_report(
                report=enriched,
                location_label=location_label or "Unknown Location",
                space_type=enriched["space_type"],
                image_bytes=contents,
            )
            pdf_id = str(uuid.uuid4())
            _pdf_store[pdf_id] = pdf_bytes
            enriched["pdf_url"] = "/api/reports/{}/pdf".format(pdf_id)

            return enriched

    except ImportError:
        return Response(status_code=500, content=json.dumps({
            "error": "rocketride package not installed. Run: uv add rocketride"
        }), media_type="application/json")
    except Exception as e:
        logger.error("RocketRide pipeline failed: %s", e)
        return Response(status_code=500, content=json.dumps({
            "error": str(e),
            "fallback": "Use /api/analyze for direct Gemini analysis"
        }), media_type="application/json")


@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
