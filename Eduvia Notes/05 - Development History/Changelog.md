# Changelog

All notable changes to the Eduvia platform are documented chronologically here.

---

## [Phase 9: Gemini Production & RAG Ingestion] — 2026-09-19
- **Added**: Migration from deprecated `google.generativeai` to modern `google-genai` SDK (`from google import genai`), completely eliminating runtime deprecation warnings.
- **Added**: Vector database integration with Qdrant client managing collections `eduvia_knowledge` and `eduvia_curriculum` with 768-dimensional cosine vector configuration.
- **Added**: Knowledge domain models (`KnowledgeDocument`, `KnowledgeChunk`) and validation schemas (`RetrievedChunk`, `KnowledgeIngestionResult`, `KnowledgeCategory`).
- **Added**: Semantic markdown chunking service `KnowledgeIngestionService` with heading parsing (`##`) and deterministic UUIDv5 point ID generation.
- **Added**: `KnowledgeRetrievalService` for semantic pedagogical context lookup by objective and strategy with score thresholding ($\ge 0.5$).
- **Added**: Contextual RAG grounding injection in `build_activity_generation_messages` with `grounding_sources` payload returned in `ActivityGenerateResponse`.
- **Added**: Zero-Strand Guarantee preservation: deterministic fallback generation is immediately triggered upon any RAG or provider exception.
- **Added**: Frontend type contract updates for `GroundingSource` and `ActivityGenerateResponse`.
- **Verified**: 19 newly introduced Phase 9 tests across `test_ai_providers.py`, `test_knowledge_retrieval.py`, `test_knowledge_ingestion.py`, and `test_rag_generation.py` (with 29 tests total across Phase 9-related test files, including 10 pre-existing foundational tests in `test_ai_providers.py`), achieving **178/178 passing tests** across full backend suite with 83% code coverage and 0 deprecation warnings from Gemini. Frontend production build passing with 0 errors.

## [Phase 8: Adaptive Learning Intelligence Engine] — 2026-09-19

- **Added**: Deterministic `AdaptationEngine` in `app/ai/adaptation/engine.py` evaluating curriculum prerequisites, teacher overrides, difficulty calibration (1–5), presentation modality selection, and pedagogical teaching strategy selection.
- **Added**: Curriculum prerequisite graph traversal preventing recommendations of objectives whose prerequisites are not mastered in Phase 7 analytics.
- **Added**: Strict teacher override precedence (`lock_difficulty_level`, `enforce_strategy`) and teacher constraint enforcement (`excluded_modalities`, `required_modalities`).
- **Added**: Empirical evidence threshold (minimum 5 events) before switching away from learner profile default presentation modalities.
- **Added**: Recommendation schemas (`RecommendationDecision`, `AdaptiveNextActivityResponse`, `ProfileSyncResult`, `ConfidenceLevel`) in `app/recommendations/schemas.py`.
- **Added**: Recommendation service (`RecommendationService`) and REST router endpoints (`GET /learners/{id}`, `POST /learners/{id}/next-activity`, `POST /learners/{id}/sync-profile`).
- **Added**: Frontend adaptive UI components: `RecommendationCard.tsx` with confidence indicator, rationale, applied constraints, 1-click launch, and profile synchronization.
- **Added**: Dashboard "Adaptive Engine" tab with real-time learner selection and recommendation cards.
- **Verified**: 16 new tests in `test_recommendations.py`, achieving **159/159 passing tests** across full backend suite with 82% code coverage. Frontend build passing with 0 errors.

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
- **Verified**: 26 new tests in `test_activities.py` (22 test functions defined in code: 21 standalone functions + 1 function parametrized across 5 modalities), achieving **80/80 passing tests**. Frontend build verified. Committed (`42d1420`).

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
