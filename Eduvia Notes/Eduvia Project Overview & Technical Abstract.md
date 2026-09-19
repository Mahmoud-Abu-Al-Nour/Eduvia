# Eduvia Project Overview & Technical Abstract

> **Standardized Curriculum + Personalized Delivery**

---

## Executive Summary

Special education systems worldwide face an acute pedagogical bottleneck: learners with cognitive differences, neurodivergence, or sensory sensitivities require individualized instructional pacing, tailored modalities, and progressive scaffolding. However, standard educational software frequently forces a destructive compromise: either it simplifies the curriculum itself—diminishing academic expectations and creating compounding achievement gaps—or it overwhelms the learner with visually cluttered, sensorially aggressive interfaces that induce cognitive fatigue.

**Eduvia** resolves this systemic tension through a foundational engineering thesis: **keep the curriculum standardized, controlled, and academically rigorous, while dynamically personalizing the instructional delivery**. 

Developed as a modern, accessible educational platform, Eduvia provides structured learning objectives mapped to national curriculum standards while an intelligent backend evaluates learner interactions in real time. Rather than relying on unconstrained generative AI or ungrounded heuristics, Eduvia combines deterministic decision boundaries with retrieval-augmented generative AI (Gemini 2.5 Flash and Qdrant vector retrieval). The system generates sensory-tailored activities across five modalities, evaluates submissions authoritatively on the server, aggregates fine-grained telemetry, and computes transparent, objective-level mastery.

Eduvia is built specifically for **teachers, special educators, schools, and specialized academies**, providing them with transparent classroom cohort insights, deterministic intervention alerts, and longitudinal IEP (Individualized Education Program) progress reporting. For the learner, Eduvia delivers a distraction-free, WCAG 2.1 AA-hardened experience grounded in the principle of **Cognitive Calm**.

---

## Core System Principles

1. **Standardized Curriculum + Personalized Delivery**  
   Curriculum fidelity is non-negotiable. Every learner works toward verified academic standards. What changes is *how* the concept is presented—varying visual density, interaction modality, scaffolding depth, and conceptual metaphors.

2. **Authoritative Backend Evaluation**  
   The client application is strictly an input/output terminal. All correctness grading, assistance tracking, time-on-task telemetry, and mastery updates are computed authoritatively on the FastAPI backend. Client-side claims of correctness are never trusted.

3. **Deterministic Adaptation Over Black-Box AI**  
   Pedagogical progression, prerequisite traversal, and intervention triggers are governed by deterministic, rule-based state machines. Generative AI is strictly constrained to *content generation* (drafting questions, narratives, and distractors within bounded Pydantic schemas). **AI never decides whether a student has mastered an objective or which prerequisite to enforce.**

4. **Cognitive Calm & Accessibility-First Design**  
   Learners with neurodivergence or sensory sensitivities are protected from overwhelming stimulation. The interface eliminates countdown timers, punitive sound effects, flashing animations, and cluttered sidebars. Feedback is gentle, progressive, and supportive. Accessibility is engineered into the DOM hierarchy, supporting full keyboard navigation, single-switch input, ARIA live announcements, high-contrast modes, and integrated Text-to-Speech (TTS).

5. **Teacher Governance & Multi-Tenant Isolation**  
   Eduvia is an assistive tool for educators, not an autonomous replacement. Teachers retain absolute override authority over learner paths, prerequisite locks, and modality assignments. Multi-tenant data boundaries ensure teachers only access learners within their authorized classroom cohorts.

---

## End-to-End Conceptual Dataflow

