# ADA Compliance Auditor

AI-powered accessibility auditor that analyzes photos of buildings and public spaces for ADA compliance violations. Upload a photo, get instant analysis with specific ADA code references, severity ratings, and remediation cost estimates.

**Live App**: https://ada-auditor-908021165922.us-central1.run.app

**Pitch Deck**: https://docs.google.com/presentation/d/1WjN0xHFu8XcZsfil16k02PNzoV0S8tKTArAfAiBr0yE/edit

**Team**: Jerrison Li & Malik Harouna

## How It Works

1. Upload a photo of any building entrance, parking lot, restroom, or public space
2. Enter the address — RocketRide pipeline extracts the state jurisdiction and applicable building codes
3. Gemini 2.5 Flash Vision runs 3-pass analysis: Scene Classification → Violation Detection → Consistency Verification
4. Get a prioritized report with ADA code references, severity ratings, confidence scores, and remediation cost estimates
5. Download a PDF report to share with contractors

## Architecture

```
Address Input → [RocketRide Pipeline] → Jurisdiction Extraction
Photo Upload  → [Gemini Vision 3-Pass] → Scene → Violations → Verification
                                           ↓
                        ADA Knowledge Base (51 violation types)
                                           ↓
                              Enriched Report + PDF
```

- **RocketRide** processes the address through a visual pipeline (Chat → Prompt → Return) to extract state jurisdiction
- **Gemini 2.5 Flash** performs multimodal vision analysis — the image bytes are sent directly with the prompt for each of the 3 passes
- **Knowledge Base** enriches results with federal ADA codes, California CBC Title 24, and local ordinances for 7 cities
- **PDF Generator** produces downloadable reports with violation details, cost estimates, and tax credit information

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Pipeline | RocketRide (orchestration engine, Python SDK, VS Code visual pipeline) |
| AI/Vision | Google Gemini 2.5 Flash (multimodal, 3-pass analysis) |
| Backend | Python, FastAPI, SSE streaming |
| Frontend | Vanilla JS, Tailwind CSS, PWA (offline-capable, IndexedDB) |
| Reports | ReportLab PDF generation |
| Deployment | Google Cloud Run, Docker |
| APIs | Google Maps Places (address autocomplete), Nominatim (fallback) |

## Quick Start

```bash
# Install
git clone https://github.com/jerrison/ada-compliance-auditor.git
cd ada-compliance-auditor
uv sync

# Configure
cp .env.example .env
# Set GEMINI_API_KEY and GOOGLE_MAPS_API_KEY in .env

# Run
cd backend && uv run uvicorn main:app --reload --port 8000
# Open http://localhost:8000
```

Optional: Install the RocketRide VS Code extension and start the local engine for pipeline orchestration.

## ADA Violation Coverage

51 violation types across 6 space categories (entrance, parking, interior, restroom, sidewalk, counter/service area), mapped to:
- **Federal ADA** (Americans with Disabilities Act)
- **California Building Code** (CBC Title 24)
- **Local codes**: San Francisco, Los Angeles, San Jose, San Diego, Long Beach, Sacramento, Oakland

## Built at Build with AI SF Hackathon (March 21-22, 2026)
