# Changelog

All notable changes to the Eduvia platform are documented chronologically here.

---

## [Eduvia Project MCP Server] — 2026-09-19
- **Added**: Purpose-built Model Context Protocol (MCP) server under `tools/eduvia_mcp/` providing direct, sandboxed introspection and verification tools for AI coding assistants and automation pipelines.
- **Added**: 11 registered developer tools: `project_context`, `search_project`, `read_project_file`, `list_project_files`, `git_status`, `git_diff`, `run_backend_tests`, `run_frontend_tests`, `run_typecheck`, `run_build`, and `verify_project`.
- **Added**: Dual transport support: local Standard I/O (`stdio`) for CLI/agent pairing, and remote `Streamable HTTP` (Server-Sent Events via Starlette/Uvicorn) for distributed or cloud-hosted agent environments.
- **Added**: Thread concurrency locking (`_EXECUTION_LOCK`) in `project.py` preventing race conditions or resource thrashing during concurrent verification runs.
- **Added**: Path traversal sandboxing restricting file access strictly to within the repository root.
- **Added**: 35 automated unit/integration tests in `tools/eduvia_mcp/tests/test_project.py` validating tool discovery, subprocess execution, error trapping, and transport protocols.
- **Added**: Dockerfile and Terraform `cloud_run.tf` service declaration for remote MCP hosting on Google Cloud Run.
- **Verified**: 35/35 MCP tests passing. Full regression suite passing. Repository cleaned and synchronized (`4ef597b`).

## [Phase 12: Production Cloud Deployment Infrastructure] — 2026-09-19
- **Added**: Declarative Terraform infrastructure under `terraform/` targeting Google Cloud Platform (GCP): `main.tf`, `cloud_run.tf`, `cloud_sql.tf`, `secrets.tf`, `variables.tf`, and `outputs.tf`.
- **Added**: Cloud Run serverless service definitions with autoscaling (0–10 instances) and IAM service account bindings.
- **Added**: Cloud SQL PostgreSQL 16 managed database configuration with private VPC peering and automated backups.
- **Added**: Google Secret Manager integration provisioning secrets for database credentials, JWT keys, and Gemini API keys.
- **Added**: Multi-stage, hardened production `Dockerfile` featuring unprivileged execution (`USER appuser:10001`) and `dumb-init` PID 1 process supervision.
- **Added**: Automated database migration runner executing `alembic upgrade head` before web server startup.
- **Added**: Cloud Build CI/CD configuration (`cloudbuild.yaml`) orchestrating automated test execution, multi-stage container compilation, Artifact Registry push, and Cloud Run revision deployment.
- **Added**: Deployment verification test suite `backend/tests/test_cloud_deployment.py` with 8 automated tests validating Terraform syntax, Docker directives, migration commands, and Secret Manager environment mounting.
- **Verified**: 8 new deployment tests in `test_cloud_deployment.py`, achieving **217/217 passing backend tests**. Frontend build and type-check passing. Milestone locked in commit `b19168a`.

## [Phase 11: System Hardening & Accessibility Audit] — 2026-09-19
- **Added**: Centralized backend security headers middleware (`SecurityHeadersMiddleware`) enforcing `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `X-XSS-Protection: 0`, customized non-breaking Content Security Policy (CSP), and production-aware Strict-Transport-Security (HSTS; active in production HTTPS, omitted in local dev).
- **Added**: Thread-safe bounded in-memory sliding-window rate limiter (`InMemoryRateLimiter`) with automatic eviction of stale entries, HTTP 429 status, and `Retry-After` header.
- **Added**: Route-specific rate limiting on sensitive endpoints: `POST /api/v1/auth/login` (client IP, 5 req/min), `POST /api/v1/activities/generate` (teacher identity, 20 req/min), and `POST /api/v1/activities/evaluate` (client IP, 60 req/min).
- **Added**: Production documentation exposure control: disables `/docs`, `/redoc`, and `/openapi.json` when `APP_ENV=production`.
- **Added**: CORS hardening restricting allowed methods to explicit verbs (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`) and explicit headers (`Authorization`, `Content-Type`, `Accept`, `Origin`, `X-Requested-With`).
- **Added**: `get_current_active_teacher` authorization dependency enforcing verified active teacher/admin identity.
- **Added**: Frontend accessible global skip link (`<a href="#main-content" className="skip-to-content">`) targeting primary content landmarks.
- **Added**: Accessible semantic tab navigation in `DashboardPage.tsx` using `role="tablist"`, `role="tab"`, `aria-selected`, `aria-controls`, and `role="tabpanel"`, removing pseudo `href="#"` navigation.
- **Added**: Focus containment & restoration in `IEPReportModal.tsx`: captures opener element, traps `Tab` and `Shift+Tab` without leaking to background interactive controls, safely handles empty control sets, and restores focus on close.
- **Added**: Switch device & accessible keyboard navigation in `ActivityPlayer.tsx`: number keys `1`–`4` for option selection, `Enter`/`Space` for submission, `H` for progressive hint revelation, and `R` for audio prompt playback, respecting form input focus.
- **Added**: Semantic ARIA live regions (`role="status"`, `aria-live="polite"`, `aria-atomic="true"`) in `ActivityPlayer.tsx` announcing hint revelations, answer evaluations, and activity resets.
- **Added**: High contrast & forced colors enhancements in `index.css` via `@media (forced-colors: active)` ensuring focus rings, selected controls, borders, and state indicators remain visible.
- **Added**: Multi-cue non-color indicators on alert severity badges, question options, and feedback dialogs.
- **Verified**: 17 new tests in `test_hardening.py` achieving **209/209 passing backend tests** with 84% code coverage. 6 new frontend accessibility tests in `accessibility.test.mjs` achieving **13/13 passing frontend tests**. Frontend production build passing with 0 errors and 0 type-check errors. Milestone locked in commit `ebbd539`.