```text
 ┌──────────────────────────────────────────────────────────────┐
 │                  Teacher / Curriculum Layer                  │
 │   Standardized Objectives, Prerequisite Trees, Grade Levels   │
 └──────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
 ┌──────────────────────────────────────────────────────────────┐
 │              Activity Generation & RAG Grounding             │
 │   Qdrant Evidence Retrieval + Gemini Structured Generation   │
 │   (Guaranteed Zero-Strand Fallback for Offline Resilience)   │
 └──────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
 ┌──────────────────────────────────────────────────────────────┐
 │               Accessible Learner Interaction                 │
 │   Cognitive Calm UI • 5 Modalities • Keyboard/Switch Control │
 │   Progressive Scaffolding (Hints, Elimination, Demonstration)│
 └──────────────────────────────┬───────────────────────────────┘
                                │ Raw Telemetry & Inputs
                                ▼
 ┌──────────────────────────────────────────────────────────────┐
 │                Authoritative Server Evaluation               │
 │   Server-side Rubric Grading • Assistance Level Scored       │
 │   Immutable PerformanceEvent & ActivityAttempt Logging       │
 └──────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
 ┌──────────────────────────────────────────────────────────────┐
 │             Analytics & Dynamic Mastery Engine               │
 │   Objective Accuracy • Assistance Independence Threshold     │
 │   Error Pattern Detection • Zero Speculative Data Drift      │
 └──────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
 ┌──────────────────────────────────────────────────────────────┐
 │           Deterministic Adaptive Recommendation Engine       │
 │   Prerequisite Traversal • Calibrated Difficulty Scaling     │
 │   Teacher Overrides Enforced • Transparent Pedagogical Logic │
 └──────────────────────────────┬───────────────────────────────┘
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
┌───────────────────────────────┐       ┌───────────────────────────────┐
│     Next Learning Activity    │       │   Teacher Insights Dashboard  │
│   Adaptive delivery cycle     │       │   IEP Reports, Alert Signals, │
│   continues for learner       │       │   Longitudinal Mastery Matrix │
└───────────────────────────────┘       └───────────────────────────────┘
```

---

## Technical Abstract

Eduvia is engineered as a production-ready, modular full-stack application with strict domain isolation and clean architectural boundaries.

### Backend Architecture
* **Core Runtime**: Python 3.12 running asynchronous **FastAPI** on an ASGI Uvicorn stack.
* **Domain Design**: Bounded modular domains (`auth`, `users`, `curriculum`, `learners`, `activities`, `analytics`, `recommendations`, `teacher_dashboard`, `knowledge`).
* **Database & Persistence**: **PostgreSQL 16** managed through **SQLAlchemy 2.0** utilizing the asynchronous `asyncpg` driver. Schema migrations are strictly versioned via **Alembic**.
* **Security & Auth**: OAuth2 password flow with stateless **JWT tokens**, password hashing using **Bcrypt** (`passlib[bcrypt]`), role-based access control (`admin`, `teacher`, `learner`), and scoped multi-tenant isolation.
* **Data Contracts**: Strict schema enforcement via **Pydantic v2** models, input sanitization, and discriminated unions for polymorphic payloads.
* **System Hardening**: Bounded in-memory sliding-window rate limiting on sensitive endpoints (`/auth/login`, `/activities/generate`, `/activities/evaluate`), security headers (CSP, HSTS, X-Frame-Options), and hardened production documentation toggles.

### Frontend Architecture
* **Core Framework**: **React 19** paired with **TypeScript** and bundled via **Vite**.
* **Accessibility & UX**: Semantic HTML5 hierarchy, custom ARIA live region hooks (`useAnnounce`), focus trapping and restoration for dialogs, switch-accessible keybindings (`1–4`, `Enter`, `Space`, `H`, `R`), native Web Speech API Text-to-Speech integration, and WCAG 2.1 AA compliant color palettes.
* **Styling**: Modern, low-overhead styling utilizing responsive CSS variables and Tailwind CSS v4, supporting system-level dark mode, high-contrast mode, and `prefers-reduced-motion`.

### AI & Retrieval-Augmented Generation (RAG)
* **SDK & Model**: Google GenAI SDK (`google-genai`) interfacing with **Gemini 2.5 Flash**.
* **Vector Store**: **Qdrant** vector database running dual collections (`eduvia_knowledge` for evidence-based pedagogical literature, `eduvia_curriculum` for objective embeddings).
* **Embeddings**: `text-embedding-004` producing 768-dimensional dense vector representations.
* **Grounded Pipeline**: Semantic query synthesis, metadata filtering, UUIDv5 deterministic chunk deduplication, top-$k$ pedagogical context injection, and structured JSON output constrained by strict Pydantic schemas.
* **Zero-Strand Guarantee**: 100% deterministic fallback generator providing instant, schema-valid activities if external APIs or networks become unavailable.

