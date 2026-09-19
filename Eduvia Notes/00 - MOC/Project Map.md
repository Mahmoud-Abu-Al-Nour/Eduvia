# Eduvia Project Map

This document illustrates the operational flows and system boundaries connecting all components of the Eduvia platform.

---

## 1. The Adaptive Learning Closed Loop

Eduvia continuously measures interaction telemetry to calibrate future pedagogical delivery without mutating the underlying curriculum:

```text
       ┌────────────────────────────────────────────────────────┐
       │             Standardized Curriculum                    │
       │    (Curriculum → Subject → Unit → Lesson → Objective)  │
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
       │               Activity Evaluator                       │
       │        (Accuracy, Attempts, Time, Assistance Level)     │
       └──────────────────────────┬─────────────────────────────┘
                                  │ Performance Events
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │               Learning Analytics Engine                │
       │         (Mastery Calculation, Evidence Counting)       │
       └──────────────────────────┬─────────────────────────────┘
                                  │ Updated Metrics
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │             Learner Profile Evolution                  │
       │       (Updated Weights & Adaptation Triggers)          │
       └────────────────────────────────────────────────────────┘
```

---

## 2. Technical Component Map

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
│  │     /health          /auth          /users         /curricula         │  │
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
│  │  │  LLMProvider (Gemini Base)   │    │ EduViaQdrantClient (Vector) │  │  │
│  │  └──────────────────────────────┘    └─────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────┬─────────────────────────────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
       ┌─────────────────────────┐             ┌─────────────────────────┐
       │   PostgreSQL Database   │             │      Qdrant Vector      │
       │   - users               │             │   - eduvia_knowledge    │
       │   - curricula           │             │   - eduvia_curriculum   │
       │   - subjects, units     │             └─────────────────────────┘
       │   - lessons, objectives │
       │   - prerequisites       │
       └─────────────────────────┘
```

---

## 3. Cross-Cutting Standards

1. **Strict Role Separation**: Teachers/Admins authenticate with JWT; Learners are managed through localized non-authenticated sessions in MVP.
2. **Deterministic Adaptation**: Pedagogical decisions use strict mathematical and logical rules; Gemini is strictly a generative engine for content.
3. **Resilience**: Optional external services (Qdrant, Gemini) gracefully degrade if credentials are absent during local testing.