## [Phase 10: Teacher Dashboard & Insights] — 2026-09-19
- **Added**: Backend teacher dashboard service (`TeacherDashboardService`) and REST router (`/api/v1/teacher/dashboard`, `/api/v1/teacher/cohort/insights`, `/api/v1/teacher/alerts`, `/api/v1/teacher/learners/{id}/iep-report`).
- **Added**: Real-time overview KPI aggregations across assigned learners, completed practice counts, cohort accuracy, and active educational alerts.
- **Added**: Classroom & cohort analytics with configurable date-range filtering, sensory modality distribution metrics, and curriculum objective competency state counts.
- **Added**: Deterministic educational intervention alerts with strict non-diagnostic pedagogical wording (`low_accuracy_repeated`, `assistance_reliance_high`, `mastery_stalled`, `inactivity_threshold`).
- **Added**: Individualized Education Plan (IEP) progress reporting with longitudinal mastery summaries, modality efficacy metrics, evidence-based recommendations, and multi-format export (standardized Markdown, structured JSON, and print layout).
- **Added**: Strict server-side multi-tenant teacher ownership validation (`learner.teacher_id == current_user.id`), with 403 Forbidden for unassigned educators.
- **Added**: Frontend teacher dashboard components: `TeacherOverview.tsx`, `CohortInsightsView.tsx`, `IEPReportModal.tsx`, and integrated sidebar navigation in `DashboardPage.tsx`.
- **Added**: Offline mock support in `dev_server.py` with `MockTeacherDashboardService`.
- **Verified**: 14 new tests in `test_teacher_dashboard.py`, achieving **192/192 passing tests** across full backend suite with 84% code coverage. Frontend build passing with 0 errors and 7/7 frontend unit tests passing. Milestone locked in commit `d1c5727`.

## [Phase 9: Gemini Production & RAG Ingestion] — 2026-09-19
- **Added**: Migration from deprecated `google.generativeai` to modern `google-genai` SDK (`from google import genai`), completely eliminating runtime deprecation warnings.
- **Added**: Vector database integration with Qdrant client managing collections `eduvia_knowledge` and `eduvia_curriculum` with 768-dimensional cosine vector configuration.
- **Added**: Knowledge domain models (`KnowledgeDocument`, `KnowledgeChunk`) and validation schemas (`RetrievedChunk`, `KnowledgeIngestionResult`, `KnowledgeCategory`).
- **Added**: Semantic markdown chunking service `KnowledgeIngestionService` with heading parsing (`##`) and deterministic UUIDv5 point ID generation.
- **Added**: `KnowledgeRetrievalService` for semantic pedagogical context lookup by objective and strategy with score thresholding ($\ge 0.5$).
- **Added**: Contextual RAG grounding injection in `build_activity_generation_messages` with `grounding_sources` payload returned in `ActivityGenerateResponse`.
- **Added**: Zero-Strand Guarantee preservation: deterministic fallback generation is immediately triggered upon any RAG or provider exception.
- **Added**: Frontend type contract updates for `GroundingSource` and `ActivityGenerateResponse`.
- **Verified**: 19 newly introduced Phase 9 tests across `test_ai_providers.py`, `test_knowledge_retrieval.py`, `test_knowledge_ingestion.py`, and `test_rag_generation.py` (with 29 tests total across Phase 9-related test files, including 10 pre-existing foundational tests in `test_ai_providers.py`), achieving **178/178 passing tests** across full backend suite with 83% code coverage and 0 deprecation warnings from Gemini. Frontend production build passing with 0 errors. Milestone locked in commit `a8fe793`.

