# Eduvia Architecture & System Design

> **Modular Monolith Architecture Engineered for Stability, Accessibility, and Strict Pedagogical Governance**

---

## Architectural Philosophy

Eduvia is engineered as an asynchronous **Modular Monolith**. This architectural choice provides high cohesion, transactional integrity, and minimal operational overhead during active educational deployments, while maintaining clean domain boundaries that allow individual services to be extracted into distributed cloud microservices if needed.

The platform enforces five core architectural invariants:
1. **Clean Domain Segregation**: Each domain (`auth`, `curriculum`, `learners`, `activities`, `analytics`, `recommendations`, `teacher_dashboard`, `knowledge`) manages its own database models, Pydantic schemas, and service layer logic.
2. **Server-Side Evaluation Authority**: Frontend clients are strictly presentation layers. All grading, assistance level attribution, and mastery scoring take place on the server.
3. **Dynamic Metric Synthesis (Zero Speculative Data)**: Telemetry events are stored as immutable records. Analytics, mastery states, and cohort metrics are synthesized dynamically, preventing desynchronization between historical logs and cached tables.
4. **Deterministic Orchestration of Generative AI**: Generative AI models are encapsulated behind strict provider interfaces and are used exclusively for text generation within pre-validated schemas. All routing, pedagogical progression, and curriculum decisions are deterministic.
5. **Multi-Tenant Teacher Boundaries**: Educators can only inspect and manage learners enrolled in their assigned classroom cohorts.

---

## High-Level System Topology

```text
                               ┌──────────────────────────────────────────────┐
                               │                Web Clients                   │
                               │  React 19 + TypeScript (WCAG 2.1 AA / a11y)  │
                               └──────────────────────┬───────────────────────┘
                                                      │ HTTPS / JSON
                                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                           FastAPI Backend Gateway                                           │
│  Security Headers (CSP, HSTS) • In-Memory Rate Limiting • OAuth2 JWT Auth • Global Error Interceptors       │
└─────────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                            Modular Domain Services                                          │
│                                                                                                             │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐                     │
│  │   Auth & RBAC Domain    │  │    Curriculum Domain    │  │     Learners Domain     │                     │
│  │   JWT, Bcrypt, Roles    │  │ 5-Level Hierarchy, Graph│  │ Profile, Sensory State  │                     │
│  └────────────┬────────────┘  └────────────┬────────────┘  └────────────┬────────────┘                     │
│               │                            │                            │                                   │
│  ┌────────────┴────────────┐  ┌────────────┴────────────┐  ┌────────────┴────────────┐                     │
│  │ Activity Gen Service    │  │ Evaluation Authority    │  │ Telemetry Ingestion     │                     │
│  │ 5 Modalities + Fallback │  │ Server-Side Grading     │  │ Immutable Events/Attempts│                    │
│  └────────────┬────────────┘  └────────────┬────────────┘  └────────────┬────────────┘                     │
│               │                            │                            │                                   │
│  ┌────────────┴────────────┐  ┌────────────┴────────────┐  ┌────────────┴────────────┐                     │
│  │ Dynamic Mastery Engine  │  │ Recommendation Engine   │  │ Teacher Dashboard & IEP │                     │
│  │ Accuracy + Independence │  │ Deterministic Hierarchy │  │ Scoped Cohort Analytics │                     │
│  └────────────┬────────────┘  └────────────┬────────────┘  └────────────┬────────────┘                     │
│               │                            │                            │                                   │
│  ┌────────────┴────────────────────────────┴────────────────────────────┴────────────┐                     │
│  │                             RAG Knowledge & AI Orchestration                      │                     │
│  │         Gemini 2.5 Flash (`google-genai`) • Semantic Grounding • Fallback Engine  │                     │
│  └─────────────────────────────────────────┬─────────────────────────────────────────┘                     │
└────────────────────────────────────────────┼────────────────────────────────────────────────────────────────┘
                                             │
                      ┌──────────────────────┴──────────────────────┐
                      ▼                                             ▼
       ┌─────────────────────────────┐               ┌─────────────────────────────┐
       │     PostgreSQL 16 (RDBMS)   │               │     Qdrant (Vector DB)      │
       │   Relational State Store    │               │    Pedagogical Knowledge    │
       │  • Users, Roles, Passwords  │               │  • `eduvia_knowledge`       │
       │  • Curriculum & Prereqs     │               │  • `eduvia_curriculum`      │
       │  • Learner Profiles         │               │  • 768-dim Embeddings       │
       │  • PerformanceEvents (Logs) │               │  • UUIDv5 Deduplication     │
       │  • ActivityAttempts (Logs)  │               │  • Grounding Metadata       │
       └─────────────────────────────┘               └─────────────────────────────┘
```

