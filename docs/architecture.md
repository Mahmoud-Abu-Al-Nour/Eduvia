# Eduvia — System Architecture

## Overview

Eduvia is an adaptive educational web platform designed to support learners with intellectual disabilities and special educational needs.

## Two Separated Learner Experiences

Eduvia provides two clearly separated learner experiences under each Curriculum Objective:

```text
Curriculum Objective
        │
        ├──────────────► Instructional Content
        │                 - Explanation & modeling (visual, step-by-step, worked example, text)
        │                 - Non-evaluative: NO score, NO pass/fail, NO mastery decision
        │                 - Web Speech TTS read-aloud support
        │                 - Direct seamless transition to "Start Practice"
        │
        └──────────────► Practice Activity
                          - Multi-question interactive practice (3–10 questions, default 5)
                          - Homogeneous modality per activity
                          - Per-question authoritative server evaluation & state isolation
                          - Activity-level aggregate scoring and telemetry
                          - Feeds Phase 7 mastery and Phase 8 adaptation engines
```

**Core Principle:**
```
Same Curriculum → Same Learning Objective → Instructional Content (Modeling)
→ Practice Activity (Multi-Question) → Track Performance → Analyze Learning Pattern → Adapt Future Activities
```

---

## System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        TEACHER BROWSER                          │
│                   React + TypeScript + Vite                      │
└─────────────────────────────┬────────────────────────────────────┘
                              │ REST API (JSON)
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────────┐ │
│  │  API Layer  │  │  Core Logic  │  │   AI Orchestrator       │ │
│  │ (REST/v1)   │  │  (Services)  │  │                         │ │
│  └──────┬──────┘  └──────┬───────┘  │  LLM Provider Interface │ │
│         │                │          │         ↓               │ │
│  ┌──────▼──────────────────────────┐│  Gemini Provider        │ │
│  │       Domain Modules            ││                         │ │
│  │  auth │ users │ learners        │└─────────────────────────┘ │
│  │  curriculum │ activities        │                             │
│  │  analytics │ recommendations    │                             │
│  └─────────────────────────────────┘                             │
└────────────────┬──────────────────────────────────────────────────┘
                 │
     ┌───────────┼───────────┐
     ↓           ↓           ↓
┌─────────┐ ┌────────┐ ┌──────────────────┐
│PostgreSQL│ │Qdrant  │ │ Gemini API       │
│(Primary) │ │(Vector)│ │ (External)       │
│          │ │        │ │                  │
│Auth data │ │Know-   │ │Activity genera-  │
│Learners  │ │ledge   │ │tion, strategy    │
│Curriculum│ │RAG     │ │recommendations   │
│Analytics │ │chunks  │ │                  │
└─────────┘ └────────┘ └──────────────────┘
```

---

## Component Architecture

### Frontend Architecture

```
frontend/src/
├── app/                    Application shell, routing
├── components/             Shared UI components
│   ├── ui/                 shadcn/ui primitives
│   └── layout/             Layout components
├── features/               Feature-oriented modules
│   ├── auth/               Authentication (Phase 1)
│   ├── dashboard/          Teacher dashboard (Phase 10)
│   ├── learners/           Learner management (Phase 3)
│   ├── curriculum/         Curriculum management (Phase 2)
│   ├── instructional/      Teacher instructional content studio
│   ├── activities/         Activity engine & multi-step player (Phase 4)
│   ├── learning/           Learner experience & instructional viewer (Phase 5)
│   ├── analytics/          Learning analytics (Phase 7)
│   └── recommendations/    AI recommendations (Phase 8)
├── services/               API client + service layer
├── hooks/                  Custom React hooks
├── types/                  TypeScript type definitions
└── utils/                  Utility functions
```

### Backend Architecture (Modular Monolith)

```
backend/app/
├── api/v1/                 REST API endpoints
├── core/                   Config, logging, errors
├── auth/                   JWT authentication
├── users/                  User management
├── teachers/               Teacher-specific logic
├── learners/               Learner profiles
├── curriculum/             Curriculum engine
├── content/                Authoritative content bank
├── instructional/          Instructional content service & models
├── activities/             Multi-question activity management & evaluation
├── learning/               Active learning sessions
├── analytics/              Performance analytics & telemetry
├── recommendations/        Strategy recommendations
├── ai/
│   ├── orchestrator/       Central AI coordinator
│   ├── providers/          LLM provider abstractions
│   │   ├── base.py         Abstract interface
│   │   └── gemini.py       Gemini implementation
│   ├── generation/         Activity & instructional prompt generation
│   ├── evaluation/         Modality evaluators
│   ├── adaptation/         Adaptation logic (Phase 8)
│   └── strategies/         Strategy selection (Phase 8)
├── knowledge/              RAG + Qdrant client
└── database/               SQLAlchemy + Alembic
```

---

## AI Architecture

### Provider Abstraction

Business logic never calls Gemini directly:

```
Business Logic
      ↓
AIOrchestrator (app/ai/orchestrator/)
      ↓
LLMProvider interface (app/ai/providers/base.py)
      ↓
GeminiProvider (app/ai/providers/gemini.py)
```

Adding a new provider (e.g., OpenAI):
1. Create `app/ai/providers/openai.py`
2. Implement `LLMProvider` interface
3. Register in `get_ai_orchestrator()`

### RAG Architecture (Phase 9)

```
Knowledge Base Documents
         ↓
    Embeddings
         ↓
    Qdrant Collections
         ↓
