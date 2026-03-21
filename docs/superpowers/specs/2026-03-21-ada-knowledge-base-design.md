# ADA Compliance Knowledge Base — Design Spec

**Date:** 2026-03-21
**Project:** ADA Compliance Auditor (Build with AI - SF Hackathon)
**Author:** Jerrison + Claude

## Problem

The current system has 18 violation types with basic federal ADA references and generic cost ranges. This is insufficient for a San Francisco audience because:

1. California Building Code (CBC) Title 24 is often stricter than federal ADA
2. SF has local accessibility ordinances and programs not captured
3. Cost estimates don't reflect SF market rates
4. Remediation guidance is a single sentence — not actionable
5. No legal risk context (Unruh Civil Rights Act exposure)
6. No visual detection guidance for the AI model

## Solution

Build a comprehensive, single-file knowledge base (`ada_knowledge_base.json`) covering ~55 violation types across federal ADA, CBC Title 24, and SF local codes. Each entry includes codes, SF-market costs, step-by-step remediation, legal risk, and visual detection cues for AI image analysis.

## Team Context

- **Teammate:** Builds image capture (iOS) and image processing → violation identification
- **Jerrison:** Builds the knowledge base + enrichment layer that maps identified violations to structured report data
- **Interface:** Teammate sends an array of violation type strings (with confidence/location); Jerrison's layer enriches them from the knowledge base and outputs a report-ready JSON payload

## Data Flow

```
Teammate's pipeline:
  Photo → Image processing → Violation identification
                                        ↓
Jerrison's layer:
  Identified violations (list of violation_type strings)
    → Query ada_knowledge_base.json by violation_type keys
    → Assemble structured report payload
                                        ↓
Output consumers:
  → iOS app (JSON — quick summary view)
  → HTML/PDF report generator (JSON — full detail)
```

## Knowledge Base Schema

Single file: `backend/data/ada_knowledge_base.json`

Each violation entry:

