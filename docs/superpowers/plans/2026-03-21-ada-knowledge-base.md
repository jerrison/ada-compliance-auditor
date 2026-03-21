# ADA Knowledge Base Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a comprehensive ADA compliance knowledge base (~56 violation types) covering federal ADA, CBC Title 24, and SF local codes, with an enrichment layer that produces report-ready JSON for iOS app and HTML/PDF consumers.

**Architecture:** Single JSON knowledge base file replaces two existing data files. `violations.py` is rewritten to load the KB and produce a structured report payload with priority sorting. `gemini_client.py` is rewritten to dynamically build its prompt from the KB's violation types and visual cues.

**Tech Stack:** Python 3.12+, FastAPI, pytest, JSON

**Spec:** `docs/superpowers/specs/2026-03-21-ada-knowledge-base-design.md`

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `backend/data/ada_knowledge_base.json` | Create | ~56 violation entries with full schema (codes, costs, remediation, detection) |
| `backend/violations.py` | Rewrite | Load KB, enrich violations, compute priority/risk, produce report JSON |
| `backend/gemini_client.py` | Rewrite | Build prompt dynamically from KB, keep same Gemini call interface |
| `backend/data/ada_codes.json` | Delete | Superseded by knowledge base |
| `backend/data/cost_estimates.json` | Delete | Superseded by knowledge base |
| `tests/test_violations.py` | Create | Tests for enrichment, priority sorting, risk computation, headline generation |
| `tests/test_gemini_client.py` | Create | Tests for dynamic prompt building |
| `ARCHITECTURE.md` | Update | Reflect new KB file, ~56 violation types, updated data flow |
| `CLAUDE.md` | Update | Update Key Paths to reference new KB file |

---

### Task 1: Research ADA/CBC/SF code references

**Files:**
- Reference: `docs/superpowers/specs/2026-03-21-ada-knowledge-base-design.md` (violation list)
- Reference: `backend/data/ada_codes.json` (existing 18 entries for baseline)

This is a research task. For each of the ~56 violation types listed in the spec, research and document the accurate code references:
- Federal ADA Standards section numbers and requirement text
- CBC Title 24 (Chapter 11B) section numbers and where they differ from federal
- SF local ordinances where applicable

- [ ] **Step 1: Research Entrances & Doors (8 types)**

Web search for ADA Standards sections 404, 405, 206 and CBC 11B equivalents. Document section numbers and requirement text for: `missing_ramp`, `no_accessible_entrance`, `step_only_entrance`, `narrow_doorway`, `round_door_knob`, `missing_automatic_door`, `insufficient_door_clearance`, `excessive_door_force`.

- [ ] **Step 2: Research Ramps & Slopes (6 types)**

ADA sections 405.x and CBC 11B-405.x for: `steep_ramp`, `missing_handrail`, `missing_ramp_landing`, `missing_edge_protection`, `missing_handrail_extensions`, `excessive_ramp_rise`.

- [ ] **Step 3: Research Parking (5 types)**

ADA sections 502.x and CBC 11B-502.x for: `missing_accessible_parking_sign`, `missing_parking_striping`, `insufficient_accessible_spaces`, `missing_van_accessible_space`, `damaged_parking_surface`.

- [ ] **Step 4: Research Routes & Pathways (8 types)**

ADA sections 402, 406, 307 and CBC 11B equivalents for: `blocked_accessible_route`, `missing_curb_cut`, `surface_gaps_or_cracks`, `excessive_cross_slope`, `insufficient_route_width`, `changes_in_level`, `unstable_ground_surface`, `protruding_objects`.

- [ ] **Step 5: Research Signage (6 types)**

ADA sections 703.x, 705 and CBC 11B equivalents for: `missing_tactile_signage`, `missing_directional_signage`, `missing_detectable_warnings`, `missing_exit_signage`, `missing_isa_symbol`, `non_compliant_sign_mounting`.

- [ ] **Step 6: Research Restrooms (8 types)**

