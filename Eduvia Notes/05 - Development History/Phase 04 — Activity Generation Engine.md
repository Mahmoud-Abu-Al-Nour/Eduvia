# Phase 04 — Activity Generation Engine

## Objective
Design and implement the structured AI Activity Generation Engine. The engine translates academic curriculum objectives into individualized, multi-modal, accessible educational activities tailored to the learner's cognitive profile, while guaranteeing 100% availability through deterministic fallback generation.

---

## Requirements & Scope
- **5 Activity Modalities**:
  1. `matching`: Key-value concept association with distractors.
  2. `multiple_choice`: Question prompts with distraction-free distractors and authoritative answer indexing.
  3. `ordering`: Sequential arrangement (chronological, quantitative, procedural).
  4. `visual_identification`: Image/icon identification with accessible text cues.
  5. `drag_drop`: Categorical spatial sorting.
- **Strict Validation Contracts**: Pydantic schemas with `extra="forbid"`, regex constraints, and non-empty content validation (`ActivityContent`, `MatchingActivityContent`, etc.).
- **Context-Aware Prompts**: Prompt builders incorporating curriculum standards, objective criteria, learner modality preferences, sensory constraints, and teacher overrides.
- **AI Orchestration**: Flexible LLM provider abstraction supporting Google Gemini with temperature control and structured JSON schema output enforcement.
- **The Zero-Strand Guarantee**: Mandatory deterministic fallback generation (`fallbacks.py`) intercepting any LLM exception, timeout, rate limit, or invalid JSON payload to produce an immediate, valid, objective-aligned activity.
- **REST API**: `POST /api/v1/activities/generate` endpoint with authenticated teacher/admin access.
- **Development Server**: Complete in-memory activity generator in `dev_server.py`.

---

## Key Architecture & Components
* **Schemas**: `backend/app/activities/schemas.py` (Modality Pydantic models, `ActivityGenerationRequest`, `ActivityGenerationResponse`)
* **Fallbacks**: `backend/app/activities/fallbacks.py` (Deterministic activity generator implementing Zero-Strand Guarantee)
* **Prompts**: `backend/app/ai/generation/prompts.py` (Cognitive Calm prompt templates)
* **Orchestrator**: `backend/app/ai/orchestrator/orchestrator.py` & `backend/app/ai/providers/gemini.py`
* **Service**: `backend/app/activities/service.py` (`ActivityService`)
* **Router**: `backend/app/activities/router.py`

---

## Important Decisions
* **The Zero-Strand Guarantee**: Under no circumstances does an AI failure surface an error to the student. Fallback activities are pre-constructed from curriculum objective templates to ensure seamless instructional continuity.
* **Deprecation Notice Handling**: The `google.generativeai` package deprecation notice was cataloged and explicitly deferred to Phase 9 to maintain stability across foundational phases.

---

## Verification & Testing
* **Test Suite**: 26 unit and integration tests (22 test functions defined in code: 21 standalone functions + 1 function parametrized across 5 modalities) in `backend/tests/test_activities.py` covering:
  * Successful LLM generation.
  * LLM network timeout fallback.
  * Invalid JSON response fallback.
  * Valid JSON with invalid schema fallback.
  * Missing required fields fallback.
  * Unsupported activity type handling.
  * Teacher constraint application.
  * Multi-lingual prompt construction.
* **Full Backend Regression**: **80/80 tests passed** (26 Phase 4 + 54 previous baseline).
* **Frontend Build**: Vite production build succeeded cleanly.


---

## Gate Status
# **PHASE 4 — LOCKED**

---

## Navigation & Related Notes
* Back to: [[05 - Development History/Eduvia Development History|Eduvia Development History]]
* Archived Report: [[05 - Development History/Reports/Phase 04 Report|Phase 04 Implementation Report]]
* Architecture: [[03 - AI & Adaptive Learning/Activity Generation|Activity Generation Architecture]]
* Previous Phase: [[05 - Development History/Phase 03 — Learner Profile|Phase 03 — Learner Profile]]
* Next Phase: [[05 - Development History/Phase 05 — Learner Experience & Activity Interaction|Phase 05 — Learner Experience & Activity Interaction]]

