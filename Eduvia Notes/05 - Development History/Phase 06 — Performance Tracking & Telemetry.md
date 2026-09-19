# Phase 06 — Performance Tracking & Telemetry

## Objective
Establish the authoritative, relational telemetry store capturing persistent performance events from learner interactions and server-side activity evaluations. Phase 6 captures fine-grained, immutable observational data (response times, hint usage, assistance levels, environmental factors) with strict schema validation and teacher multi-tenant access control.

---

## Requirements & Scope
- **Relational Telemetry Data Models**:
  - `PerformanceEvent`: Immutable event record capturing `learner_id`, `activity_id`, `objective_id`, `activity_type`, `modality`, `teaching_strategy`, `correct`, `score` (0.0–1.0), `response_time_ms`, `hints_used`, `assistance_level` (0–3), `environmental_factors`, `event_data`, and UTC `timestamp`.
  - `ActivityAttempt`: Session tracking record capturing `learner_id`, `activity_id`, `session_id`, `started_at`, `completed_at`, `completed`, and summary `score`.
- **Database Indexing & Migrations**:
  - Alembic migration `b4c5d6e7f8a9` (`create_analytics_tables`).
  - High-performance composite indexes: `(learner_id, timestamp)`, `(activity_id, timestamp)`, `objective_id`, and `activity_type`.
- **Strict Ingestion Contracts**: Pydantic validation forbidding extra fields, asserting bounded scores ($0.0 \le s \le 1.0$), non-negative response latencies, and valid assistance levels (0 to 3).
- **Authoritative Integration Hook**: In `activities/service.py`, `evaluate_submission()` automatically emits a verified `PerformanceEventCreate` record directly to `AnalyticsService` whenever `learner_id` is present in the submission.
- **Teacher Multi-Tenant Isolation**: Server-side access enforcement ensuring teachers can only access telemetry for learners assigned to them (`learner.teacher_id == current_user.id`). Admins retain global visibility.
- **REST Endpoints**:
  - `POST /api/v1/analytics/events`: Ingest performance event (201 Created).
  - `POST /api/v1/analytics/attempts`: Ingest activity attempt (201 Created).
  - `GET /api/v1/analytics/learners/{learner_id}/events`: Retrieve filtered event history (200 OK).
  - `GET /api/v1/analytics/events/{event_id}`: Retrieve single event by ID (200 OK).
- **Client & Dev Support**: `analyticsApi` helper methods in `frontend/src/services/api.ts` and in-memory mock repository in `dev_server.py`.

---

## Key Architecture & Components
* **Models**: `backend/app/analytics/models.py` (`PerformanceEvent`, `ActivityAttempt`)
* **Schemas**: `backend/app/analytics/schemas.py` (`PerformanceEventCreate`, `PerformanceEventRead`, `PerformanceEventQueryFilter`, `ActivityAttemptCreate`, `ActivityAttemptRead`)
* **Service**: `backend/app/analytics/service.py` (`AnalyticsService`)
* **Router**: `backend/app/analytics/router.py`
* **Migration**: `backend/alembic/versions/20260919_0730_b4c5d6e7f8a9_create_analytics_tables.py`
* **Frontend Client**: `frontend/src/services/api.ts` (`analyticsApi`)

---

## Phase Boundary Discipline
Phase 6 strictly confines its responsibility to raw event ingestion and persistence:
* **No Dynamic Aggregation**: Does not compute aggregate accuracy percentages or modality breakdowns (reserved for Phase 7).
* **No Mastery Scoring**: Does not evaluate cumulative objective mastery (reserved for Phase 7).
* **No Adaptive Decisioning**: Does not suggest next activities or adjust learner profiles (reserved for Phase 8).

---

## Verification & Testing
* **Test Coverage**: 17 comprehensive backend tests in `backend/tests/test_analytics.py` verifying:
  * Strict schema rejection of out-of-bound scores and assistance levels.
  * Successful event and attempt relational persistence.
  * Direct telemetry emission from `evaluate_submission()`.
  * Teacher multi-tenant isolation (`403 Forbidden` on unassigned learner queries).
  * Administrator global event retrieval.
  * Complex event filtering by objective, modality, and correctness.
* **Full Backend Regression**: **128/128 tests passed** (17 Phase 6 + 111 previous).
* **Frontend Build**: Vite production build succeeded cleanly.

---

## Gate Status
# **PHASE 6 — LOCKED**

---

## Navigation & Related Notes
* Back to: [[05 - Development History/Eduvia Development History|Eduvia Development History]]
* Archived Report: [[05 - Development History/Reports/Phase 06 Report|Phase 06 Implementation Report]]
* Architecture: [[03 - AI & Adaptive Learning/Learning Analytics|Learning Analytics Architecture]]
* Previous Phase: [[05 - Development History/Phase 05 — Learner Experience & Activity Interaction|Phase 05 — Learner Experience & Activity Interaction]]
* Next Phase: [[05 - Development History/Phase 07 — Learner Analytics & Mastery Tracking|Phase 07 — Learner Analytics & Mastery Tracking]]