ADA sections 603, 604.x and CBC 11B equivalents for: `inaccessible_restroom`, `missing_grab_bars`, `insufficient_stall_size`, `high_mirror`, `insufficient_sink_clearance`, `non_compliant_toilet_height`, `inaccessible_flush_control`, `inaccessible_dispenser_placement`.

- [ ] **Step 7: Research Counters & Services (4 types)**

ADA section 904.x and CBC 11B equivalents for: `inaccessible_counter`, `inaccessible_atm_or_kiosk`, `inaccessible_queue`, `inaccessible_dining_surface`.

- [ ] **Step 8: Research California & SF Specific (6 types)**

CBC path-of-travel rules, CASp program (SB 1608), SF Accessible Business Entrance program, historic building provisions, CBC slope differences, tenant improvement triggers for: `path_of_travel_trigger`, `missing_casp_inspection`, `sf_business_entrance_noncompliant`, `historic_building_no_alt_compliance`, `cbc_stricter_slope_violation`, `tenant_improvement_trigger`.

- [ ] **Step 9: Research California legal risk context**

Research Unruh Civil Rights Act statutory damages, SB 1608 CASp protections, construction-related accessibility standards act (CRASA), and common litigation patterns in SF. This informs the `legal_risk` field for all entries.

---

### Task 2: Build the knowledge base JSON

**Files:**
- Create: `backend/data/ada_knowledge_base.json`
- Reference: `docs/superpowers/specs/2026-03-21-ada-knowledge-base-design.md` (schema)
- Reference: Research output from Task 1

- [ ] **Step 1: Create KB with Entrances & Doors category (8 entries)**

Create `backend/data/ada_knowledge_base.json` with the 8 entrances entries. Each entry follows the full schema from the spec: `id`, `category`, `title`, `description`, `codes` (federal_ada, cbc_title24, sf_local), `severity`, `legal_risk`, `estimated_cost`, `cost_unit`, `cost_note`, `remediation` (summary, steps, contractor_type, permit_required, permit_type, timeline), `tax_credits` (eligible, notes), `detection` (visual_cues, common_contexts, needs_measurement, false_positive_notes).

Use researched code references from Task 1. Synthesize SF-market costs and remediation steps from domain knowledge.

- [ ] **Step 2: Add Ramps & Slopes category (6 entries)**

Append 6 ramps/slopes entries to the KB following the same schema.

- [ ] **Step 3: Add Parking category (5 entries)**

Append 5 parking entries.

- [ ] **Step 4: Add Routes & Pathways category (8 entries)**

Append 8 routes/pathways entries.

- [ ] **Step 5: Add Signage category (6 entries)**

Append 6 signage entries.

- [ ] **Step 6: Add Restrooms category (8 entries)**

Append 8 restroom entries.

- [ ] **Step 7: Add Counters & Services category (4 entries)**

Append 4 counters/services entries.

- [ ] **Step 8: Add California & SF Specific category (6 entries)**

Append 6 California/SF-specific entries.

- [ ] **Step 9: Validate KB structure**

Run:
```bash
cd /Users/jerrison/03-hackatons/01-build-with-ai-sf && python3 -c "
import json
kb = json.load(open('backend/data/ada_knowledge_base.json'))
print(f'{len(kb)} entries')
assert len(kb) >= 51, f'Expected ~56 entries, got {len(kb)}'
required = ['id','category','title','codes','severity','estimated_cost','remediation','detection']
for k, v in kb.items():
    missing = [f for f in required if f not in v]
    assert not missing, f'{k} missing fields: {missing}'
print('Schema validation passed')
"
```

Expected: `51+ entries` and `Schema validation passed`

- [ ] **Step 10: Commit knowledge base**

```bash
git add backend/data/ada_knowledge_base.json
git commit -m "feat: add comprehensive ADA knowledge base with ~56 violation types

Covers federal ADA, CBC Title 24, and SF local codes with SF-market
costs, step-by-step remediation, legal risk, and visual detection cues."
```

---

