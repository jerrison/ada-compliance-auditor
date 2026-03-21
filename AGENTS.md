# AGENTS.md — ADA Compliance Auditor

> AI-powered ADA accessibility auditor: photo upload → Gemini Vision analysis → ADA code mapping → cost estimation → structured report.

## Quick Orientation

- **Architecture**: See `ARCHITECTURE.md` for full system design, data flow, and component responsibilities.
- **Tech stack**: Python/FastAPI backend, vanilla JS/Tailwind frontend, Gemini 2.0 Flash via Vertex AI, RocketRide pipeline.
- **Package manager**: `uv` (not pip). Use `uv sync` to install, `uv run` to execute.

## Build & Run

```bash
# Install
uv sync

# Run (from project root)
cd backend && uv run uvicorn main:app --reload --port 8000

# Serves at http://localhost:8000
```

## Environment

```bash
cp .env.example .env
# Required: GOOGLE_CLOUD_PROJECT=<your-gcp-project-id>
# Optional: GOOGLE_CLOUD_LOCATION=us-central1 (default)
gcloud auth application-default login
```

## Project Structure

```
backend/main.py             → FastAPI app, routes, middleware
backend/gemini_client.py    → Gemini Vision API (direct + pipeline modes)
backend/pipeline_client.py  → RocketRide SDK client
backend/violations.py       → ADA code enrichment + cost mapping
backend/data/ada_codes.json → 18 violation types → ADA section references
backend/data/cost_estimates.json → 18 violation types → remediation costs
frontend/index.html         → UI (Tailwind dark theme)
frontend/app.js             → Upload, API calls, result rendering
frontend/style.css          → Severity colors, drag-drop states
pipeline/ada_auditor.pipe.json → RocketRide visual pipeline config
```

## Code Conventions

### Python (backend/)
- Async handlers for FastAPI routes
- Use `logging` module, not print()
- JSON responses for all API endpoints
- Imports: stdlib → third-party → local

### JavaScript (frontend/)
- Vanilla JS only — no frameworks, no bundler, no build step
- Tailwind CSS via CDN
- Direct DOM manipulation

## Architecture Invariants

1. **Dual execution path**: Always try RocketRide pipeline first, fall back to direct Gemini API. Never remove the fallback.
2. **Data-driven violations**: The 18 violation types are defined in `backend/data/ada_codes.json` and `backend/data/cost_estimates.json`. Adding a new violation type requires updating both JSON files AND the Gemini prompt in `gemini_client.py`.
3. **Static frontend**: No SSR, no build step. Frontend served via FastAPI's StaticFiles mount at `/static`.
4. **No test suite yet**: Validate changes manually by running the server and uploading an image.

## API

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/analyze` | Upload image (multipart), returns enriched violation analysis JSON |
| GET | `/` | Serves frontend HTML |

## Security

- `.env` is gitignored — never commit credentials
- Image data is in-memory only (not persisted)
- CORS allows all origins (demo/hackathon setting)
- Vertex AI authenticated via Application Default Credentials

## Commit Style

- Small, logical commits — each reviewable independently
- PR descriptions explain *why*, not just *what*
- Link to relevant issue or spec when applicable