Semantic Retrieval (query)
         ↓
Retrieved Context Chunks
         ↓
  Gemini + Context → Activity Schema
         ↓
   Pydantic Validation
         ↓
  Structured Activity JSON
```

### 1. Multi-Question Activity Generation Pipeline

```
Curriculum Objective
      +
Learner Profile / Context
      +
Phase 8 Constraints (Modality, Difficulty)
      +
Content Bank (5+ distinct source items)
      +
RAG Pedagogical Context
      ↓
Gemini Structured Generation (or Content Bank Deterministic Fallback)
      ↓
Pydantic Schema Validation (3 <= len(questions) <= 10, default 5)
      ↓
Activity Object with questions[]
      ↓
Multi-Step Activity Player (React)
      ↓
Learner Final Submission (all question answers)
      ↓
Authoritative Per-Question Backend Evaluation
      ↓
ActivityAttempt & Question-Level Telemetry (No Activity Count Inflation)
```

### 2. Instructional Content Generation & Workflow Pipeline

```
Curriculum Objective
      +
Explanation Method (visual_explanation | step_by_step | worked_example | text_explanation)
      +
Content Bank Authoritative Facts
      +
RAG Pedagogical Guidance
      ↓
Gemini Structured Generation (or Deterministic Pedagogical Fallback)
      ↓
Pydantic Validation -> Status: review_required
      ↓
Teacher Studio Review & Editing (/teacher/instructional-content)
      ↓
Teacher Approval (status: approved)
      ↓
Teacher Publication (status: published)
      ↓
Learner Instructional View (/learn/objective/:id/content)
      ↓
Non-Evaluative Learning (TTS, Visual Cues, Step-by-Step, Worked Examples)
      ↓
Direct Action Button: "Start Practice Activity"
```

**IMPORTANT:** Gemini generates structured JSON only. It does NOT generate arbitrary HTML or React code. Correctness, scores, and mastery are authoritatively calculated server-side.

---

## Adaptive Learning Intelligence Engine

```
Adaptive Learning Intelligence Engine
│
├── Learner Profiler         Track modality + strategy effectiveness
├── Learning Analytics       Structured performance event processing
├── Strategy Engine          Select optimal teaching strategy
├── Curriculum Engine        Navigate curriculum objectives
├── Activity Generator       Generate schema-validated activities
├── Activity Evaluator       Score learner responses
├── Adaptation Engine        Decide when/how to adapt
├── Recommendation Engine    Suggest next approach
└── Strategy Explainer       Generate human-readable explanations
```

### Adaptation Hierarchy

```
Level 1: Adjust Difficulty
Level 2: Add Hints / Scaffolding
Level 3: Change Activity Type
Level 4: Change Teaching Strategy
Level 5: Change Modality (requires strong evidence)
```

---

## Data Flow: Learning Loop

```
1. Teacher selects learner + learning objective
2. System retrieves learner profile
3. System retrieves relevant educational knowledge (RAG)
4. AI Orchestrator generates activity (Gemini + context)
5. Activity validated against Pydantic schema
6. Activity rendered in learner interface
7. Learner interacts with activity
8. Performance event recorded (accuracy, time, hints, etc.)
9. Learning Analytics processes event
10. Learner Profile updated
11. Next activity adapts based on updated profile
```

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | React 18 + TypeScript | UI |
| Build Tool | Vite | Fast dev + build |
| Styling | Tailwind CSS | Utility-first CSS |
| Components | shadcn/ui + Radix UI | Accessible primitives |
| Animation | Framer Motion | Micro-animations |
| Backend | FastAPI + Python 3.12 | REST API |
| Validation | Pydantic v2 | Schema validation |
| ORM | SQLAlchemy 2 (async) | Database abstraction |
| Migrations | Alembic | Database versioning |
| Primary DB | PostgreSQL 16 | Source of truth |
| Vector DB | Qdrant | RAG knowledge retrieval |
| AI | Gemini (via abstraction) | Activity generation |
| Logging | structlog | Structured JSON logging |
| Containers | Docker + Compose | Local development |

---

## Development Phases

| Phase | Name | Status |
|-------|------|--------|
| 0 | Project Initialization | ✅ Complete |
| 1 | Database + Authentication | ⬜ Not started |
| 2 | Curriculum | ⬜ Not started |
| 3 | Learner Profiles | ⬜ Not started |
| 4 | Activity Engine | ⬜ Not started |
| 5 | Learner Experience | ⬜ Not started |
| 6 | Performance Tracking | ⬜ Not started |
| 7 | Learning Analytics | ⬜ Not started |
| 8 | Adaptive Engine | ⬜ Not started |
| 9 | Gemini + RAG | ⬜ Not started |
| 10 | Teacher Dashboard | ⬜ Not started |
| 11 | Testing + Accessibility | ⬜ Not started |
| 12 | Deployment | ⬜ Not started |

---

## Security Principles

- All secrets via environment variables — never hardcoded
- JWT authentication for teacher/admin roles
- Learner interface uses teacher-managed sessions (no learner login for MVP)
- AI provider keys stored in environment only
- Database passwords in environment only
- CORS restricted to known origins

---

## Accessibility Principles

- Minimum 16px body text
- Minimum 44×44px touch targets for learner UI
- Focus-visible outlines on all interactive elements
- Reduced motion media query respected
- Semantic HTML structure
- ARIA labels on interactive components
- High contrast ratio compliance (WCAG AA)
