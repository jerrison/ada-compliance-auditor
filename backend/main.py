import os
import logging

from dotenv import load_dotenv

load_dotenv()

import vertexai
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pipeline_client import analyze_via_pipeline
from gemini_client import analyze_image_direct
from violations import enrich_violations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
)

app = FastAPI(title="ADA Compliance Auditor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    """Analyze an uploaded image for ADA compliance violations.

    Tries RocketRide pipeline first, falls back to direct Gemini API.
    """
    contents = await file.read()
    mime_type = file.content_type or "image/jpeg"

    # Try RocketRide pipeline first
    raw_analysis = await analyze_via_pipeline(contents, mime_type)

    # Fallback to direct Gemini call
    if raw_analysis is None:
        logger.info("Using direct Gemini API (RocketRide not available)")
        raw_analysis = analyze_image_direct(contents, mime_type)

    enriched = enrich_violations(raw_analysis)
    return enriched


@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