```json
{
  "missing_ramp": {
    "id": "missing_ramp",
    "category": "entrances",
    "title": "Missing Wheelchair Ramp",
    "description": "Entrance lacks an accessible ramp for wheelchair users",

    "codes": {
      "federal_ada": {
        "section": "405",
        "title": "Ramps",
        "requirement": "An accessible route with a ramp must be provided where there is a change in level greater than 1/2 inch. Running slope max 1:12, min clear width 36 inches."
      },
      "cbc_title24": {
        "section": "11B-405.2",
        "title": "Ramps",
        "requirement": "CBC allows 1:10 slope for existing buildings (stricter new construction requirements). Handrails required on both sides for rises > 6 inches."
      },
      "sf_local": {
        "ordinance": "SF Building Code Chapter 11B",
        "note": "SF DBI enforces CBC Title 24 with local amendments. Accessible Business Entrance program may apply."
      }
    },

    "severity": "high",
    "legal_risk": "Lawsuit exposure under Unruh Civil Rights Act — California allows statutory damages of $4,000+ per visit. High-frequency litigation target in SF.",

    "estimated_cost": 12000,
    "cost_unit": "per ramp",
    "cost_note": "SF market rate, includes permit fees. Concrete permanent ramp. Modular/aluminum alternatives may be lower.",

    "remediation": {
      "summary": "Install code-compliant ramp with handrails",
      "steps": [
        "1. Engage licensed general contractor experienced with ADA work",
        "2. Pull SF DBI building permit (over-the-counter for simple ramps, full permit for structural)",
        "3. Design ramp to CBC 11B-405 specs (1:12 slope max, 36-inch min width, landings at top/bottom)",
        "4. Install handrails on both sides (34-38 inches height, 12-inch extensions)",
        "5. Add detectable warning surface at bottom if adjacent to vehicular way",
        "6. Schedule DBI inspection for permit sign-off"
      ],
      "contractor_type": "Licensed general contractor",
      "permit_required": true,
      "permit_type": "SF DBI building permit",
      "timeline": "2-4 weeks"
    },

    "tax_credits": {
      "eligible": true,
      "notes": "Likely qualifies for Federal Disabled Access Credit (IRS 8826) and Federal Barrier Removal Deduction (IRC 190)"
    },

    "detection": {
      "visual_cues": [
        "Steps at entrance with no adjacent ramp",
        "Raised entrance platform with no sloped approach",
        "Single step up to doorway without ramp alternative"
      ],
      "common_contexts": ["building entrance", "side entrance", "rear entrance"],
      "needs_measurement": false,
      "false_positive_notes": "Temporary construction barriers may obscure an existing ramp. A portable ramp stored inside is not compliant — must be deployed."
    }
  }
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique violation identifier, used as the JSON key |
| `category` | string | One of 8 categories (see below) |
| `title` | string | Human-readable violation name |
| `description` | string | One-line description of the violation |
| `codes.federal_ada` | object/null | ADA Standards section, title, requirement text |
| `codes.cbc_title24` | object/null | California Building Code section, title, requirement text |
| `codes.sf_local` | object/null | SF-specific ordinance or program reference |
| `severity` | string | `high`, `medium`, or `low` |
| `legal_risk` | string | California-specific legal exposure description |
| `estimated_cost` | number | Single SF-market cost estimate in USD |
| `cost_unit` | string | What the cost applies to (e.g., "per ramp", "per door") |
| `cost_note` | string | Context for the cost figure |
| `remediation.summary` | string | One-line fix description |
| `remediation.steps` | array | Ordered remediation steps |
| `remediation.contractor_type` | string | Who to hire |
| `remediation.permit_required` | boolean | Whether SF permits are needed |
| `remediation.permit_type` | string | Which permit type |
| `remediation.timeline` | string | Estimated completion time |
| `tax_credits.eligible` | boolean | Whether tax credits likely apply |
| `tax_credits.notes` | string | Which credits and conditions |
| `detection.visual_cues` | array | What AI should look for in images |
| `detection.common_contexts` | array | Where this violation typically appears |
| `detection.needs_measurement` | boolean | Whether physical measurement is needed to confirm |
| `detection.false_positive_notes` | string | Common misidentifications to avoid |

## Violation Categories (~55 types)

### 1. Entrances & Doors (8 types)
- `missing_ramp` — No ramp at entrance with level change
- `no_accessible_entrance` — No accessible entrance to building
- `step_only_entrance` — Steps-only entrance, no alternative
- `narrow_doorway` — Door clear width < 32 inches
- `round_door_knob` — Non-compliant door hardware (round knobs)
- `missing_automatic_door` — High-traffic entrance lacks automatic opener
- `insufficient_door_clearance` — Inadequate maneuvering clearance at door
- `excessive_door_force` — Door requires > 5 lbs force to open

### 2. Ramps & Slopes (6 types)
- `steep_ramp` — Ramp slope exceeds 1:12
- `missing_handrail` — Ramp lacks required handrails
- `missing_ramp_landing` — Ramp lacks level landing at top/bottom or at direction change
- `missing_edge_protection` — Ramp lacks edge protection (curbs, rails, or walls)
- `missing_handrail_extensions` — Handrails don't extend 12 inches beyond ramp
- `excessive_ramp_rise` — Single ramp run rise exceeds 30 inches without landing

### 3. Parking (5 types)
- `missing_accessible_parking_sign` — Accessible space lacks ISA signage
- `missing_parking_striping` — Access aisle not properly marked
- `insufficient_accessible_spaces` — Parking lot has too few accessible spaces for total count
- `missing_van_accessible_space` — No van-accessible space (96-inch aisle)
- `damaged_parking_surface` — Accessible route from parking has cracks, potholes, or heaving

### 4. Routes & Pathways (7 types)
- `blocked_accessible_route` — Obstruction in accessible path
- `surface_gaps_or_cracks` — Walking surface has gaps > 1/2 inch or significant cracks
- `excessive_cross_slope` — Cross slope exceeds 1:48
- `insufficient_route_width` — Path width < 36 inches (44 for high-traffic corridors)
- `changes_in_level` — Abrupt level changes > 1/4 inch without ramp or bevel
- `unstable_ground_surface` — Gravel, grass, or loose material on accessible route
- `protruding_objects` — Wall-mounted objects protrude > 4 inches into path (27-80 inch zone)

### 5. Signage (6 types)
- `missing_tactile_signage` — Room/space identification sign lacks raised characters and Braille
- `missing_directional_signage` — No directional signs to accessible features
- `missing_detectable_warnings` — Curb ramp or hazardous area lacks truncated dome surface
- `missing_exit_signage` — Accessible exit route not identified
- `missing_isa_symbol` — Required International Symbol of Accessibility not displayed
- `non_compliant_sign_mounting` — Sign not mounted at correct height or location (48-60 inches, latch side)

### 6. Restrooms (8 types)
- `inaccessible_restroom` — Restroom generally inaccessible (multiple issues)
- `missing_grab_bars` — Toilet lacks required grab bars
- `insufficient_stall_size` — Accessible stall dimensions inadequate (60x60 minimum)
- `high_mirror` — Mirror bottom edge > 40 inches above floor
- `insufficient_sink_clearance` — Sink lacks 27-inch knee clearance or 29-inch clear height
- `non_compliant_toilet_height` — Toilet seat not 17-19 inches above floor
- `inaccessible_flush_control` — Flush control not on open side or not automatic
- `inaccessible_dispenser_placement` — Paper/soap dispensers mounted too high or out of reach

### 7. Counters & Services (4 types)
- `inaccessible_counter` — Service counter > 36 inches high with no lowered section
- `inaccessible_atm_or_kiosk` — Self-service kiosk/ATM not accessible
- `inaccessible_queue` — Queuing area not wheelchair accessible
- `inaccessible_dining_surface` — Dining tables lack wheelchair clearance (27 inch knee, 28-34 inch surface)

### 8. California & SF Specific (6 types)
- `path_of_travel_trigger` — Renovation exceeds CBC path-of-travel spending threshold (20% rule)
- `missing_casp_inspection` — Property lacks CASp inspection (relevant for legal protection)
- `sf_business_entrance_noncompliant` — Fails SF Accessible Business Entrance program requirements
- `historic_building_no_alt_compliance` — Historic building lacks alternative compliance plan
- `cbc_stricter_slope_violation` — Ramp meets federal ADA but fails stricter CBC slope requirements
- `tenant_improvement_trigger` — Tenant improvement work triggers CBC accessibility upgrade requirements

## Report Output Schema

The enrichment layer (`violations.py`) produces this JSON payload:

```json
{
  "report": {
    "id": "uuid",
    "generated_at": "ISO-8601 timestamp",
    "location": {
      "address": "",
      "type": "commercial"
    },

    "summary": {
      "total_violations": 5,
      "by_severity": { "high": 2, "medium": 2, "low": 1 },
      "total_estimated_cost": 34500,
      "overall_risk": "high",
      "headline": "2 critical access barriers found — entrance and restroom require immediate attention"
    },

    "violations": [
      {
        "violation_type": "missing_ramp",
        "category": "entrances",
        "title": "Missing Wheelchair Ramp",
        "description": "Steps at main entrance with no adjacent ramp",
        "severity": "high",
        "confidence": 0.92,
        "location_in_image": "front entrance, left side",
        "codes": { "...": "..." },
        "legal_risk": "...",
        "estimated_cost": 12000,
        "cost_unit": "per ramp",
        "remediation": { "...": "..." },
        "priority": 1
      }
    ],

    "tax_credits": [
      {
        "name": "Federal Disabled Access Credit",
        "form": "IRS 8826",
        "max_amount": 5000,
        "eligibility": "Small businesses with <$1M revenue or <30 employees"
      },
      {
        "name": "Federal Barrier Removal Deduction",
        "section": "IRC 190",
        "max_amount": 15000,
        "eligibility": "Any business"
      },
      {
        "name": "CA CASp Inspection Tax Credit",
        "max_amount": 250,
        "eligibility": "After qualified CASp inspection"
      }
    ],

    "next_steps": [
      "Schedule a CASp inspection for legal protection under SB 1608",
      "Address high-severity violations first — highest legal exposure",
      "Contact SF Mayor's Office on Disability for technical assistance",
      "Small businesses: file IRS Form 8826 for up to $5,000 in access credits"
    ],

    "disclaimer": "This is an AI-powered pre-screening tool. A Certified Access Specialist (CASp) or ADA consultant should verify findings before remediation. This report does not constitute legal advice. Cost estimates reflect SF market rates and are approximate."
  }
}
```

### Priority Assignment Logic

Violations are auto-sorted by priority:
1. **High severity** violations first (blocks access entirely)
2. Within same severity, higher confidence first
3. Within same severity and confidence, lower cost first (quick wins)

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `backend/data/ada_knowledge_base.json` | **Create** | ~55 violation entries with full schema |
| `backend/violations.py` | **Rewrite** | Load new KB, produce report output schema, priority sorting |
| `backend/gemini_client.py` | **Update** | Dynamic prompt with violation types + visual cues from KB |
| `backend/data/ada_codes.json` | **Delete** | Superseded by knowledge base |
| `backend/data/cost_estimates.json` | **Delete** | Superseded by knowledge base |

## Research Approach

- **Code references** (federal ADA, CBC Title 24, SF local): Web research for accuracy
- **Cost estimates**: Domain knowledge synthesized for SF market rates
- **Remediation steps**: Domain knowledge — practical, contractor-oriented guidance
- **Visual cues**: Domain knowledge — what's identifiable in photos
- **Legal risk**: Research California Unruh Civil Rights Act and SB 1608 implications

## Constraints

- Knowledge base must be a single JSON file loadable by `violations.py`
- Violation type IDs must be stable strings (teammate's pipeline will reference them)
- Output JSON must serve both iOS app (summary view) and HTML/PDF (full report)
- Estimated costs are single numbers, not ranges
- All costs reflect SF market rates
