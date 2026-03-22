# RocketRide Integration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make RocketRide the core execution engine for the ADA Compliance Auditor so it qualifies for the Build with AI SF hackathon. The pipeline must be visually demonstrable in VS Code AND programmatically executable from the FastAPI backend via the Python SDK.

**Architecture:** The `.pipe` file defines a 3-pass Gemini pipeline (Scene Classification → Violation Detection → Consistency Check). The FastAPI backend loads this pipeline via the RocketRide Python SDK (`client.use(pipeline=config_dict)`), sends images via `client.send()`, and enriches results with the knowledge base. The visual pipeline in VS Code shows the architecture during the demo. Direct Gemini API calls serve as fallback when RocketRide isn't running.

**Tech Stack:** RocketRide Engine (local), RocketRide Python SDK (`rocketride`), Google Gemini 2.5 Flash, FastAPI, Python 3.12+

---

## Critical Context for the Implementing Agent

### RocketRide .pipe File Format (VERIFIED from working files)

The visual pipeline editor is built on React Flow. Nodes MUST have `"formDataValid": true` to show connection ports. The Gemini LLM node provider is `"llm_gemini"` (NOT `"gemini"`).

**Working Gemini node config** (extracted from user's UI-configured nodes):
```json
{
  "id": "llm_gemini_1",
  "provider": "llm_gemini",
  "config": {
    "profile": "gemini-2_5-flash",
    "gemini-3-pro": {},
    "gemini-2.5-flash": {
      "apiKey": "literal:${GEMINI_API_KEY}",
      "systemInstruction": "Your prompt here"
    },
    "parameters": { "google": {} },
    "gemini-2_5-flash": {
      "apikey": "literal:${GEMINI_API_KEY}"
    }
  },
  "ui": {
    "position": { "x": 500, "y": 400 },
    "measured": { "width": 160, "height": 65 },
    "data": { "provider": "llm_gemini", "class": "llm", "type": "default" },
    "formDataValid": true
  },
  "input": [{ "lane": "data", "from": "dropper_1" }]
}
```

**Key format details:**
- `"profile"` uses UNDERSCORES: `"gemini-2_5-flash"` (not dots)
- Two API key entries required: `"gemini-2.5-flash": { "apiKey": "..." }` (dot, capital K) AND `"gemini-2_5-flash": { "apikey": "..." }` (underscore, lowercase k)
- `"gemini-3-pro": {}` is a vestigial empty entry (left by the extension, don't remove)
- `"parameters": { "google": {} }` is required
- `"formDataValid": true` is REQUIRED for connection ports to render
- `"class": "llm"` must be a string, not an array

**Working connection format** (verified from dropper→parse that renders correctly):
```json
"input": [{ "lane": "tags", "from": "dropper_1" }]
```

**Lane names for chaining:**
- Source (dropper/webhook) → Gemini: `"lane": "data"`
- Gemini → Gemini: `"lane": "answers"`
- Gemini → Output: `"lane": "answers"`

**NOTE:** Visual connections between nodes may NOT render from JSON alone — the user may need to drag-connect them in the VS Code UI. This is a known limitation. The pipeline still executes correctly via the Python SDK regardless of visual connections.

### Pipeline Configuration for SDK Execution (from docs)

The `client.use()` method accepts either `filepath=` or `pipeline=` (dict). Using `pipeline=` with a loaded dict is more reliable because it avoids path resolution issues between the SDK client and the engine.

```python
# Load the .pipe file as a dict
with open("pipeline/ada_auditor.pipe") as f:
    pipeline_config = json.load(f)

result = await client.use(pipeline=pipeline_config)
token = result["token"]
response = await client.send(token, image_bytes, objinfo={"name": "photo.jpg"}, mimetype="image/jpeg")
```

The SDK auto-substitutes `${ROCKETRIDE_*}` patterns from `.env`.

### Environment Variables

```
ROCKETRIDE_URI=http://localhost:5565
ROCKETRIDE_APIKEY=             (empty for local, set for cloud)
GEMINI_API_KEY=literal:${GEMINI_API_KEY}
GOOGLE_MAPS_API_KEY=literal:${GOOGLE_MAPS_API_KEY}
```

### Existing Files

- `pipeline/ada_auditor.pipe` — The 3-pass visual pipeline (all nodes now have `formDataValid: true`)
- `backend/main.py` — FastAPI app with RocketRide SDK integration (routes through RocketRide first, falls back to direct Gemini)
- `backend/gemini_pipeline.py` — Direct Gemini 3-pass pipeline (fallback)
- `backend/prompts.py` — Dynamic prompt builders using knowledge base
- `backend/violations.py` — KB enrichment
- `backend/pdf_generator.py` — PDF report generation
- `backend/data/ada_knowledge_base.json` — 51 violation types
- `docs/rocketride/` — Full RocketRide documentation (90 pages saved as .md)

### Gemini API Key
`literal:${GEMINI_API_KEY}` (paid tier, set on Cloud Run)

### Hackathon Context (from Notion: Build with AI - SF Hackathon)

**Event:** Build with AI SF, March 21-22 2026, 10am-5pm, 995 Market St, San Francisco
**Luma:** https://luma.com/j2176blg
**Discord:** RocketRide: https://discord.com/invite/9hr3tdZmEG

**Theme:** "Design and build AI systems that meaningfully improve how people live, work, and interact with the world."

**A strong project should:**
1. Address a clear and specific real-world pain point
2. Go beyond a generic chatbot or wrapper
3. Demonstrate a working prototype with real functionality
4. Show how AI creates meaningful impact, not just novelty

**Think in terms of:** Systems, not just features. Workflows, not just prompts. Real users, not hypothetical scenarios.

**Submission:** Fill out form before Sunday 22th 5:00 PM. Link: https://www.notion.so/329a4bb59d718042ad74d2e7d20b0537

**RocketRide Sponsor Requirements (from Tool Resources page):**
- "Make RocketRide a core part of the system (not just a screenshot)"
- "Show your pipeline structure clearly: inputs, nodes, outputs, and why each step exists"
- "Prefer one 'wow' workflow over many half-finished ones"
- Use the IDE extension to build and run pipelines
- Create a `.pipe` file where you wire nodes together
- Start with a tiny end-to-end flow: Input → LLM call → Output
- Use deterministic prompts where you can so demos are repeatable
- SDK (optional): call a pipeline from an app using TypeScript or Python SDKs

**Quick start path recommended by RocketRide:**
1. Install the RocketRide extension in VS Code
2. Open the RocketRide (🚀) panel
3. Choose Local server (recommended)
4. Create a `.pipe` file and build your workflow (drag nodes, connect them, set params)

**Presenters:** Jerrison Li & Malik Harouna (3 minutes)

**Full hackathon docs saved to:** `docs/hackathon/` (being downloaded)

---

## Task 1: Align Backend Model to gemini-2.5-flash

**Files:**
- Modify: `backend/gemini_pipeline.py:19`
- Modify: `backend/gemini_client.py:18`

- [ ] **Step 1: Verify current model setting**

Run: `grep -n "MODEL = " backend/gemini_pipeline.py backend/gemini_client.py`
Expected: Both should show `MODEL = "gemini-2.5-flash"` (was changed from lite earlier in session)

- [ ] **Step 2: Run tests to confirm baseline**

Run: `uv run pytest tests/ -q`
Expected: 41 passed

- [ ] **Step 3: Commit if model was changed**

```bash
git add backend/gemini_pipeline.py backend/gemini_client.py
git commit -m "fix: align model to gemini-2.5-flash across backend"
```

---

## Task 2: Fix Pipeline SDK Execution — Use Dict Instead of Filepath

The current `_run_via_rocketride()` uses `client.use(filepath=PIPELINE_PATH)` which requires the RocketRide engine to resolve the file path. Using `client.use(pipeline=config_dict)` is more reliable per the docs.

**Files:**
- Modify: `backend/main.py:50-74`

- [ ] **Step 1: Refactor _run_via_rocketride to load pipeline as dict**

Replace the `_run_via_rocketride` function in `backend/main.py`:

```python
async def _run_via_rocketride(image_bytes: bytes, mime_type: str, state: str):
    """Execute the 3-pass analysis through the RocketRide pipeline engine."""
    from rocketride import RocketRideClient, AuthenticationException
    from rocketride.core.exceptions import PipeException, ExecutionException

    logger.info("Executing via RocketRide pipeline at %s", ROCKETRIDE_URI)

    # Load pipeline definition as dict (avoids filepath resolution issues)
    with open(PIPELINE_PATH) as f:
        pipeline_config = json.load(f)

    async with RocketRideClient(uri=ROCKETRIDE_URI, auth=ROCKETRIDE_APIKEY) as client:
        result = await client.use(pipeline=pipeline_config)
        token = result["token"]

        # Subscribe to processing events
        await client.set_events(token, ["apaevt_status_processing"])

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
```

- [ ] **Step 2: Enhance /api/pipeline/status to ping the engine**

Replace the `pipeline_status` endpoint in `backend/main.py`:

```python
@app.get("/api/pipeline/status")
async def pipeline_status():
    """Check pipeline execution mode and RocketRide availability."""
    rr_status = {"connected": False, "error": None}
    if USE_ROCKETRIDE:
        try:
            from rocketride import RocketRideClient
            async with RocketRideClient(uri=ROCKETRIDE_URI, auth=ROCKETRIDE_APIKEY) as client:
                rr_status["connected"] = client.is_connected()
                info = client.get_connection_info()
                rr_status["transport"] = info.get("transport", "unknown")
        except Exception as e:
            rr_status["error"] = str(e)

    return {
        "mode": "rocketride" if USE_ROCKETRIDE else "direct_gemini",
        "rocketride_uri": ROCKETRIDE_URI or None,
        "rocketride_available": USE_ROCKETRIDE,
        "rocketride_status": rr_status,
        "pipeline_file": PIPELINE_PATH,
        "model": "gemini-2.5-flash",
    }
```

- [ ] **Step 3: Run tests**

Run: `uv run pytest tests/ -q`
Expected: 41 passed

- [ ] **Step 4: Test endpoints manually**

Run:
```bash
cd backend && uv run python -c "
from main import app
from fastapi.testclient import TestClient
client = TestClient(app)
r = client.get('/api/pipeline/status')
print(r.json())
r = client.get('/api/config')
print(r.json())
"
```

- [ ] **Step 5: Commit**

```bash
git add backend/main.py
git commit -m "feat: load pipeline as dict via SDK, add engine health check"
```

---

## Task 3: Verify Visual Pipeline Has Connected Nodes

The `.pipe` file now has all three Gemini nodes with `formDataValid: true` and matching configs. The connections SHOULD render.

**Files:**
- Modify: `pipeline/ada_auditor.pipe` (only if connections still don't show)

- [ ] **Step 1: Open pipeline in VS Code**

Open `pipeline/ada_auditor.pipe` in VS Code. Check if connection lines show between nodes.

- [ ] **Step 2: If connections don't render, manually drag-connect**

If no lines show:
1. Drag from Dropper's `Data` output → first Gemini's input
2. Drag from Gemini 1's `Answers` output → Gemini 2's input
3. Drag from Gemini 2's `Answers` output → Gemini 3's input
4. Drag from Gemini 3's `Answers` output → Local Text Output's input
5. Save the file (Cmd+S)

- [ ] **Step 3: Read the saved file to capture the extension's connection format**

After saving, read `pipeline/ada_auditor.pipe` and note the exact `input` format the extension wrote. This is the canonical format for future reference.

- [ ] **Step 4: Commit the working pipeline**

```bash
git add pipeline/ada_auditor.pipe
git commit -m "feat: working 3-pass RocketRide pipeline with visual connections"
```

---

## Task 4: Test End-to-End RocketRide Pipeline Execution

**Prerequisites:** RocketRide local engine must be running (status bar should show "RocketRide: Connected (local)")

- [ ] **Step 1: Test via Python SDK directly**

```bash
uv run python3 -c "
import asyncio, json
from rocketride import RocketRideClient

async def test():
    async with RocketRideClient() as client:
        with open('pipeline/ada_auditor.pipe') as f:
            config = json.load(f)
        result = await client.use(pipeline=config)
        print('Pipeline started:', result['token'])
        # Send a test image
        with open('00-examples/San_Francisco__building_with_steps.webp', 'rb') as img:
            response = await client.send(result['token'], img.read(), objinfo={'name': 'test.webp'}, mimetype='image/webp')
        print('Response:', json.dumps(response, indent=2)[:500])
        await client.terminate(result['token'])

asyncio.run(test())
"
```

- [ ] **Step 2: Test via the web app**

1. Start the backend: `cd backend && uv run uvicorn main:app --reload --port 8000`
2. Open http://localhost:8000
3. Upload one of the example images
4. Enter a San Francisco address
5. Click Analyze
6. Verify the report shows `pipeline_mode: "rocketride"` (check browser console or the API response)

- [ ] **Step 3: Test the fallback (stop RocketRide, verify direct Gemini still works)**

1. Stop the RocketRide engine (disconnect from VS Code sidebar)
2. Upload another image and analyze
3. Verify it still works via direct Gemini API (may show `pipeline_mode: "direct_gemini"`)

---

## Task 5: Deploy to Cloud Run

**Files:**
- No code changes needed — just deploy

- [ ] **Step 1: Commit all pending changes**

```bash
git add -A && git status
git commit -m "feat: complete RocketRide integration with SDK execution and visual pipeline"
git push origin main
```

- [ ] **Step 2: Deploy to Cloud Run**

```bash
gcloud run deploy ada-auditor \
  --source . \
  --region us-central1 \
  --project ada-compliance-490919 \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 300 \
  --concurrency 10
```

Note: Cloud Run won't have a local RocketRide engine, so it will use the direct Gemini fallback. This is expected — the RocketRide demo is done locally from VS Code during the presentation.

- [ ] **Step 3: Verify Cloud Run deployment works**

```bash
curl -s https://ada-auditor-908021165922.us-central1.run.app/api/pipeline/status
```

Expected: `"mode": "direct_gemini"` (no RocketRide engine on Cloud Run)

---

## Task 6: Prepare Demo Script

- [ ] **Step 1: Write demo script for the presentation**

The demo flow for showing RocketRide integration:

1. **Show the visual pipeline** — Open `pipeline/ada_auditor.pipe` in VS Code. Point out the 5 nodes: Dropper → Gemini (Scene Classification) → Gemini (Violation Detection) → Gemini (Consistency Check) → Output
2. **Show the SDK integration** — Open `backend/main.py`, show `_run_via_rocketride()` which loads the pipeline config and executes via `RocketRideClient`
3. **Run the pipeline** — From VS Code, hit play on the Dropper node, drop in a building photo, show results flowing through the 3 passes
4. **Show the web app** — Open the live Cloud Run URL, upload a photo, show the full report
5. **Talking point:** "RocketRide is our pipeline execution engine. We define the 3-pass Gemini analysis as a visual directed graph, and our FastAPI backend executes it via the Python SDK. This separates pipeline design from application code — you can modify the analysis flow without changing the backend."

---

## Summary of Changes

| File | Change |
|------|--------|
| `backend/gemini_pipeline.py` | MODEL = "gemini-2.5-flash" |
| `backend/gemini_client.py` | MODEL = "gemini-2.5-flash" |
| `backend/main.py` | Load pipeline as dict, add event streaming, improve error handling, enhance /api/pipeline/status |
| `pipeline/ada_auditor.pipe` | All nodes `formDataValid: true`, matching configs, `source` field added |
| `.env` | ROCKETRIDE_URI, GEMINI_API_KEY already set |
