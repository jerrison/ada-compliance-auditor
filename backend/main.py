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
