# ADA Compliance Auditor — iOS + Web PWA Design Spec

## Overview

Extend the existing ADA Compliance Auditor into a cross-platform (PWA + iOS) "snap and report" tool. Users photograph a building or public space, receive a professional PDF audit report evaluating against California Building Code Title 24 and federal ADA standards, and keep a browsable history of past reports on-device.

**MVP scope:** California only. Single photo analysis with AI-guided follow-up suggestions. No user auth — device-based sessions with local storage.

## Architecture

Enhance the existing FastAPI monolith. No new services or infrastructure.

```
iOS (Swift WebView)  ←→  Web (PWA)
         ↓                    ↓
      FastAPI Backend (extended)
         ↓
┌──────────────────────────────────────┐
│  Multi-Pass Gemini  │  CA Enrichment │
│  SQLite Sessions    │  PDF Generator │
└──────────────────────────────────────┘
```

Both clients hit the same backend. The iOS app is a thin WKWebView wrapper (~200 lines of Swift) that adds native PDF save and share sheet. The web app is a PWA with offline history browsing.

## 1. Multi-Pass Gemini Analysis Pipeline

Replaces the current single-call Gemini analysis with a 3-pass pipeline for improved accuracy.

### Pass 1 — Scene Classification (~1s)

- **Input:** Raw photo
- **Output:** Space type enum: `entrance`, `parking_lot`, `interior`, `restroom`, `sidewalk_path`, `counter_service_area`
- **Purpose:** Narrows the violation checklist for Pass 2 so it evaluates only relevant violations

### Pass 2 — Violation Detection (~3-4s)

- **Input:** Original photo + scene type from Pass 1
- **Prompt:** Scoped to violations relevant to the detected space type. Includes measurement heuristics (e.g., "a standard door is ~80in tall — use as scale reference") and California-specific thresholds from CBC Title 24.
- **Output:** Structured JSON per violation:
  - Violation type (from the supported set)
  - Severity: HIGH / MEDIUM / LOW
  - Confidence score (0.0–1.0)
  - Location description (e.g., "front entrance, left side")
  - Reasoning (e.g., "no ramp visible adjacent to the 3-step entrance")

### Pass 3 — Consistency Check (~1-2s)

- **Input:** Original photo + Pass 2 results
- **Output:** Refined violations (contradictions removed, confidence adjusted) + follow-up photo suggestions (e.g., "photograph the restroom for a more complete audit")

**Total estimated latency:** ~5-7 seconds. Frontend shows progress per pass.

## 2. California ADA Enrichment Layer

California is always on — no geolocation, no toggle. Every report evaluates against both standards.

### Data

**New file: `backend/data/california_codes.json`**
- Maps each of the 18 violation types to CBC Title 24 equivalents
- Includes stricter California thresholds where they differ (e.g., CA requires 1:10 max ramp slope for existing buildings vs federal 1:12 for new)
- Adds California-only requirements not in federal ADA (e.g., path-of-travel spending triggers, CASp references)

### Integration

- Pass 2 Gemini prompt is augmented with California-specific thresholds
- Enrichment layer maps each violation to both federal ADA section and CBC Title 24 section
- Report notes which standard is stricter for each violation

## 3. PDF Report Generation

Generated server-side using a Python PDF library. Styled like a professional CASp inspection report.

### Structure

**Page 1 — Cover**
- "ADA Compliance Audit Report"
- Photo thumbnail
- Location label (user-entered)
- Date of audit
- Overall risk level badge (HIGH / MEDIUM / LOW)

**Page 2 — Executive Summary**
- Space type identified
- Total violations (confirmed vs potential)
- "Evaluated against California Building Code Title 24 and federal ADA standards"
- Total estimated remediation cost range
- Remediation priority ranking

**Pages 3+ — Violation Details (one section per violation)**
- Violation name and description
- Severity + confidence score
- Location in photo (described by Gemini)
- Federal ADA section reference
- CBC Title 24 reference (stricter threshold noted)
- Specific remediation recommendation
- Cost estimate (low–high range)

**Final Page — Summary**
- Cost matrix table: all violations with cost ranges
- Total estimated remediation cost
- Positive accessibility features noted
- Disclaimer: "This AI-generated report is not a substitute for a certified CASp inspection"
- Follow-up photo suggestions from Pass 3