### Infrastructure & Cloud Architecture
* **Containerization**: Multi-stage, non-root Docker images (`backend/Dockerfile`, `frontend/Dockerfile`, `frontend/nginx.conf`) with `dumb-init` process supervision.
* **Cloud Orchestration**: Declarative **Terraform** configurations (`terraform/`) targeting **Google Cloud Platform (GCP)**.
* **Target Services**: Serverless **Google Cloud Run** for stateless API containers, managed **Cloud SQL PostgreSQL 16**, **Secret Manager** for zero-leak credential isolation, and automated **Cloud Build** CI/CD deployment pipelines.
* **Infrastructure as Code Validation**: Phase 12 implemented and validated the cloud deployment architecture and automation via automated test suites (`test_cloud_deployment.py`), distinguishing codified infrastructure from live cloud billing resources.

### Developer Tooling & Context Architecture
* **Eduvia Project MCP**: Custom **Model Context Protocol** server (`tools/eduvia_mcp`) exposing 11 project verification, search, test, and diagnostic tools to AI coding agents and external systems. Supports both local `stdio` IPC and production `Streamable HTTP` remote transport.

---

## Platform Deliverables & Capabilities

| Capability Area | What Eduvia Delivers | Explicit Non-Goals & Boundaries |
| :--- | :--- | :--- |
| **Learner Experience** | Accessible, sensory-friendly activities across 5 modalities with text-to-speech, keyboard navigation, and calm progressive scaffolding. | No gamified dopamine loops, flashing graphics, penalty timers, or unmonitored free-form chat. |
| **Curriculum Delivery** | Standardized 5-tier academic hierarchy (Subject, Grade, Domain, Topic, Objective) with prerequisite dependency graphs. | Curriculum standards are never watered down or bypassed without educator intervention. |
| **Adaptation & Personalization** | Deterministic difficulty calibration, scaffolding progression, and modality affinity shifts based on empirical attempt history. | Generative AI never determines student mastery or promotes students through curriculum nodes. |
| **Assessment & Telemetry** | Server-side evaluation of raw interactions, logging latency, attempt counts, and assistance levels into immutable audit logs. | Client-side correctness claims are rejected. Zero speculative summary tables; analytics are calculated dynamically. |
| **Mastery Tracking** | Deterministic mastery rubric requiring both high accuracy ($\ge 80\%$) and pedagogical independence ($\text{assistance} \le \text{Level 1}$). | Mastery is never awarded for high scores achieved through heavy step-by-step assistance. |
| **Teacher Governance** | Multi-tenant dashboards, classroom cohort mastery matrices, deterministic intervention alerts, and multi-format IEP progress reports (JSON, Markdown, Print). | Eduvia does not provide clinical diagnoses, medical classifications, or autonomous educator replacement. |

---

## Document Navigation

* [[00 - MOC/Eduvia Home|Eduvia Knowledge Base Home]]
* Master System Architecture: [[Eduvia Architecture & System Design|Eduvia Architecture & System Design]]
* Personalization & Adaptation: [[Eduvia Learning & Personalization Approach|Eduvia Learning & Personalization Approach]]
* AI & RAG Engineering: [[Eduvia AI & RAG Technical Approach|Eduvia AI & RAG Technical Approach]]
* Accessibility & Cognitive Calm: [[Eduvia Accessibility & Cognitive Calm|Eduvia Accessibility & Cognitive Calm]]
* Security & Privacy: [[Eduvia Security & Privacy Engineering|Eduvia Security & Privacy Engineering]]
* User Workflows: [[Eduvia User Workflows|Eduvia User Workflows]]
* Full Implementation History: [[Eduvia Implementation History — Phases 0–12|Eduvia Implementation History — Phases 0–12]]
* Phase 12 Details: [[05 - Development History/Phase 12 — Production Cloud Deployment & Staging|Phase 12 — Production Cloud Deployment & Staging]]
* Testing & Verification: [[Eduvia Testing & Verification|Eduvia Testing & Verification]]
* Cloud Deployment: [[Eduvia Production & Cloud Deployment|Eduvia Production & Cloud Deployment]]
* Model Context Protocol: [[Eduvia Project MCP|Eduvia Project MCP]]