### Task 3: Write tests for violations.py enrichment layer

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_violations.py`
- Reference: `backend/violations.py` (current implementation)
- Reference: Spec report output schema

- [ ] **Step 1: Create test directory and init file**

```bash
mkdir -p /Users/jerrison/03-hackatons/01-build-with-ai-sf/tests
touch /Users/jerrison/03-hackatons/01-build-with-ai-sf/tests/__init__.py
```

- [ ] **Step 2: Add pytest to dev dependencies**

```bash
cd /Users/jerrison/03-hackatons/01-build-with-ai-sf && uv add --dev pytest
```

- [ ] **Step 3: Write test file**

Create `tests/test_violations.py` with tests for:

```python
import json
from pathlib import Path


def _make_raw_analysis(violations=None):
    """Helper to create a raw Gemini analysis dict."""
    return {
        "violations": violations or [],
        "positive_features": ["Automatic door at main entrance"],
        "overall_risk": "medium",
        "summary": "Some issues found.",
    }


def _make_violation(vtype="missing_ramp", severity="high", confidence=0.9):
    return {
        "violation_type": vtype,
        "description": "Test violation",
        "severity": severity,
        "confidence": confidence,
        "location_in_image": "center",
        "needs_measurement": False,
    }


class TestEnrichViolations:
    def test_empty_violations_returns_report_structure(self):
        """enrich_violations with no violations returns valid report with zero cost."""
        from backend.violations import enrich_violations
        result = enrich_violations(_make_raw_analysis())
        report = result["report"]
        assert report["summary"]["total_violations"] == 0
        assert report["summary"]["total_estimated_cost"] == 0
        assert report["summary"]["overall_risk"] == "none"
        assert "tax_credits" in report
        assert "disclaimer" in report
        assert "next_steps" in report

    def test_single_violation_enriched_with_kb_data(self):
        """A known violation type gets codes, cost, remediation from KB."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([_make_violation("missing_ramp")])
        report = enrich_violations(raw)["report"]
        v = report["violations"][0]
        assert v["violation_type"] == "missing_ramp"
        # Verify KB enrichment populated the codes object with a federal_ada section
        assert v["codes"]["federal_ada"] is not None
        assert "section" in v["codes"]["federal_ada"]
        assert v["estimated_cost"] > 0
        assert "steps" in v["remediation"]
        assert v["category"] == "entrances"

    def test_unknown_violation_type_handled_gracefully(self):
        """Unknown violation types get default/empty enrichment, not errors."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([_make_violation("unknown_type_xyz")])
        report = enrich_violations(raw)["report"]
        v = report["violations"][0]
        assert v["violation_type"] == "unknown_type_xyz"
        assert v["estimated_cost"] == 0

    def test_priority_sorting_high_before_medium(self):
        """High severity violations get lower priority numbers than medium."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([
            _make_violation("round_door_knob", severity="medium", confidence=0.9),
            _make_violation("missing_ramp", severity="high", confidence=0.9),
        ])
        report = enrich_violations(raw)["report"]
        assert report["violations"][0]["severity"] == "high"
        assert report["violations"][0]["priority"] < report["violations"][1]["priority"]

    def test_priority_tiebreak_by_confidence(self):
        """Same severity: higher confidence gets lower priority number."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([
            _make_violation("missing_ramp", severity="high", confidence=0.7),
            _make_violation("no_accessible_entrance", severity="high", confidence=0.95),
        ])
        report = enrich_violations(raw)["report"]
        assert report["violations"][0]["confidence"] > report["violations"][1]["confidence"]

    def test_overall_risk_high_when_any_high_severity(self):
        """overall_risk is 'high' if any violation is high severity."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([
            _make_violation("round_door_knob", severity="low"),
            _make_violation("missing_ramp", severity="high"),
        ])
        report = enrich_violations(raw)["report"]
        assert report["summary"]["overall_risk"] == "high"

    def test_overall_risk_medium_when_no_high(self):
        """overall_risk is 'medium' when no high but some medium."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([
            _make_violation("round_door_knob", severity="medium"),
        ])
        report = enrich_violations(raw)["report"]
        assert report["summary"]["overall_risk"] == "medium"

    def test_overall_risk_none_when_no_violations(self):
        from backend.violations import enrich_violations
        report = enrich_violations(_make_raw_analysis())["report"]
        assert report["summary"]["overall_risk"] == "none"

    def test_total_cost_sums_all_violations(self):
        """total_estimated_cost is sum of all violation estimated_costs."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([
            _make_violation("missing_ramp"),
            _make_violation("round_door_knob"),
        ])
        report = enrich_violations(raw)["report"]
        expected = sum(v["estimated_cost"] for v in report["violations"])
        assert report["summary"]["total_estimated_cost"] == expected

    def test_headline_generated(self):
        """headline is a non-empty template-generated string."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([_make_violation("missing_ramp")])
        report = enrich_violations(raw)["report"]
        assert len(report["summary"]["headline"]) > 0
        assert "access barrier" in report["summary"]["headline"].lower()

    def test_by_severity_counts(self):
        """by_severity correctly counts violations per severity level."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis([
            _make_violation("missing_ramp", severity="high"),
            _make_violation("round_door_knob", severity="medium"),
            _make_violation("missing_tactile_signage", severity="low"),
        ])
        report = enrich_violations(raw)["report"]
        assert report["summary"]["by_severity"] == {"high": 1, "medium": 1, "low": 1}

    def test_location_defaults_to_empty(self):
        """location fields default to empty strings when not provided."""
        from backend.violations import enrich_violations
        report = enrich_violations(_make_raw_analysis())["report"]
        assert report["location"]["address"] == ""
        assert report["location"]["type"] == ""

    def test_location_populated_when_provided(self):
        """location is populated when caller passes it."""
        from backend.violations import enrich_violations
        raw = _make_raw_analysis()
        report = enrich_violations(raw, address="123 Market St", location_type="commercial")["report"]
        assert report["location"]["address"] == "123 Market St"
        assert report["location"]["type"] == "commercial"
```

- [ ] **Step 4: Run tests — expect all to fail**

Run: `cd /Users/jerrison/03-hackatons/01-build-with-ai-sf && uv run pytest tests/test_violations.py -v`

Expected: All 13 tests FAIL (violations.py hasn't been rewritten yet).

- [ ] **Step 5: Commit test file**

```bash
git add tests/ && git commit -m "test: add tests for violations enrichment layer"
```

---

### Task 4: Rewrite violations.py

**Files:**
- Modify: `backend/violations.py`
- Reference: `backend/data/ada_knowledge_base.json` (from Task 2)
- Test: `tests/test_violations.py` (from Task 3)

- [ ] **Step 1: Rewrite violations.py**

Replace the contents of `backend/violations.py` with:

```python
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

_kb = None


def _load_kb():
    global _kb
    if _kb is None:
        with open(DATA_DIR / "ada_knowledge_base.json") as f:
            _kb = json.load(f)
    return _kb


SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}

TAX_CREDITS = [
    {
        "name": "Federal Disabled Access Credit",
        "form": "IRS 8826",
        "max_amount": 5000,
        "eligibility": "Small businesses with <$1M revenue or <30 employees",
    },
    {
        "name": "Federal Barrier Removal Deduction",
        "section": "IRC 190",
        "max_amount": 15000,
        "eligibility": "Any business",
    },
    {
        "name": "CA CASp Inspection Tax Credit",
        "max_amount": 250,
        "eligibility": "After qualified CASp inspection",
    },
]

NEXT_STEPS = [
    "Schedule a CASp inspection for legal protection under SB 1608",
    "Address high-severity violations first — highest legal exposure",
    "Contact SF Mayor's Office on Disability for technical assistance",
    "Small businesses: file IRS Form 8826 for up to $5,000 in access credits",
]

DISCLAIMER = (
    "This is an AI-powered pre-screening tool. A Certified Access Specialist (CASp) "
    "or ADA consultant should verify findings before remediation. This report does not "
    "constitute legal advice. Cost estimates reflect SF market rates and are approximate."
)


def _compute_overall_risk(violations):
    severities = {v.get("severity") for v in violations}
    if "high" in severities:
        return "high"
    if "medium" in severities:
        return "medium"
    if "low" in severities:
        return "low"
    return "none"


def _generate_headline(violations):
    if not violations:
        return "No accessibility violations detected"
    by_sev = {}
    categories = set()
    for v in violations:
        sev = v.get("severity", "low")
        by_sev[sev] = by_sev.get(sev, 0) + 1
        categories.add(v.get("category", "general"))
    top_sev = "critical" if "high" in by_sev else "moderate" if "medium" in by_sev else "minor"
    count = by_sev.get("high", by_sev.get("medium", by_sev.get("low", 0)))
    cat_str = " and ".join(sorted(categories)[:2])
    return f"{count} {top_sev} access barrier(s) found — {cat_str} require attention"


def _sort_key(violation):
    sev = SEVERITY_ORDER.get(violation.get("severity", "low"), 2)
    conf = -(violation.get("confidence", 0))
    cost = violation.get("estimated_cost", 0)
    return (sev, conf, cost)


def enrich_violations(analysis, address="", location_type=""):
    """Take raw Gemini analysis and enrich with KB data, produce report payload."""
    kb = _load_kb()
    enriched_violations = []
    total_cost = 0

    for violation in analysis.get("violations", []):
        vtype = violation["violation_type"]
        entry = kb.get(vtype, {})

        enriched = {
            **violation,
            "category": entry.get("category", "general"),
            "title": entry.get("title", violation.get("description", vtype)),
            "codes": entry.get("codes", {"federal_ada": None, "cbc_title24": None, "sf_local": None}),
            "legal_risk": entry.get("legal_risk", ""),
            "estimated_cost": entry.get("estimated_cost", 0),
            "cost_unit": entry.get("cost_unit", ""),
            "remediation": entry.get("remediation", {"summary": "", "steps": []}),
        }
        enriched_violations.append(enriched)
        total_cost += entry.get("estimated_cost", 0)

    # Sort AFTER enrichment — _sort_key reads estimated_cost which is set during enrichment above
    enriched_violations.sort(key=_sort_key)
    for i, v in enumerate(enriched_violations, 1):
        v["priority"] = i

    by_severity = {"high": 0, "medium": 0, "low": 0}
    for v in enriched_violations:
        sev = v.get("severity", "low")
        if sev in by_severity:
            by_severity[sev] += 1

    return {
        "report": {
            "id": str(uuid.uuid4()),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "location": {
                "address": address,
                "type": location_type,
            },
            "summary": {
                "total_violations": len(enriched_violations),
                "by_severity": by_severity,
                "total_estimated_cost": total_cost,
                "overall_risk": _compute_overall_risk(enriched_violations),
                "headline": _generate_headline(enriched_violations),
            },
            "violations": enriched_violations,
            "tax_credits": TAX_CREDITS,
            "next_steps": NEXT_STEPS,
            "disclaimer": DISCLAIMER,
        }
    }
```

- [ ] **Step 2: Run tests — expect all to pass**

Run: `cd /Users/jerrison/03-hackatons/01-build-with-ai-sf && uv run pytest tests/test_violations.py -v`

Expected: All 13 tests PASS.

- [ ] **Step 3: Commit**

```bash
git add backend/violations.py && git commit -m "feat: rewrite violations.py for new KB schema and report output format"
```

---

### Task 5: Write tests for gemini_client.py prompt builder

**Depends on:** Task 2 (KB file must exist — `gemini_client.py` loads KB at import time, so importing the module will fail with `FileNotFoundError` if KB doesn't exist)

**Files:**
- Create: `tests/test_gemini_client.py`
- Reference: `backend/gemini_client.py` (current)
- Reference: `backend/data/ada_knowledge_base.json`

- [ ] **Step 1: Write test file**

Create `tests/test_gemini_client.py`:

```python
class TestBuildPrompt:
    def test_prompt_contains_all_violation_types(self):
        """The built prompt includes all violation type IDs from the KB."""
        import json
        from backend.gemini_client import build_prompt
        from pathlib import Path
        kb_path = Path(__file__).parent.parent / "backend" / "data" / "ada_knowledge_base.json"
        with open(kb_path) as f:
            kb = json.load(f)
        prompt = build_prompt()
        for vtype in kb:
            assert vtype in prompt, f"Violation type '{vtype}' not found in prompt"

    def test_prompt_contains_visual_cues(self):
        """The prompt includes visual cue text from at least some KB entries."""
        from backend.gemini_client import build_prompt
        prompt = build_prompt()
        # Check a known visual cue from missing_ramp
        assert "Steps at entrance with no adjacent ramp" in prompt or "steps" in prompt.lower()

    def test_prompt_specifies_json_output_format(self):
        """The prompt instructs Gemini to return JSON."""
        from backend.gemini_client import build_prompt
        prompt = build_prompt()
        assert "JSON" in prompt
        assert "violation_type" in prompt
        assert "severity" in prompt
        assert "confidence" in prompt

    def test_prompt_includes_severity_guide(self):
        """The prompt includes the severity guide."""
        from backend.gemini_client import build_prompt
        prompt = build_prompt()
        assert "high" in prompt.lower()
        assert "medium" in prompt.lower()
        assert "low" in prompt.lower()

    def test_analyze_image_direct_uses_built_prompt(self):
        """analyze_image_direct uses the dynamically built prompt, not hardcoded."""
        from backend.gemini_client import ANALYSIS_PROMPT
        # After rewrite, ANALYSIS_PROMPT should contain more than 18 types
        assert "missing_automatic_door" in ANALYSIS_PROMPT
        assert "insufficient_door_clearance" in ANALYSIS_PROMPT
```

- [ ] **Step 2: Run tests — expect failures**

Run: `cd /Users/jerrison/03-hackatons/01-build-with-ai-sf && uv run pytest tests/test_gemini_client.py -v`

Expected: FAIL (build_prompt doesn't exist yet, prompt is still hardcoded).

- [ ] **Step 3: Commit**

```bash
git add tests/test_gemini_client.py && git commit -m "test: add tests for dynamic prompt building in gemini_client"
```

---

### Task 6: Rewrite gemini_client.py

**Files:**
- Modify: `backend/gemini_client.py`
- Reference: `backend/data/ada_knowledge_base.json`
- Test: `tests/test_gemini_client.py`

- [ ] **Step 1: Rewrite gemini_client.py**

Replace the contents of `backend/gemini_client.py` with:

```python
"""
Gemini Vision analysis for ADA compliance.

