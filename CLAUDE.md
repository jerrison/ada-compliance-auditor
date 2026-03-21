# CLAUDE.md — ADA Compliance Auditor

## Project Context

Hackathon project (Build with AI - SF, March 2026). AI-powered ADA accessibility auditor that analyzes photos of buildings/public spaces for compliance violations using Gemini Vision.

See `ARCHITECTURE.md` for full system design and data flow.

## Build & Run

```bash
# Install dependencies
uv sync

# Run backend (from project root)
cd backend && uv run uvicorn main:app --reload --port 8000

# App serves at http://localhost:8000
# Frontend is served as static files from backend
```

## Code Style

### Python (backend/)
- No type stubs or excessive type annotations — keep it practical
- Use `logging` module (already configured in main.py), not print()
- Imports: stdlib → third-party → local (no enforced formatter, but keep it clean)
- JSON response format for all API endpoints
- Async handlers for FastAPI routes

### JavaScript (frontend/)
- Vanilla JS only — no frameworks, no build step
- Tailwind CSS via CDN for styling
- DOM manipulation via getElementById/querySelector
- No module bundler — script tags in HTML

## Architecture Rules

- **Two execution paths**: RocketRide pipeline (primary) → Direct Gemini API (fallback). Always try pipeline first.
- **Data files are source of truth**: `backend/data/ada_codes.json` and `backend/data/cost_estimates.json` define the 18 supported violation types. New violation types must be added to both files.
- **Frontend is static**: served by FastAPI's StaticFiles mount. No SSR, no build step.
- **CORS is wide open** (`allow_origins=["*"]`) — acceptable for hackathon/demo, not production.

## Key Paths

- Backend entry: `backend/main.py`
- API endpoint: `POST /api/analyze` (accepts multipart file upload)
- Gemini prompt: defined inline in `backend/gemini_client.py`
- Pipeline config: `pipeline/ada_auditor.pipe.json`
- ADA reference data: `backend/data/ada_codes.json`
- Cost data: `backend/data/cost_estimates.json`

## Environment Setup

```bash
cp .env.example .env
# Set GOOGLE_CLOUD_PROJECT=<your-gcp-project>
gcloud auth application-default login
```

Optional: Start RocketRide local engine for pipeline mode (VS Code extension required).

## Testing

No test suite yet. To validate manually:
1. Start the server (`cd backend && uv run uvicorn main:app --reload --port 8000`)
2. Open http://localhost:8000
3. Upload a photo of a building entrance or public space
4. Verify the response includes violations with ADA codes, severity, confidence, and cost estimates

## Security Notes

- Never commit `.env` files (contains GCP credentials)
- Image data is processed in-memory, not persisted to disk
- CORS is permissive — tighten for any production deployment
- Gemini API calls go through Vertex AI (authenticated via ADC)