---

## Domain Responsibility Matrix

| Domain Module | Primary Responsibilities | Data Persistence | Invariants & Guardrails |
| :--- | :--- | :--- | :--- |
| **Auth & Security** | User registration, authentication, JWT issuing, password hashing, RBAC enforcement (`admin`, `teacher`, `learner`). | `users` table | Passwords hashed with Bcrypt. Tokens expire after configurable TTL. Public registration disabled in production. |
| **Curriculum** | 5-level educational taxonomy (Subject $\rightarrow$ Grade $\rightarrow$ Domain $\rightarrow$ Topic $\rightarrow$ Objective), multilingual JSONB titles, prerequisite graph resolution. | `subjects`, `grades`, `domains`, `topics`, `learning_objectives`, `prerequisites` | Prerequisite DAG must remain acyclic. Objectives require target difficulty and assessment criteria. |
| **Learners** | Learner entity creation, teacher association, demographic metadata, dynamic modality affinity, and sensory accommodation preferences. | `learners`, `learner_profiles` | Each learner is assigned to an authoritative teacher. Accommodations are applied during prompt synthesis and UI rendering. |
| **Activities** | Dynamic synthesis of 5 modality types (Matching, Multiple Choice, Ordering, Visual Identification, Drag and Drop) via Gemini and local fallback. | Ephemeral or cached; validated against Pydantic models | Zero-Strand Guarantee: fallback generator produces fully valid activities if AI provider is disconnected. |
| **Evaluation Authority** | Server-side validation of student interaction submissions, calculation of score, determination of correctness, tracking of assistance level used. | Processes raw payloads; invokes telemetry logging | Client-side correctness claims are rejected. Answers are matched against authoritative server keys. |
| **Telemetry & Ingestion** | Ingestion and storage of granular learner interactions: time on task, hint usage, error attempts, and interaction sequences. | `performance_events`, `activity_attempts` tables (Alembic migration 3) | Records are immutable. High-efficiency composite indexes on `(learner_id, objective_id, created_at)`. |
| **Mastery & Analytics** | Aggregation of raw telemetry into objective accuracy, independence ratio, error patterns, and pedagogical mastery classifications. | Read-only calculation; zero persistent speculative tables | Mastery requires both accuracy $\ge 80\%$ and average assistance level $\le 1$ across $\ge 3$ attempts. |
| **Recommendations** | Deterministic traversal of curriculum prerequisite trees, difficulty calibration, and next-step recommendations based on learner profile. | Ephemeral recommendation DTOs | Rule-based state machine. Teacher manual overrides always supersede algorithmic recommendations. |
| **Teacher Dashboard** | Classroom cohort analytics, student-by-student mastery matrices, deterministic intervention alerts, and IEP progress reporting. | Scoped SQL aggregations over assigned learners | Multi-tenant isolation enforced. Teachers attempting to access unassigned learners receive `403 Forbidden`. |
| **RAG & Knowledge** | Markdown knowledge chunking, UUIDv5 deduplication, dense vector embedding generation, similarity retrieval, and prompt context grounding. | Qdrant vector store (`eduvia_knowledge`, `eduvia_curriculum`) | Grounding sources are tracked and returned in activity metadata. Retrieval failure gracefully falls back to core prompts. |