## [Phase 8: Adaptive Learning Intelligence Engine] — 2026-09-19
- **Added**: Deterministic `AdaptationEngine` in `app/ai/adaptation/engine.py` evaluating curriculum prerequisites, teacher overrides, difficulty calibration (1–5), presentation modality selection, and pedagogical teaching strategy selection.
- **Added**: Curriculum prerequisite graph traversal preventing recommendations of objectives whose prerequisites are not mastered in Phase 7 analytics.
- **Added**: Strict teacher override precedence (`lock_difficulty_level`, `enforce_strategy`) and teacher constraint enforcement (`excluded_modalities`, `required_modalities`).
- **Added**: Empirical evidence threshold (minimum 5 events) before switching away from learner profile default presentation modalities.
- **Added**: Recommendation schemas (`RecommendationDecision`, `AdaptiveNextActivityResponse`, `ProfileSyncResult`, `ConfidenceLevel`) in `app/recommendations/schemas.py`.
- **Added**: Recommendation service (`RecommendationService`) and REST router endpoints (`GET /learners/{id}`, `POST /learners/{id}/next-activity`, `POST /learners/{id}/sync-profile`).
- **Added**: Frontend adaptive UI components: `RecommendationCard.tsx` with confidence indicator, rationale, applied constraints, 1-click launch, and profile synchronization.
- **Added**: Dashboard "Adaptive Engine" tab with real-time learner selection and recommendation cards.
- **Verified**: 16 new tests in `test_recommendations.py`, achieving **159/159 passing tests** across full backend suite with 82% code coverage. Frontend build passing with 0 errors. Milestone locked in commit `6d58bb8`.

## [Phase 7: Learner Analytics & Mastery Tracking] — 2026-09-19
- **Added**: Dynamic analytics aggregation service computing overall accuracy, mean response latency, hint usage, and assistance levels on-demand from raw `PerformanceEvent` records without speculative permanent tables.
- **Added**: Sensory modality metrics (`ModalityMetrics`) analyzing accuracy across all 5 presentation channels (`visual`, `interactive`, `reading`, `audio`, `writing`).
- **Added**: Activity modality metrics (`ActivityTypeMetrics`) across 5 interaction types (`matching`, `multiple_choice`, `ordering`, `visual_identification`, `drag_drop`).
- **Added**: Deterministic objective mastery rubric enforcing the Pedagogical Independence Principle ($\text{accuracy} \ge 0.80 \land \text{avg\_assistance} \le 1$). Excessive assistance strictly invalidates mastery.
- **Added**: Longitudinal progress trajectory grouping performance chronologically by calendar day (UTC).
- **Added**: REST API endpoints: `GET /learners/{id}/summary`, `GET /learners/{id}/mastery`, `GET /learners/{id}/progress` with teacher multi-tenant authorization (`403 Forbidden` for unassigned educators).
- **Added**: Cognitive Calm `AnalyticsDashboard.tsx` UI with student selector, summary KPI cards, sensory modality efficacy badges, and mastery tables.
- **Fixed**: Resolved 7 type-checking and lint errors in `backend/app/analytics/models.py`.
- **Verified**: 15 new tests in `test_learner_analytics.py`, achieving **143/143 passing tests** across full backend suite with 82% code coverage. Frontend build passing with 0 errors. Committed (`f11130f`) and pushed to `origin/develop`.

## [Phase 6: Performance Tracking & Telemetry] — 2026-09-19
- **Added**: Relational models `PerformanceEvent` and `ActivityAttempt` for immutable persistent telemetry storage in `backend/app/analytics/models.py`.
- **Added**: Alembic migration `20260919_0730_b4c5d6e7f8a9_create_analytics_tables.py`.
- **Added**: Composite database indexes on `(learner_id, timestamp)`, `(activity_id, timestamp)`, `objective_id`, and `activity_type`.
- **Added**: Authoritative evaluation hook in `activities/service.py` automatically emitting verified performance events upon answer submission.
- **Added**: Teacher multi-tenant data access control and REST endpoints (`/api/v1/analytics/events`, `/api/v1/analytics/attempts`, `/api/v1/analytics/learners/{id}/events`).
- **Added**: Frontend API client methods in `analyticsApi` and dev server mock storage.
- **Verified**: 17 new tests in `test_analytics.py`, achieving **128/128 passing tests**. Frontend build verified. Committed (`42d1420`).

