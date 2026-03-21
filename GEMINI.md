# GEMINI.md — ADA Compliance Auditor

## Project Overview

ADA Compliance Auditor: AI-powered tool that analyzes photos of buildings and public spaces for ADA accessibility violations. Returns structured reports with ADA code references, severity ratings, and remediation cost estimates.

**Hackathon project** — Build with AI - SF (March 2026).

For detailed system design, see `ARCHITECTURE.md`.

## Setup & Run

```bash
# Package manager is uv (not pip)
uv sync

# Start the backend server
cd backend && uv run uvicorn main:app --reload --port 8000

# Frontend auto-served at http://localhost:8000
```

### Environment Variables

```bash
cp .env.example .env
# GOOGLE_CLOUD_PROJECT=<your-gcp-project-id>  (required)
# GOOGLE_CLOUD_LOCATION=us-central1           (optional, default)
gcloud auth application-default login
```

## Architecture

```
Photo → Frontend (vanilla JS) → POST /api/analyze → FastAPI backend
  → RocketRide pipeline (primary) OR direct Gemini 2.0 Flash (fallback)
  → Raw violations → Enrichment (ADA codes + costs) → JSON response → UI
```

### Key Files

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI app, `/api/analyze` endpoint, CORS, Vertex AI init |
| `backend/gemini_client.py` | Gemini 2.0 Flash wrapper, structured analysis prompt |
| `backend/pipeline_client.py` | RocketRide engine client (localhost:5565) |
| `backend/violations.py` | Maps violations → ADA sections + cost estimates |
| `backend/data/ada_codes.json` | 18 violation types with ADA section references |
| `backend/data/cost_estimates.json` | Remediation cost ranges per violation type |
| `frontend/index.html` | Dark-theme UI with Tailwind CSS |
| `frontend/app.js` | File upload, API integration, result rendering |
| `frontend/style.css` | Severity colors, interaction states |
| `pipeline/ada_auditor.pipe.json` | RocketRide visual pipeline definition |

## Coding Guidelines

### Python (backend/)
- Use `logging` module — not print()
- Async route handlers for FastAPI
- JSON-formatted API responses
- Import order: stdlib → third-party → local modules

### JavaScript (frontend/)
- Vanilla JS only — no frameworks, no build tools
- Tailwind CSS loaded via CDN
- DOM manipulation with getElementById/querySelector

## Critical Rules

1. **Always try RocketRide pipeline before direct Gemini API** — the fallback path exists for when the pipeline engine isn't running
2. **Violation types must stay synchronized** across three locations:
   - `backend/data/ada_codes.json` (ADA section mapping)
   - `backend/data/cost_estimates.json` (cost ranges)
   - `backend/gemini_client.py` (analysis prompt)
3. **Frontend has no build step** — served as static files by FastAPI
4. **Never commit `.env`** — it contains GCP credentials
5. **CORS is permissive** (`*`) — this is a hackathon demo, not production

## Testing

No automated tests yet. Manual validation:
1. Start server: `cd backend && uv run uvicorn main:app --reload --port 8000`
2. Open http://localhost:8000
3. Upload a building/entrance photo
4. Check response for: violations array, ADA codes, severity levels, confidence scores, cost estimates

## Commit Conventions

- Small, focused commits — one logical change per commit
- Descriptive messages explaining intent, not just changes