---

## Data Layer & Persistence Architecture

### Relational Persistence (PostgreSQL 16)
The relational schema is managed through **SQLAlchemy 2.0 AsyncEngine** backed by **asyncpg**. Database structure evolves through tracked, linear **Alembic** migrations:
* **Migration 1 (`001_initial_auth_and_users`)**: Base user entities, credential hashes, and role hierarchies.
* **Migration 2 (`002_curriculum_and_objectives`)**: 5-level curriculum taxonomy, localized JSONB fields, prerequisite mapping.
* **Migration 3 (`003_learners_telemetry_attempts`)**: Learner entities, dynamic profiles, immutable `performance_events`, and comprehensive `activity_attempts`.

```text
┌──────────────────────┐       1:N       ┌────────────────────────┐
│        Users         │────────────────▶│        Learners        │
│   (Teachers/Admins)  │                 │  (Name, Grade, Age)    │
└──────────────────────┘                 └───────────┬────────────┘
                                                     │ 1:1
                                                     ▼
                                         ┌────────────────────────┐
                                         │    LearnerProfiles     │
                                         │  (Affinities, Accomms) │
                                         └────────────────────────┘
                                                     │
                                                     ├──────────────────────────┐
                                                     │ 1:N                      │ 1:N
                                                     ▼                          ▼
                                         ┌────────────────────────┐ ┌────────────────────────┐
                                         │   PerformanceEvents    │ │    ActivityAttempts    │
                                         │  (Granular telemetry)  │ │  (Completed sessions)  │
                                         └────────────────────────┘ └────────────────────────┘
```

### Vector Persistence (Qdrant)
Unstructured pedagogical literature, Universal Design for Learning (UDL) guidelines, and cognitive accommodation research are stored in **Qdrant**:
* **Vector Dimensions**: 768 dimensions corresponding to Google `text-embedding-004`.
* **Distance Metric**: Cosine similarity (`Distance.COSINE`).
* **Collection Partitioning**:
  * `eduvia_knowledge`: Evidence-based special education literature and instructional strategies.
  * `eduvia_curriculum`: Dense vector representations of learning objectives for semantic prerequisite mapping.
* **Idempotent Ingestion**: Documents are segmented into semantically coherent passages, assigned deterministic **UUIDv5** IDs generated from namespace and chunk content, and upserted idempotently.

---

## API & Gateway Layer

FastAPI serves as the asynchronous HTTP engine, organized around feature routers registered under the `/api/v1` namespace:

```text
/api/v1
  ├── /auth              → Authentication, JWT tokens, session inspection
  ├── /curriculum        → Subject, grade, domain, and objective exploration
  ├── /learners          → Learner management, profiles, sensory settings
  ├── /activities        → Activity generation, server-side evaluation, hints
  ├── /analytics         → Objective-level mastery, modality breakdowns, timelines
  ├── /recommendations   → Deterministic next-step recommendations
  ├── /teacher-dashboard → Scoped cohort analytics, alerts, IEP reports
  └── /health            → System liveness, database ping, Qdrant status
```