This module provides two execution paths:
1. Via RocketRide pipeline (primary) - called through the pipeline engine
2. Direct Gemini API (fallback) - for testing without RocketRide running

The prompt is dynamically built from the knowledge base at import time,
so it stays in sync with the violation types defined in ada_knowledge_base.json.
"""

import json
from pathlib import Path
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig

DATA_DIR = Path(__file__).parent / "data"


def _load_kb():
    with open(DATA_DIR / "ada_knowledge_base.json") as f:
        return json.load(f)


def build_prompt():
    """Build the analysis prompt dynamically from the knowledge base."""
    kb = _load_kb()

    # Group violations by category
    categories = {}
    for vtype, entry in kb.items():
        cat = entry.get("category", "general")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((vtype, entry))

    # Build violation reference section
    violation_ref = []
    for cat, entries in sorted(categories.items()):
        cat_title = cat.replace("_", " ").title()
        violation_ref.append(f"\n### {cat_title}")
        for vtype, entry in entries:
            cues = entry.get("detection", {}).get("visual_cues", [])
            cues_str = "; ".join(cues) if cues else "Visual inspection required"
            violation_ref.append(f"- `{vtype}`: {entry.get('title', vtype)} — Look for: {cues_str}")

    violation_section = "\n".join(violation_ref)
    all_types = ", ".join(sorted(kb.keys()))

    return f"""You are an expert ADA (Americans with Disabilities Act) compliance auditor specializing in California and San Francisco requirements. You are analyzing a photo of a building, facility, or public space.

