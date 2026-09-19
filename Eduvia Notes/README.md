# Eduvia Notes — Project Knowledge Base & Documentation Vault

> **Comprehensive Engineering, Architectural, and Pedagogical Documentation for the Eduvia Platform**

---

## What is this Directory?

`Eduvia Notes/` is the authoritative knowledge base and documentation vault for **Eduvia**, an adaptive educational platform engineered specifically for learners with special educational needs (SEN).

This directory functions both as a standalone **Obsidian Vault** (utilizing bi-directional wikilinks such as `[[00 - MOC/Eduvia Home|Eduvia Home]]` and hierarchical Maps of Content) and as a structured technical reference for developers, reviewers, supervisors, and evaluators browsing the repository on GitHub or in an IDE.

It thoroughly documents:
* **Product Thesis & Vision**: The core premise of *Standardized Curriculum + Personalized Delivery*.
* **System Architecture**: Modular monolith topology, asynchronous FastAPI backend, React 19 frontend, PostgreSQL 16 relational persistence, and Qdrant vector retrieval.
* **Pedagogical Intelligence**: 5 interactive activity modalities, server-side evaluation authority, dynamic telemetry logging, and the 5-tier deterministic adaptation hierarchy.
* **AI & RAG Engineering**: Bounded Gemini 2.5 Flash integration, evidence-based Universal Design for Learning (UDL) knowledge grounding, and the 100% deterministic local fallback generator (Zero-Strand Guarantee).
* **Accessibility & UX**: First-class WCAG 2.1 AA compliance, assistive switch device keybindings, focus containment, and the Cognitive Calm philosophy.
* **Production Cloud Infrastructure**: Terraform Infrastructure as Code (Cloud Run, Cloud SQL, Secret Manager, Artifact Registry), Docker containerization, and Cloud Build CI/CD.
* **Implementation History**: Chronological milestones, architectural decision logs, and verified test records for all 13 phases (Phases 0 through 12, plus the Eduvia Project MCP server).

---

## Vault Structure & Navigation Map

```text
Eduvia Notes/
│
├── 00 - MOC/                      # Maps of Content (Vault Index & Navigation)
│   ├── Eduvia Home.md             # Primary starting point & knowledge clusters
│   ├── Current Status.md          # Live phase scorecard & verified test status
│   └── Project Map.md             # Closed-loop dataflow & component topology
│
├── 01 - Product/                  # Product Strategy & Requirements
│   ├── Core Principles.md         # Non-negotiable philosophical & pedagogical rules
│   ├── Problem Statement.md       # Special education bottlenecks & the "Modification Trap"
│   ├── Product Vision.md          # Long-term mission & educational impact
│   ├── Solution Overview.md       # End-to-end platform mechanisms
│   └── Target Users.md            # Personas: SEN Learners, Teachers, Administrators
│
├── 02 - Architecture/             # System Architecture & Technical Specifications
│   ├── Accessibility.md           # WCAG 2.1 AA, switch bindings, ARIA live regions
│   ├── Backend Architecture.md    # FastAPI, dependency injection, async patterns
│   ├── Database Architecture.md   # PostgreSQL 16 schema, Alembic migrations, indexes
│   ├── Frontend Architecture.md   # React 19, TypeScript, feature-driven structure
│   ├── Security & Privacy.md      # JWT auth, Bcrypt, rate limiting, multi-tenancy
│   ├── System Architecture.md     # Modular monolith topology & domain boundaries
│   └── Technology Stack.md        # Runtime dependencies, frameworks, and tools
│
├── 03 - AI & Adaptive Learning/   # Intelligent Personalization & GenAI Pipeline
│   ├── Activity Evaluation.md     # Server-side grading & assistance level tracking
│   ├── Activity Generation.md     # Pydantic schemas, prompt builders, fallbacks
│   ├── Adaptive Learning Engine.md# 5-tier deterministic adaptation hierarchy
│   ├── Gemini Integration.md      # Modern google-genai SDK, structured JSON output
│   ├── Learner Profile.md         # Dynamic modality & strategy affinity tracking
│   ├── Learning Analytics.md      # Dynamic mastery rubric & longitudinal progress
│   ├── RAG Knowledge Base.md      # Qdrant vector store, 768-dim embeddings, UUIDv5
│   └── Strategy Engine.md         # Deterministic selection of instructional scaffolding
│
├── 04 - Curriculum/               # Academic Standards & Objectives
│   ├── Curriculum Architecture.md # 5-level relational hierarchy (Subject → Objective)
│   ├── Curriculum Localization.md # Multilingual JSONB schema (EN/AR)
│   ├── Curriculum Progression.md  # Prerequisite DAG & dependency resolution
│   └── Learning Objectives.md     # Measurable targets, difficulties, rubrics
│
├── 05 - Development History/      # Historical Records & Milestone Gates
│   ├── Changelog.md               # Chronological platform change log
│   ├── Eduvia Development History.md # Detailed decision log & verified test milestones
│   ├── Phase 0 - Initialization.md ... Phase 12 — Production Cloud Deployment.md
│   └── Reports/                   # Detailed phase implementation audit reports
│       ├── Phase 04 Report.md ... Phase 12 Report.md
│
├── 06 - Decisions/                # Architecture Decision Records (ADRs)
│   ├── AI Decisions.md            # Bounded AI rules, no autonomous decision-making
│   ├── Architecture Decisions.md  # Modular monolith, asyncpg, Qdrant vs relational
│   └── Product Decisions.md       # Web MVP scope, non-authenticated learner sessions
│
├── 07 - Roadmap/                  # Execution Planning & Future Horizons
│   ├── Development Roadmap.md     # 13-phase master execution plan
│   ├── MVP Scope.md               # Boundaried pilot release scope
│   └── Future Phases.md           # Post-Phase 12 evolutionary roadmap
│
└── 🌟 Master Technical Documents (Root Level)
    ├── Eduvia Project Overview & Technical Abstract.md
    ├── Eduvia Architecture & System Design.md
    ├── Eduvia Learning & Personalization Approach.md
    ├── Eduvia AI & RAG Technical Approach.md
    ├── Eduvia Accessibility & Cognitive Calm.md
    ├── Eduvia Security & Privacy Engineering.md
    ├── Eduvia User Workflows.md
    ├── Eduvia Implementation History — Phases 0–12.md
    ├── Eduvia Testing & Verification.md
    ├── Eduvia Production & Cloud Deployment.md
    └── Eduvia Project MCP.md
```

