# ADA Compliance Auditor — Demo Script (3 min)

## Presenters: Jerrison Li & Malik Harouna

---

## 1. The Problem (30 sec)

> "8,667 ADA federal lawsuits were filed in 2025. In California, serial filers
> exploit the Unruh Act — $4,000 minimum per visit — targeting small businesses
> that don't know they're non-compliant. A single CASp inspection costs
> $2,000-5,000 and takes weeks to schedule. We built an AI auditor that gives
> you an instant compliance report from a photo."

## 2. Live Demo — Web App (60 sec)

1. Open the live app: **https://ada-auditor-908021165922.us-central1.run.app**
2. Upload a photo of a building entrance (use `00-examples/San_Francisco__building_with_steps.webp`)
3. Enter a San Francisco address
4. Click **Analyze**
5. Walk through the report:
   - **Space classification** (entrance, parking lot, etc.)
   - **Violations** with ADA codes, severity, confidence scores
   - **Estimated remediation costs** (single numbers, not ranges)
   - **Positive features** already in compliance
   - **PDF download** for sharing with contractors

## 3. RocketRide Pipeline Architecture (60 sec)

> "Under the hood, we use RocketRide as our pipeline execution engine."

1. **Switch to VS Code** — open `pipeline/ada_auditor.pipe`
2. Point out the 5-node directed graph:
   - **Dropper** (image input)
   - **Gemini Pass 1** — Scene Classification (entrance? parking lot? restroom?)
   - **Gemini Pass 2** — Violation Detection (checks 51 violation types from our knowledge base)
   - **Gemini Pass 3** — Consistency Check (removes false positives, adjusts confidence)
   - **Output** (text results)
3. **Show the SDK integration** — open `backend/main.py`, show `_run_via_rocketride()`:
   > "Our FastAPI backend loads this pipeline config as a dict and executes it
   > through the RocketRide Python SDK. This separates pipeline design from
   > application code — you can modify the analysis flow in VS Code without
   > touching the backend."

4. **Show the fallback** — the backend tries RocketRide first, falls back to
   direct Gemini API calls. Cloud Run uses the fallback; local dev uses the
   full pipeline.

## 4. Technical Differentiators (30 sec)

- **3-pass pipeline** reduces false positives (scene → detect → verify)
- **51-type knowledge base** with ADA/CBC codes, remediation steps, and cost estimates
- **State-aware analysis** — California CBC, SF local codes
- **PDF reports** with photo, violations, costs — shareable with contractors
- **RocketRide integration** — visual pipeline design + programmatic SDK execution

## Key Talking Points

- "We're not just wrapping an LLM. The 3-pass pipeline with a structured
  knowledge base produces actionable compliance reports, not generic
  suggestions."
- "RocketRide is our execution engine — we define the multi-step Gemini
  analysis as a visual graph, and execute it via the Python SDK."
- "This addresses a $1.4B market. Every building renovation, lease signing,
  or business opening triggers an ADA compliance check."