### Middleware & Cross-Cutting Concerns
1. **Security Headers**: Injects `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, and `Strict-Transport-Security`.
2. **Rate Limiting**: Sliding-window in-memory throttling prevents denial-of-service or credential stuffing attacks on authentication and AI generation routes.
3. **CORS Validation**: Restricts cross-origin resource sharing to explicitly whitelisted client origins.
4. **Exception Mapping**: Intercepts domain errors (e.g., `LearnerNotFoundError`, `UnauthorizedAccessError`, `PrerequisiteNotMetError`) and maps them to clean RFC 7807 problem details with non-leaking error responses.

---

## Frontend Component & Layer Design

The frontend is constructed using **React 19**, **TypeScript**, and **Vite**:

* **Presentation Layer (`components/`)**: Atomic, accessible visual components (accessible buttons, high-contrast inputs, modal dialogs with focus trapping).
* **Feature Modules (`features/`)**:
  * `activities/`: Specialized renderers for the 5 modalities (`MatchingActivity`, `MultipleChoiceActivity`, `OrderingActivity`, `VisualIdentificationActivity`, `DragAndDropActivity`), orchestrating keyboard shortcuts and screen-reader announcements.
  * `learner/`: Distraction-free learner workspace (`ActivityPlayer`), TTS controller, and progressive scaffolding visualizer.
  * `teacher/`: Classroom cohort dashboard, intervention alert cards, and longitudinal IEP progress export views.
  * `curriculum/`: Recursive curriculum tree explorer with prerequisite visualization.
* **State & Services (`services/`, `hooks/`)**:
  * Asynchronous API clients with typed error boundaries.
  * Accessibility hooks: `useAnnounce` for ARIA live messages, `useFocusTrap` for modal containment, and `useSpeech` for Web Speech API integration.

---

---

## Deployment & Infrastructure Architecture

Phase 12 codified and validated the production infrastructure as code, maintaining a clean architectural separation between application logic and deployment topology:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Application Layer                              │
│         FastAPI Modular Monolith Backend & React 19 Accessible Frontend     │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Containerization
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               Container Layer                               │
│  • Backend Dockerfile: Python 3.12, non-root `eduvia:1001`, dumb-init, $PORT│
│  • Frontend Dockerfile: Node 20 builder, Alpine Nginx runtime, SPA fallback │
│  • MCP Dockerfile: Streamable HTTP microservice container                   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Cloud Build CI/CD
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Cloud Runtime (Serverless)                         │
│  Google Cloud Run v2 Services:                                              │
│  • `eduvia-backend-${env}`: Autoscaling 0–10, Unix socket Cloud SQL mount   │
│  • `eduvia-frontend-${env}`: Public static SPA delivery via Nginx           │
│  • `eduvia-mcp-${env}`: Dedicated Model Context Protocol server endpoint    │
│  • `eduvia-migration-job`: Cloud Run Job executing `alembic upgrade head`   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Private IAM & VPC
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Managed Database / Secrets / Registry                    │
│  • Google Cloud SQL: Managed PostgreSQL 16 instance with SSD storage        │
│  • Google Secret Manager: Injected runtime credentials (DB, JWT, Gemini)    │
│  • Google Artifact Registry: Versioned image repository (`eduvia-containers`)│
└─────────────────────────────────────────────────────────────────────────────┘
```

> **Architectural Boundary:** The application code is cloud-agnostic and maintains local development parity via Docker Compose, while declarative Terraform scripts (`terraform/`) configure the GCP production runtime environment.

---

## Related Documentation

* Central Abstract: [[Eduvia Project Overview & Technical Abstract|Eduvia Project Overview & Technical Abstract]]
* Learning & Personalization: [[Eduvia Learning & Personalization Approach|Eduvia Learning & Personalization Approach]]
* AI & RAG Specifications: [[Eduvia AI & RAG Technical Approach|Eduvia AI & RAG Technical Approach]]
* Accessibility Standards: [[Eduvia Accessibility & Cognitive Calm|Eduvia Accessibility & Cognitive Calm]]
* Security Engineering: [[Eduvia Security & Privacy Engineering|Eduvia Security & Privacy Engineering]]
* Cloud Infrastructure: [[Eduvia Production & Cloud Deployment|Eduvia Production & Cloud Deployment]]
* Phase 12 Architecture History: [[05 - Development History/Phase 12 — Production Cloud Deployment & Staging|Phase 12 — Production Cloud Deployment & Staging]]
* Testing & Verification: [[Eduvia Testing & Verification|Eduvia Testing & Verification]]