---

## 📖 Recommended Reading Guide

Depending on your role and focus, start with the following entry points:

### For Technical Reviewers & Evaluators
1. **[Eduvia Project Overview & Technical Abstract](Eduvia%20Project%20Overview%20&%20Technical%20Abstract.md)**: High-level abstract, technical stack summary, and core deliverables.
2. **[Eduvia Architecture & System Design](Eduvia%20Architecture%20&%20System%20Design.md)**: Modular monolith topology, domain boundaries, and persistence model.
3. **[Eduvia Testing & Verification](Eduvia%20Testing%20&%20Verification.md)**: Automated test breakdown across the 217 backend tests, 13 frontend tests, and 35 MCP tests.
4. **[Current Status](00%20-%20MOC/Current%20Status.md)**: Up-to-date milestone scorecard verifying that Phases 0 through 12 and the MCP server are completely locked.

### For Software Engineers & Contributors
1. **[Eduvia Learning & Personalization Approach](Eduvia%20Learning%20&%20Personalization%20Approach.md)**: Modality schemas, server-side grading rules, and telemetry models.
2. **[Eduvia AI & RAG Technical Approach](Eduvia%20AI%20&%20RAG%20Technical%20Approach.md)**: Prompt engineering, Qdrant vector retrieval, and fallback mechanisms.
3. **[Eduvia Production & Cloud Deployment](Eduvia%20Production%20&%20Cloud%20Deployment.md)**: Terraform files, Cloud Run configurations, Dockerfiles, and CI/CD pipelines.
4. **[Eduvia Project MCP](Eduvia%20Project%20MCP.md)**: Developer tooling instructions for running the Model Context Protocol server.

### For Educators & Pedagogical Supervisors
1. **[Problem Statement](01%20-%20Product/Problem%20Statement.md)**: The educational challenges Eduvia addresses.
2. **[Eduvia Accessibility & Cognitive Calm](Eduvia%20Accessibility%20&%20Cognitive%20Calm.md)**: Sensory accommodation features and WCAG 2.1 AA accessibility.
3. **[Eduvia User Workflows](Eduvia%20User%20Workflows.md)**: Teacher and learner workflows, including classroom cohort management and IEP progress reporting.

---

## 🛠️ How to Use This Knowledge Base

### Viewing in Obsidian
1. Open the [Obsidian](https://obsidian.md/) application.
2. Select **"Open folder as vault"**.
3. Choose the `Eduvia Notes` folder inside this repository.
4. Start exploring from **`00 - MOC/Eduvia Home.md`** or open the Graph View to visualize the interconnected concepts.

### Viewing in an IDE or GitHub
Every file is standard GitHub-Flavored Markdown. While bi-directional wikilinks (such as `[[00 - MOC/Eduvia Home|Eduvia Home]]`) are optimized for Obsidian, all markdown files can be read seamlessly in GitHub, VS Code, or any markdown editor. All master documents at the root level include relative links to their respective deep-dive topics.