## 4. Frontend — PWA + Camera Experience

Mobile-first vanilla JS + Tailwind. Existing dark theme carries over.

### Camera Flow

1. User taps "Scan" — opens device camera (`getUserMedia` or file input fallback)
2. Subtle overlay hint: "Capture the full entrance including ground level"
3. Photo preview → "Analyze" button
4. Progress steps visible: "Classifying space... Detecting violations... Verifying results..."
5. Report renders live → "Download PDF" button
6. Follow-up suggestion from Gemini (e.g., "For a more complete audit, photograph the parking area") → user can snap another photo for a separate report

### History Screen

- Card list of past reports: photo thumbnail, date, location label, risk badge, violation count
- Tap card → view full report or re-download PDF
- Sorted by date, filterable by risk level
- Stored in IndexedDB

### Navigation

Bottom nav bar: **Scan** | **History**

### PWA Features

- Service worker for offline history browsing
- Web app manifest for "Add to Home Screen"
- Mobile-first responsive, works on desktop

## 5. Data Model

### Report Metadata (IndexedDB on device)

```json
{
  "id": "uuid",
  "sessionId": "device-generated-id",
  "locationLabel": "123 Main St, Oakland",
  "photoThumbnail": "base64-compressed-preview",
  "date": "2026-03-21T14:30:00Z",
  "spaceType": "entrance",
  "riskLevel": "HIGH",
  "violationCount": 5,
  "confirmedCount": 3,
  "potentialCount": 2,
  "totalCostLow": 12000,
  "totalCostHigh": 35000,
  "pdfBlob": "Blob",
  "followUpSuggestions": ["Photograph the parking area"]
}
```

### Backend Response (`POST /api/analyze`)

- `report`: Full structured JSON (violations, costs, ADA + CBC references)
- `pdf_url`: Temporary download link for the generated PDF
- `follow_up_suggestions`: Array of next-photo prompts from Pass 3
- `space_type`: Scene classification result
- `summary`: Executive summary text

**No server-side persistence.** Backend generates the report and PDF, returns them, forgets. All storage is client-side.

## 6. iOS Swift WebView Wrapper

Thin native shell for App Store distribution.

### Responsibilities

- `WKWebView` loading the PWA
- Intercepts PDF download links → saves to app Documents directory → native share sheet (AirDrop, email, Messages, Files)
- Camera access via `getUserMedia` (WKWebView supports this natively)
- IndexedDB persists in WebView's app sandbox

### Does NOT include

- No native UI beyond WebView
- No custom camera view
- No push notifications
- No separate backend communication

### File Structure

```
ios/
├── ADAauditor/
│   ├── ADAauditorApp.swift      # App entry
│   ├── WebView.swift            # WKWebView + navigation delegate
│   ├── ShareHandler.swift       # PDF save + share sheet bridge
│   └── Info.plist               # Camera permission description
└── ADAauditor.xcodeproj
```

~200 lines of Swift total.

## 7. Backend Changes Summary

| Component | Change |
|-----------|--------|
| `backend/gemini_client.py` | Replace single call with 3-pass pipeline (scene classify → scoped violation detect → consistency check) |
| `backend/violations.py` | Add California enrichment from `california_codes.json`, return both ADA + CBC references |
| `backend/main.py` | Add PDF generation endpoint, update `/api/analyze` response shape, add progress streaming |
| `backend/pdf_generator.py` | **New.** Generates styled PDF reports server-side |
| `backend/data/california_codes.json` | **New.** CBC Title 24 mappings for all 18 violation types |
| `frontend/app.js` | Rewrite for camera flow, history screen, IndexedDB storage, PDF download |
| `frontend/index.html` | Mobile-first layout with bottom nav (Scan / History) |
| `frontend/sw.js` | **New.** Service worker for PWA offline support |
| `frontend/manifest.json` | **New.** Web app manifest |
| `ios/` | **New.** Swift WebView wrapper |

## Dependencies (New)

- PDF generation: `reportlab` or `weasyprint` (Python)
- No new frontend dependencies (vanilla JS, Tailwind CDN)
- Xcode for iOS wrapper build

## Out of Scope (MVP)

- Multi-state support (California only)
- User authentication
- Server-side report storage
- Push notifications
- Custom native camera UI
- Batch photo analysis
- Real-time collaboration/sharing
