# Eduvia — System Architecture

## Overview

Eduvia is an adaptive educational web platform designed to support learners with intellectual disabilities and special educational needs.

**Core Principle:**
```
Same Curriculum → Same Learning Objective → Different Delivery Method
→ Track Performance → Analyze Learning Pattern → Adapt Future Activities
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
│   ├── activities/         Activity engine (Phase 4)
│   ├── learning/           Learner experience (Phase 5)
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
├── activities/             Activity management
├── learning/               Active learning sessions
├── analytics/              Performance analytics
├── recommendations/        Strategy recommendations
├── ai/
│   ├── orchestrator/       Central AI coordinator
│   ├── providers/          LLM provider abstractions
│   │   ├── base.py         Abstract interface
│   │   └── gemini.py       Gemini implementation
│   ├── generation/         Activity generation (Phase 9)
│   ├── evaluation/         Response evaluation (Phase 9)
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

### Activity Generation Pipeline

```
Curriculum Objective
      +
Learner Profile
      +
RAG Knowledge Context
      ↓
Gemini Structured Generation
      ↓
Pydantic Schema Validation
      ↓
React Activity Renderer
```

**IMPORTANT:** Gemini generates structured JSON only. It does NOT generate arbitrary HTML or React code.

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
