# Architecture

## System Overview

ADA Compliance Auditor is a web application that uses AI vision to analyze photos of buildings and public spaces for ADA accessibility violations. It produces structured reports with ADA code references, severity ratings, and remediation cost estimates.

## Data Flow

```
User uploads photo
  → Frontend (vanilla JS) sends POST /api/analyze
    → Backend (FastAPI) receives image bytes + mime type
      → Try RocketRide pipeline first (pipeline/ada_auditor.pipe.json)
      → Fallback: direct Gemini 2.0 Flash API call
    → Raw analysis JSON (violations, severity, confidence)
      → Enrichment layer maps violations to knowledge base (backend/data/ada_knowledge_base.json):
        - ADA/CBC/SF code sections, remediation steps, cost estimates, legal risk
    → Enriched JSON response → Frontend renders report
```

## Directory Structure

```
├── backend/                    # FastAPI service (Python)
│   ├── main.py                 # App entry, routes, CORS, Vertex AI init
│   ├── gemini_client.py        # Gemini Vision API wrapper (direct + pipeline)
│   ├── pipeline_client.py      # RocketRide SDK integration
│   ├── violations.py           # ADA code enrichment + cost estimation
│   └── data/
│       └── ada_knowledge_base.json  # 51 violation types → codes, costs, remediation, detection
├── frontend/                   # Static web UI
│   ├── index.html              # Tailwind CSS dark-theme layout
│   ├── app.js                  # Upload, API call, result rendering
│   └── style.css               # Severity color scheme, drag-drop states
├── pipeline/
│   └── ada_auditor.pipe.json   # RocketRide visual pipeline definition
├── pyproject.toml              # uv project config, dependencies
├── .env.example                # Required env vars template
└── main.py                     # Root entry (scaffold placeholder, not used by backend)
```

## Key Components

### Backend (`backend/`)

| File | Responsibility |
|------|---------------|
| `main.py` | FastAPI app, CORS middleware, `/api/analyze` endpoint, serves frontend static files |
| `gemini_client.py` | Wraps Gemini 2.0 Flash for image analysis. Dynamic prompt built from knowledge base with 51 violation types and visual detection cues. Temperature 0.2, JSON response format |
| `pipeline_client.py` | Connects to RocketRide engine at `localhost:5565`. Base64 encodes images, sends through pipeline. Graceful fallback on failure |
| `violations.py` | Loads knowledge base. Enriches violations with codes, costs, remediation, legal risk. Produces structured report JSON with priority sorting |

### Frontend (`frontend/`)

Vanilla JS with Tailwind CSS (CDN). No build step. Features: drag-and-drop upload, image preview, severity-colored violation cards, cost summary, risk badge (HIGH/MEDIUM/LOW).

### Pipeline (`pipeline/`)

RocketRide visual pipeline: webhook source → image processor → Gemini 2.0 Flash LLM → output. Requires RocketRide VS Code extension and local engine running.

## Dependencies

- **Runtime**: Python >=3.12, FastAPI, uvicorn, python-multipart, google-cloud-aiplatform, python-dotenv, rocketride
- **Package manager**: uv
- **Note**: `rocketride` is not on PyPI — it installs via the RocketRide VS Code extension ecosystem. The app falls back to direct Gemini API if the package or engine is unavailable.
- **AI model**: Gemini 2.0 Flash via Vertex AI
- **Frontend CDN**: Tailwind CSS

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_CLOUD_PROJECT` | Yes | GCP project ID for Vertex AI |
| `GOOGLE_CLOUD_LOCATION` | No | GCP region (default: `us-central1`) |

## Violation Types (51 total)

Organized into 8 categories:

- **california_sf** — California Building Code and SF-specific requirements
- **counters** — Counter height and accessibility
- **entrances** — Door hardware, thresholds, entrance accessibility
- **parking** — Accessible parking spaces, signage, striping
- **ramps** — Ramp slope, handrails, landings
- **restrooms** — Grab bars, clearances, fixtures
- **routes** — Accessible paths of travel, surfaces, obstructions
- **signage** — Tactile, directional, and informational signage
