# Eduvia Project Map

This document illustrates the operational flows, architectural boundaries, and lifecycle stages connecting all components of the Eduvia platform.

---

## 🌟 Master System Documents

For complete, deep architectural and pedagogical specifications, consult the master documents:

* **[[Eduvia Project Overview & Technical Abstract|Project Overview & Technical Abstract]]** — Executive summary, core thesis, and full-stack technical abstract.
* **[[Eduvia Architecture & System Design|Architecture & System Design]]** — Modular monolith topology, domain boundaries, relational/vector persistence, and API gateway.
* **[[Eduvia Learning & Personalization Approach|Learning & Personalization Approach]]** — Modality design, server-side evaluation, dynamic telemetry, and deterministic adaptation hierarchy.
* **[[Eduvia AI & RAG Technical Approach|AI & RAG Technical Approach]]** — Bounded Gemini 2.5 Flash, Qdrant RAG pipeline, UUIDv5 deduplication, and Zero-Strand fallback guarantee.
* **[[Eduvia Accessibility & Cognitive Calm|Accessibility & Cognitive Calm]]** — WCAG 2.1 AA hardening, switch device bindings, focus trapping, and calm sensory design.
* **[[Eduvia Security & Privacy Engineering|Security & Privacy Engineering]]** — JWT auth, Bcrypt, multi-tenant teacher scoping, sliding-window rate limiting, and zero-secret policy.
* **[[Eduvia User Workflows|User Workflows]]** — Dual lifecycle for special educators (cohorts, alerts, IEP reports) and sensory-attuned learners.
* **[[Eduvia Implementation History — Phases 0–12|Implementation History (Phases 0–12)]]** — Master progression matrix, lockpoint commits, and verification milestones.
* **[[Eduvia Testing & Verification|Testing & Verification]]** — Quality assurance hierarchy, 217 backend tests, 13 frontend tests, and 35 MCP tests.
* **[[Eduvia Production & Cloud Deployment|Production & Cloud Deployment]]** — Terraform GCP infrastructure (Cloud Run, Cloud SQL, Secret Manager) and automated migration runner.
* **[[05 - Development History/Phase 12 — Production Cloud Deployment & Staging|Phase 12 — Production Cloud Deployment & Staging]]** — Phase 12 milestone history, containerization, and IaC validation.
* **[[Eduvia Project MCP|Eduvia Project MCP]]** — Model Context Protocol developer server (11 tools, stdio & Streamable HTTP transports).

---

## 1. The Adaptive Learning Closed Loop

Eduvia continuously measures interaction telemetry to calibrate future pedagogical delivery without mutating the underlying curriculum:

```text
       ┌────────────────────────────────────────────────────────┐
       │             Standardized Curriculum                    │
       │    (Subject → Grade → Domain → Topic → Objective)      │
       └──────────────────────────┬─────────────────────────────┘
                                  │ Target Objective
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │                 Learner Profile                        │
       │   (Modality Scores, Strategy Scores, Confidence, Hist) │
       └──────────────────────────┬─────────────────────────────┘
                                  │ Profile State
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │             Strategy Engine & RAG Retrieval            │
       │     (Deterministic Selector + Qdrant Pedagogical Base) │
       └──────────────────────────┬─────────────────────────────┘
                                  │ Selected Strategy + Modality
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │                Activity Generator                      │
       │  (Gemini LLM Provider → Strict JSON Schema Validation) │
       │  (100% Deterministic Fallback / Zero-Strand Guarantee) │
       └──────────────────────────┬─────────────────────────────┘
                                  │ Validated Activity JSON
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │                Learner Experience (UI)                 │
       │      (5 Activity Types + TTS + Distraction-Free UX)    │
       └──────────────────────────┬─────────────────────────────┘
                                  │ Interaction Telemetry
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │               Activity Evaluator (Server)              │
       │        (Accuracy, Attempts, Time, Assistance Level)     │
       └──────────────────────────┬─────────────────────────────┘
                                  │ Performance Events
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │               Learning Analytics Engine                │
       │  (Dynamic Mastery Rubric: Accuracy >= 80% & Assist<=1) │
       └──────────────────────────┬─────────────────────────────┘
                                  │ Updated Metrics
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │             Deterministic Adaptation Engine            │
       │       (Prerequisite Step-Back & Difficulty Scaling)    │
       └────────────────────────────────────────────────────────┘
```

---

## 2. Technical Component Topology

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                             Frontend (React 19)                             │
│                                                                             │
│  ┌──────────────────────┐  ┌───────────────────────┐  ┌──────────────────┐ │
│  │   Auth / Protected   │  │   Curriculum Browser  │  │   Teacher View   │ │
│  │    Context & Views   │  │    (5-Level Nav)      │  │    Dashboard     │ │
│  └──────────┬───────────┘  └──────────┬────────────┘  └────────┬─────────┘ │
│             │                         │                        │           │
│             └─────────────────────────┼────────────────────────┘           │
│                                       ▼                                     │
│                     Centralized API Service (Axios Client)                 │
│               - Bearer Token Interceptor (`eduvia_access_token`)           │
│               - Normalized Error Handling                                  │
└───────────────────────────────────────┬─────────────────────────────────────┘
                                        │ HTTP / JSON REST API
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             Backend (FastAPI)                               │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                           API v1 Router                               │  │
│  │     /health          /auth          /users         /curriculum        │  │
│  │     /learners        /activities    /analytics     /recommendations   │  │
│  │     /teacher-dashboard                                                │  │
│  └────────┬───────────────┬───────────────┬────────────────┬─────────────┘  │
│           │               │               │                │                │
│           ▼               ▼               ▼                ▼                │
│  ┌─────────────────┐ ┌─────────┐ ┌────────────────┐ ┌────────────────────┐  │
│  │ Health Checker  │ │  OAuth2 │ │  UserService   │ │ CurriculumService  │  │
│  │ (Detailed Deps) │ │   JWT   │ │  (Admin/Teach) │ │ (Hierarchy/PreReq) │  │
│  └─────────────────┘ └─────────┘ └────────────────┘ └────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                 AI Orchestrator & Knowledge Subsystem                 │  │
│  │  ┌──────────────────────────────┐    ┌─────────────────────────────┐  │  │
│  │  │  LLMProvider (Gemini GenAI)  │    │ Qdrant Vector Client (768)  │  │  │
│  │  └──────────────────────────────┘    └─────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────┬─────────────────────────────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
       ┌─────────────────────────┐             ┌─────────────────────────┐
       │   PostgreSQL Database   │             │      Qdrant Vector      │
       │   - users, learners     │             │   - eduvia_knowledge    │
       │   - curricula, prereqs  │             │   - eduvia_curriculum   │
       │   - learner_profiles    │             └─────────────────────────┘
       │   - performance_events  │
       │   - activity_attempts   │
       └─────────────────────────┘
```

---

## 3. Cross-Cutting Standards & Invariants

1. **Strict Role Separation & Multi-Tenancy**: Teachers authenticate with JWT; Learners are managed through localized sessions; Teachers only access assigned cohorts.
2. **Deterministic Adaptation**: Pedagogical decisions use strict mathematical and logical rules; Gemini is strictly a generative engine for content.
3. **Zero-Strand Guarantee**: Deterministic local fallback generator produces schema-compliant activities if external AI APIs are unreachable.
4. **Authoritative Server Evaluation**: All answers, scores, and assistance metrics are graded server-side.
5. **Zero Speculative Tables**: Dynamic metric synthesis from immutable event logs prevents synchronization drift.