Analyze this image for potential ADA accessibility violations. For each violation you identify:

1. Only report issues you can VISUALLY CONFIRM in the image
2. Be specific about what you observe
3. Note items that would need physical measurement to fully verify
4. Consider both federal ADA and California Building Code (CBC Title 24) requirements

## Violation Types Reference
{violation_section}

## Output Format

Return your analysis as a JSON object with this exact structure:
{{
  "violations": [
    {{
      "violation_type": "<one of: {all_types}>",
      "description": "<what you observe in the image>",
      "severity": "<high, medium, or low>",
      "confidence": <0.0 to 1.0>,
      "location_in_image": "<where in the image this issue appears>",
      "needs_measurement": <true or false>
    }}
  ],
  "positive_features": ["<list any accessibility features that ARE present and compliant>"],
  "summary": "<2-3 sentence summary of findings>"
}}

## Severity Guide
- high: Prevents access entirely (e.g., step-only entrance, no ramp, no accessible restroom)
- medium: Creates difficulty or safety risk (e.g., missing handrails, round knobs, steep ramp)
- low: Minor non-compliance or cosmetic (e.g., faded striping, missing signage, sign mounting height)

IMPORTANT: Return ONLY the JSON object, no markdown formatting or extra text."""


# Build prompt once at module load time
ANALYSIS_PROMPT = build_prompt()


def analyze_image_direct(image_bytes: bytes, mime_type: str) -> dict:
    """Direct Gemini API call (fallback when RocketRide engine is not running)."""
    model = GenerativeModel("gemini-2.0-flash")
    image_part = Part.from_data(data=image_bytes, mime_type=mime_type)

    response = model.generate_content(
        [image_part, ANALYSIS_PROMPT],
        generation_config=GenerationConfig(
            temperature=0.2,
            max_output_tokens=8192,
            response_mime_type="application/json",
        ),
    )

    return json.loads(response.text)
```

Note: `max_output_tokens` increased to 8192 to handle potentially longer responses with more violation types.

- [ ] **Step 2: Run tests — expect all to pass**

Run: `cd /Users/jerrison/03-hackatons/01-build-with-ai-sf && uv run pytest tests/test_gemini_client.py -v`

Expected: All 5 tests PASS.

- [ ] **Step 3: Commit**

```bash
git add backend/gemini_client.py && git commit -m "feat: rewrite gemini_client with dynamic prompt from knowledge base"
```

---

### Task 7: Update main.py for new response shape

**Files:**
- Modify: `backend/main.py:38-56`

**WARNING:** The response shape changes from a flat dict to `{"report": {...}}`. The frontend (`frontend/app.js`) currently consumes the old shape and WILL BREAK after this change. Frontend updates are out of scope for this plan — a follow-up task is required.

- [ ] **Step 1: Verify the analyze endpoint works with new violations.py**

The `enrich_violations` function signature now accepts optional `address` and `location_type` kwargs. The current call `enrich_violations(raw_analysis)` works unchanged since both new params have defaults.

The return value is now `{"report": {...}}` instead of a flat dict. No code change needed in `main.py` since FastAPI serializes whatever `enrich_violations` returns.

The `address` and `location_type` parameters will be threaded through from the API in a future task when the iOS app sends them. For now, they default to empty strings.

- [ ] **Step 2: Run full test suite**

Run: `cd /Users/jerrison/03-hackatons/01-build-with-ai-sf && uv run pytest tests/ -v`

Expected: All tests PASS.

- [ ] **Step 3: Commit if any changes were needed**

```bash
git add backend/main.py && git commit -m "chore: verify main.py compatible with new violations output"
```

---

### Task 8: Delete old data files

**Files:**
- Delete: `backend/data/ada_codes.json`
- Delete: `backend/data/cost_estimates.json`

- [ ] **Step 1: Verify no other code references old files**

Search the codebase for references to `ada_codes.json` and `cost_estimates.json`:

Run: `grep -r "ada_codes\|cost_estimates" /Users/jerrison/03-hackatons/01-build-with-ai-sf/backend/ /Users/jerrison/03-hackatons/01-build-with-ai-sf/ARCHITECTURE.md /Users/jerrison/03-hackatons/01-build-with-ai-sf/CLAUDE.md`

Expected: Only references in ARCHITECTURE.md and CLAUDE.md (updated in Task 9), none in Python code.

- [ ] **Step 2: Delete old data files**

```bash
git rm backend/data/ada_codes.json backend/data/cost_estimates.json
git commit -m "chore: remove old ada_codes.json and cost_estimates.json (superseded by KB)"
```

- [ ] **Step 3: Run tests to verify nothing breaks**

Run: `cd /Users/jerrison/03-hackatons/01-build-with-ai-sf && uv run pytest tests/ -v`

Expected: All tests PASS.

---

### Task 9: Update ARCHITECTURE.md and CLAUDE.md

**Files:**
- Modify: `ARCHITECTURE.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update ARCHITECTURE.md**

Changes needed:
- Data flow: replace `ada_codes.json` + `cost_estimates.json` references with `ada_knowledge_base.json`
- Directory structure: replace the two data files with single KB file
- Key Components table: update `violations.py` description
- Key Components table: update `gemini_client.py` description
- Violation Types section: update count from 18 to ~56, list categories instead of individual types

- [ ] **Step 2: Update CLAUDE.md**

Changes needed in Key Paths section:
- Replace `ADA reference data: backend/data/ada_codes.json` and `Cost data: backend/data/cost_estimates.json` with `ADA knowledge base: backend/data/ada_knowledge_base.json`
- Update Architecture Rules to mention ~56 violation types

- [ ] **Step 3: Commit**

```bash
git add ARCHITECTURE.md CLAUDE.md && git commit -m "docs: update architecture and project docs for new knowledge base"
```

---

### Task 10: Integration smoke test

**Files:**
- Reference: All modified files

- [ ] **Step 1: Run full test suite**

Run: `cd /Users/jerrison/03-hackatons/01-build-with-ai-sf && uv run pytest tests/ -v`

Expected: All tests PASS.

- [ ] **Step 2: Validate KB loads correctly at import time**

Run: `cd /Users/jerrison/03-hackatons/01-build-with-ai-sf/backend && uv run python -c "from violations import enrich_violations; from gemini_client import ANALYSIS_PROMPT; print(f'Prompt length: {len(ANALYSIS_PROMPT)} chars'); print(f'KB loaded successfully'); r = enrich_violations({'violations': [{'violation_type': 'missing_ramp', 'description': 'test', 'severity': 'high', 'confidence': 0.9, 'location_in_image': 'center', 'needs_measurement': False}]}); print(f'Report has {r[\"report\"][\"summary\"][\"total_violations\"]} violations, cost: ${r[\"report\"][\"summary\"][\"total_estimated_cost\"]}')"`

Expected: KB loads, prompt builds, enrichment works with real KB data.

- [ ] **Step 3: Verify all violation types are covered end-to-end**

Run: `cd /Users/jerrison/03-hackatons/01-build-with-ai-sf/backend && uv run python -c "
import json
from gemini_client import ANALYSIS_PROMPT
from violations import _load_kb
kb = _load_kb()
missing = [k for k in kb if k not in ANALYSIS_PROMPT]
print(f'KB entries: {len(kb)}')
print(f'Missing from prompt: {missing}')
assert not missing, f'These KB entries are missing from the prompt: {missing}'
print('All violation types present in prompt')
"`

Expected: `All violation types present in prompt`

- [ ] **Step 4: Final commit if any fixes were needed**

```bash
git add -A && git commit -m "fix: integration fixes from smoke testing"
```
