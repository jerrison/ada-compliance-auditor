# ADA Compliance Auditor

AI-powered accessibility auditor that analyzes photos of buildings and public spaces for ADA compliance violations. Upload a photo, get instant analysis with specific ADA code references, severity ratings, and remediation cost estimates.

## Architecture

```
Photo Upload → [RocketRide Pipeline] → Gemini Vision Analysis → ADA Code Mapping → Cost Estimation → Report
```

**RocketRide Pipeline** (`pipeline/ada_auditor.pipe.json`):
- Source (webhook) → Image Processor → Gemini 2.0 Flash → Output

**Backend** (FastAPI):
- Calls RocketRide pipeline via Python SDK
- Enriches raw analysis with ADA code sections and cost estimates
- Falls back to direct Gemini API if RocketRide engine is not running

**Frontend** (Vanilla JS + Tailwind):
- Drag-and-drop image upload
- Displays violations with severity, ADA codes, and cost ranges

## Quick Start

```bash
# 1. Clone and install
git clone <repo-url>
cd 01-build-with-ai-sf
uv sync

# 2. Set up Google Cloud credentials
cp .env.example .env
# Edit .env with your project ID
gcloud auth application-default login

# 3. Set up RocketRide
# - Install RocketRide VS Code extension
# - Open the RocketRide panel, start local engine
# - Open pipeline/ada_auditor.pipe.json in VS Code

# 4. Run the app
cd backend
uv run uvicorn main:app --reload --port 8000

# 5. Open http://localhost:8000
```

## Tech Stack

- **AI**: Google Gemini 2.0 Flash (multimodal vision)
- **Pipeline**: RocketRide (visual AI pipeline builder)
- **Backend**: Python, FastAPI
- **Frontend**: HTML, Tailwind CSS, Vanilla JS
- **Cloud**: Google Cloud (Vertex AI)

## Judging Criteria Alignment

| Criteria | How We Score |
|----------|-------------|
| **Impact** | 40M+ Americans with disabilities. 8,667 ADA lawsuits/year. $75K+ penalties. |
| **Innovation** | First AI-powered physical space accessibility auditor (not web/WCAG). |
| **Execution** | End-to-end working prototype: photo → analysis → structured report. |
| **Use of AI** | Gemini Vision is the core engine - multimodal analysis, not a wrapper. |
| **Presentation** | Live demo: walk outside, photograph a building, get instant results. |

## Built at Build with AI - SF Hackathon (March 2026)