## [Phase 5: Learner Experience & Activity Interaction] — 2026-09-19
- **Added**: Distraction-free learner routes (`/learn/:activityId`, `/learn/preview`) and accessible layout.
- **Added**: `ActivityPlayer.tsx` coordinator managing activity lifecycle, attempt counters, and hint requests.
- **Added**: 5 specialized interactive renderers: `MatchingActivity`, `MultipleChoiceActivity`, `OrderingActivity`, `VisualIdentificationActivity`, and `DragDropActivity`.
- **Added**: Text-to-Speech (TTS) integration using Web Speech API with custom hook `useSpeechSynthesis.ts`.
- **Added**: 3-tier progressive scaffolding: Level 1 (Subtle prompt), Level 2 (Direct hint), Level 3 (Full demonstration).
- **Added**: Cognitive Calm feedback component `CognitiveCalmFeedback.tsx` eliminating punitive alarm indicators.
- **Added**: Authoritative backend evaluation endpoint `POST /api/v1/activities/evaluate` verifying submissions server-side.
- **Verified**: 31 new tests in `test_activity_interaction.py`, achieving **111/111 passing tests**. Frontend build verified. Committed (`42d1420`).

## [Phase 4: Activity Generation Engine] — 2026-09-19
- **Added**: Strict Pydantic contracts for 5 activity modalities: `matching`, `multiple_choice`, `ordering`, `visual_identification`, `drag_drop`.
- **Added**: Context-aware Cognitive Calm prompt builders in `app/ai/generation/prompts.py`.
- **Added**: AI Orchestrator integrating Google Gemini with structured JSON output enforcement.
- **Added**: Zero-Strand Guarantee deterministic fallback generator `fallbacks.py` handling all network/model/quota failure paths.
- **Added**: Activity generation REST API `POST /api/v1/activities/generate` and mock generator in `dev_server.py`.
- **Fixed**: Corrected Phase 4 scope from initial prompt error (Learner Profile belongs to Phase 3; Activity Generation is Phase 4).
- **Verified**: 26 new tests in `test_activities.py` (22 test functions defined in code: 21 standalone functions + 1 function parametrized across 5 modalities), achieving **80/80 tests**. Frontend build verified. Committed (`42d1420`).

## [Phase 3: Learner Profile & Domain Entity] — 2026-09-19
- **Added**: `Learner` and `LearnerProfile` models in `backend/app/learners/models.py`.
- **Added**: Relational persistence tracking communication mode, support requirements, modality effectiveness, and strategy effectiveness.
- **Added**: `LearnerService` with teacher observation log history and teacher multi-tenant access control.
- **Added**: Frontend `LearnerManager.tsx` with multi-tab profile inspection.
- **Added**: In-memory `MockLearnerService` in `dev_server.py`.
- **Verified**: 54/54 passing backend tests, 7 frontend unit tests. Committed (`32a2e3d`).

## [Phase 2 Integration & Polish] — 2026-09-19
- **Fixed**: Corrected router inclusion in `backend/app/api/v1/router.py` to register curriculum endpoints.
- **Fixed**: Unified token storage keys in frontend (`eduvia_access_token`) and resolved Axios response unwrapping bug in `LoginPage.tsx` and `AuthContext.tsx`.
- **Fixed**: Fixed CP1252 character encoding in all frontend feature `index.ts` files to resolve Oxlint UTF-8 parsing errors.
- **Added**: Upgraded `CurriculumBrowser.tsx` to full interactive 5-tier drill-down with accessible breadcrumb navigation.
- **Added**: Created comprehensive automated test suite for curriculum API authentication and role restrictions in `backend/tests/test_api_integration.py`.
- **Added**: Created `backend/scripts/seed_demo_data.py` for automated seeding of demo users and curriculum.
- **Added**: Structured Obsidian knowledge base in `Eduvia Notes/` and updated `.gitignore`.

## [Phase 2] — 2026-09-18
- **Added**: 5-tier relational curriculum hierarchy models in `backend/app/curriculum/models.py`.
- **Added**: Alembic migration `20260918_2347_65b1ea98eb6f_create_curriculum_tables.py`.
- **Added**: Pydantic schemas supporting localized JSONB titles and difficulty constraints.
- **Added**: `CurriculumService` with optimized `selectinload` queries.
- **Added**: Initial demonstration seed script `backend/scripts/seed_curriculum.py`.

## [Phase 1] — 2026-09-18
- **Added**: User models, schemas, service, and router.
- **Added**: JWT authentication with OAuth2 password request form.
- **Added**: Alembic migration `20260918_2320_268264a74567_create_users_table.py`.
- **Added**: Frontend auth context, login page, and protected route wrapper.

## [Phase 0] — 2026-09-18
- **Added**: Docker Compose configuration (PostgreSQL, Qdrant, backend, frontend).
- **Added**: FastAPI backend foundation and Vite frontend skeleton.
- **Added**: Abstract `LLMProvider` and `EduViaQdrantClient` boundaries.
