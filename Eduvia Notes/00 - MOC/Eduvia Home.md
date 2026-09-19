# Eduvia Knowledge Base

> **Standardized Curriculum + Personalized Delivery**

Welcome to the central knowledge repository for **Eduvia**, an adaptive educational platform engineered specifically for learners with special educational needs (SEN). Eduvia ensures that all learners access the same rigorous academic curriculum while adapting instructional delivery, scaffolding, modalities, and teaching strategies to individual cognitive profiles.

---

## 🗺️ Navigation & Map of Content

### [[00 - MOC/Project Map|Project Map]]
High-level conceptual, architectural, and lifecycle overview of the system.

### [[00 - MOC/Current Status|Current Status]]
Live development status, verified milestone checkpoints, and current readiness.

---

## 📚 Core Knowledge Clusters

### 1. [[01 - Product/Product Vision|Product & Strategy]]
- [[01 - Product/Product Vision|Product Vision]] — Core thesis, goals, and long-term educational impact
- [[01 - Product/Problem Statement|Problem Statement]] — Shortcomings of one-size-fits-all special education
- [[01 - Product/Solution Overview|Solution Overview]] — High-level platform mechanisms and workflow
- [[01 - Product/Target Users|Target Users]] — Personas: Teachers, Admins, and SEN Learners
- [[01 - Product/Core Principles|Core Principles]] — Non-negotiable philosophical and pedagogical rules

### 2. [[02 - Architecture/System Architecture|System Architecture]]
- [[02 - Architecture/System Architecture|System Architecture]] — Modular monolith, boundaries, and data flow
- [[02 - Architecture/Technology Stack|Technology Stack]] — React 19, FastAPI, PostgreSQL 16, Qdrant, Docker
- [[02 - Architecture/Backend Architecture|Backend Architecture]] — Layered domain design, dependency injection, async patterns
- [[02 - Architecture/Frontend Architecture|Frontend Architecture]] — Feature-driven structure, token handling, Tailwind CSS v4
- [[02 - Architecture/Database Architecture|Database Architecture]] — PostgreSQL schema, Alembic migration chain, indexing
- [[02 - Architecture/Security & Privacy|Security & Privacy]] — JWT authentication, zero-secret policy, learner data privacy
- [[02 - Architecture/Accessibility|Accessibility (a11y)]] — WCAG 2.1 AA compliance, keyboard navigation, neurodivergent UI

### 3. [[03 - AI & Adaptive Learning/Adaptive Learning Intelligence Engine|AI & Adaptive Learning]]
- [[03 - AI & Adaptive Learning/Adaptive Learning Intelligence Engine|Adaptive Learning Intelligence Engine]] — Orchestration layer and module breakdown
- [[03 - AI & Adaptive Learning/Learner Profile|Learner Profile]] — Dynamic modality and strategy affinity tracking
- [[03 - AI & Adaptive Learning/Learning Analytics|Learning Analytics]] — Measurable engagement, error analysis, and progression metrics
- [[03 - AI & Adaptive Learning/Strategy Engine|Strategy Engine]] — Deterministic ranking of pedagogical interventions
- [[03 - AI & Adaptive Learning/Activity Generation|Activity Generation]] — Strict structured JSON schemas and validation pipeline
- [[03 - AI & Adaptive Learning/Activity Evaluation|Activity Evaluation]] — Real-time performance tracking and rubric grading
- [[03 - AI & Adaptive Learning/RAG Knowledge Base|RAG Knowledge Base]] — Pedagogical and SEN evidence repository in Qdrant
- [[03 - AI & Adaptive Learning/Gemini Integration|Gemini Integration]] — LLM abstraction boundary and prompt design

### 4. [[04 - Curriculum/Curriculum Architecture|Curriculum & Objectives]]
- [[04 - Curriculum/Curriculum Architecture|Curriculum Architecture]] — 5-tier relational educational hierarchy
- [[04 - Curriculum/Learning Objectives|Learning Objectives]] — Measurable mastery targets, difficulty, assessment criteria
- [[04 - Curriculum/Curriculum Progression|Curriculum Progression]] — Prerequisite graph and dependency resolution
- [[04 - Curriculum/Curriculum Localization|Curriculum Localization]] — Native multi-lingual JSONB schema (EN/AR)

### 5. [[05 - Development History/Eduvia Development History|Development History & Verification]]
- [[05 - Development History/Eduvia Development History|Eduvia Development History]] — Master chronological history, decision log & verification milestones
- [[05 - Development History/Phase 0 - Initialization|Phase 0 — Project Initialization]]
- [[05 - Development History/Phase 1 - Database & Authentication|Phase 1 — Database & Authentication]]
- [[05 - Development History/Phase 1 - Verification|Phase 1 — Verification Report]]
- [[05 - Development History/Phase 2 - Curriculum|Phase 2 — Curriculum & Learning Objectives]]
- [[05 - Development History/Phase 2 - Integration Verification|Phase 2 — Integration Verification]]
- [[05 - Development History/Phase 03 — Learner Profile|Phase 03 — Learner Profile & Domain Entity]]
- [[05 - Development History/Phase 04 — Activity Generation Engine|Phase 04 — Activity Generation Engine]]
- [[05 - Development History/Phase 05 — Learner Experience & Activity Interaction|Phase 05 — Learner Experience & Activity Interaction]]
- [[05 - Development History/Phase 06 — Performance Tracking & Telemetry|Phase 06 — Performance Tracking & Telemetry]]
- [[05 - Development History/Phase 07 — Learner Analytics & Mastery Tracking|Phase 07 — Learner Analytics & Mastery Tracking]]
- [[05 - Development History/Changelog|Master Project Changelog]]

### 6. [[06 - Decisions/Architecture Decisions|Decisions & Governance]]
- [[06 - Decisions/Architecture Decisions|Architecture Decisions (ADRs)]] — Modular monolith, Qdrant, JWT, asyncpg
- [[06 - Decisions/Product Decisions|Product Decisions]] — Web MVP, non-authenticated learners, 5 initial activity types
- [[06 - Decisions/AI Decisions|AI Decisions]] — Generative boundaries, deterministic adaptations, no autonomous decisions
- [[06 - Decisions/Open Questions|Open Questions]] — Active questions requiring research, validation, or user agreement

### 7. [[07 - Roadmap/Development Roadmap|Roadmap & Scope]]
- [[07 - Roadmap/Development Roadmap|Development Roadmap]] — 13-phase master execution plan
- [[07 - Roadmap/MVP Scope|MVP Scope]] — Boundaried features included in the pilot release
- [[07 - Roadmap/Future Phases|Future Phases]] — Phase 3 through Phase 12 roadmap
