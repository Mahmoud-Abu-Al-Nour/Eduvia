# Eduvia Testing & Verification

> **Layered Quality Assurance, Deterministic Verification, and End-to-End Regression Testing**

---

## Testing Philosophy

In an educational platform supporting learners with special educational needs, software defects carry high pedagogical and emotional costs:
* An evaluation bug can falsely report a struggling student as proficient, or penalize a correct response.
* An unhandled exception or broken layout can disorient and overwhelm a sensory-sensitive learner.
* Inconsistent analytics can corrupt Individualized Education Program (IEP) compliance records.

Eduvia enforces a strict **zero-tolerance testing policy** across all architectural layers. Software is not merged or locked without full automated test execution, static type verification, and clean production builds.

---

## 1. Quality Assurance Hierarchy & Test Suites

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                Static Analysis & Linting                    │
 │       TypeScript (`tsc -b`) • Python Ruff & Mypy            │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │               Frontend Component & Unit Tests               │
 │           Vitest • 13 Passed • WCAG ARIA Mocking            │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │            Backend Pytest Core Suite (217 Tests)            │
 │   16 Test Modules • 84% Line Coverage • Async SQLite / Mock │
 └──────────────────────────────┬──────────────────────────────┘
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
┌───────────────────────────────┐       ┌───────────────────────────────┐
│ Cloud Deployment Validation   │       │ Eduvia Project MCP Protocol   │
│ 8 Tests • Terraform / Docker  │       │ 35 Tests • FastMCP / Stdio    │
│ Migration Runner Verification │       │ Streamable HTTP Remote Tests  │
└───────────────────────────────┘       └───────────────────────────────┘
```

---

## 2. Test Verification Counts Across Milestones

The platform's automated test coverage has grown systematically across implementation phases:

| Milestone Phase | Lock Commit | Backend Pytest | Frontend Tests | Type Check | Build Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Phase 3 (Learner Profile)** | `32a2e3d` | **54 passed** | N/A | Pass | Pass |
| **Phase 4–6 (Activities & Telemetry)** | `42d1420` | **128 passed** | N/A | Pass | Pass |
| **Phase 7 (Analytics & Mastery)** | `f11130f` | **143 passed** | N/A | Pass | Pass |
| **Phase 8 (Adaptive Engine)** | `6d58bb8` | **159 passed** | N/A | Pass | Pass |
| **Phase 9 (Gemini SDK & RAG)** | `a8fe793` | **178 passed** | N/A | Pass | Pass |
| **Phase 10 (Teacher Dashboard)** | `d1c5727` | **192 passed** | 7 passed | Pass | Pass |
| **Phase 11 (Hardening & a11y)** | `ebbd539` | **209 passed** | **13 passed** | Pass | Pass |
| **Phase 12 (Cloud Deployment)** | `b19168a` | **217 passed** | **13 passed** | Pass | Pass |
| **Post-Phase 12 (Project MCP)** | `4ef597b` | **217 passed** | **13 passed** | Pass | Pass |
| *(MCP Server Test Suite)* | `4ef597b` | *(35 MCP passed)* | — | Pass | Pass |

*Note: The 35 MCP tests validate the developer Model Context Protocol tooling located in `tools/eduvia_mcp/tests/` and are tracked separately from the 217 core Eduvia application tests.*

---

## 3. Backend Test Suite Breakdown (217 Tests)

The backend test suite (`pytest`) is organized into 16 specialized test modules executing against an isolated asynchronous database engine:

1. **`test_auth.py`** (4 tests): User login, JWT token generation, invalid password rejection, expired token handling.
2. **`test_users.py`** (4 tests): User profile retrieval, password updating, role verification.
3. **`test_curriculum.py`** (3 tests): 5-tier taxonomy resolution, multilingual JSONB localized queries, recursive tree serialization.
4. **`test_health.py`** (7 tests): Liveness, database connectivity ping, Qdrant vector status, system readiness probes.
5. **`test_api_integration.py`** (13 tests): End-to-end HTTP request flows across auth, curriculum, and learner endpoints.
6. **`test_learners.py`** (13 tests): Learner CRUD, sensory accommodation settings, teacher multi-tenant authorization barriers.
7. **`test_ai_providers.py`** (15 tests): Google GenAI SDK client, prompt templates, structured output parsing, error trapping.
8. **`test_activities.py`** (26 tests): Pydantic discriminated union schemas for all 5 modalities, prompt building, Zero-Strand fallback synthesis.
9. **`test_activity_interaction.py`** (31 tests): Authoritative server-side evaluation, score calculation, assistance level tracking, rejection of invalid payloads.
10. **`test_analytics.py`** (17 tests): Raw telemetry logging, `PerformanceEvent` and `ActivityAttempt` persistence, index queries.
11. **`test_learner_analytics.py`** (15 tests): Dynamic metric synthesis, modality breakdown calculation, error pattern detection.
12. **`test_recommendations.py`** (16 tests): Deterministic adaptation hierarchy, prerequisite DAG traversal, teacher override precedence.
13. **`test_knowledge_ingestion.py`** (5 tests): Semantic chunking, UUIDv5 deterministic ID hashing, idempotent Qdrant upserts.
14. **`test_knowledge_retrieval.py`** (6 tests): Dense vector similarity queries, metadata filtering, semantic ranking.
15. **`test_rag_generation.py`** (3 tests): Grounded prompt construction, citation source tracking, failover behavior.
16. **`test_teacher_dashboard.py`** (14 tests): Scoped cohort aggregations, multi-tenant isolation, deterministic intervention alerts, IEP report export.
17. **`test_cloud_deployment.py`** (8 tests added in Phase 12): Terraform syntax validation, Docker non-root security directives, migration runner script verification, Secret Manager environment mounting.

---

## 4. Frontend Verification Suite

* **Unit & Component Testing (`vitest`)**: **13 tests passing**
  * `ActivityPlayer.test.tsx`: Validates distraction-free mode, audio controls, progressive scaffolding escalation, and keyboard shortcuts (`1–4`, `Space`, `Enter`, `H`, `R`).
  * Accessibility tests: Validates ARIA live region announcements (`useAnnounce`), focus trapping in modal dialogs (`useFocusTrap`), and screen-reader status indicators.
* **Static Type-Checking**: `npm run type-check` (`tsc -b`) compiles with **0 errors**.
* **Production Build**: `npm run build` (`vite build`) produces an optimized production bundle with zero warnings.

---

## 5. Deployment & MCP Tooling Verification

### Deployment Test Harness (`test_cloud_deployment.py`)
To ensure enterprise-grade infrastructure without requiring live GCP billing during local continuous integration:
* Validates that `terraform/*.tf` contains all required resource definitions (`google_cloud_run_v2_service`, `google_sql_database_instance`, `google_secret_manager_secret`).
* Asserts that `Dockerfile` uses non-root execution (`USER appuser:10001`) and sets `dumb-init` as the entrypoint.
* Verifies that the automated migration runner script executes `alembic upgrade head` before starting the application.

### MCP Server Test Harness (`tools/eduvia_mcp/tests/`)
* **35 tests passing** covering all 11 MCP developer tools.
* Validates local `stdio` protocol execution.
* Validates remote `Streamable HTTP` transport over Starlette/FastMCP.
* Validates concurrency locks (`_EXECUTION_LOCK`) to prevent race conditions during parallel verification requests.

---

## Related Documentation

* Master Overview: [[Eduvia Project Overview & Technical Abstract|Eduvia Project Overview & Technical Abstract]]
* Implementation History: [[Eduvia Implementation History — Phases 0–12|Eduvia Implementation History — Phases 0–12]]
* Cloud Deployment: [[Eduvia Production & Cloud Deployment|Eduvia Production & Cloud Deployment]]
* Project MCP Server: [[Eduvia Project MCP|Eduvia Project MCP]]
