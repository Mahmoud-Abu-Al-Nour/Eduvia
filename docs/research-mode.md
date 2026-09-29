# Eduvia Research Mode: Overview & Operator Guide

## 1. Executive Summary & Purpose

Eduvia's **Research Mode / Research Sandbox** provides authorized researchers with an isolated, highly flexible experimentation environment. Researchers can explore educational content generation, novel instructional approaches, experimental assessment architectures (mixed question types, arbitrary item counts), and custom prompt configurations without being constrained by Eduvia's production learning delivery pipeline.

---

## 2. Core Principle: Sandbox vs Production Delivery

| Attribute | Production Delivery System | Research Mode Sandbox |
| :--- | :--- | :--- |
| **Objective** | Controlled, adapted learning delivery to students | Free exploration, hypothesis testing, and benchmarking |
| **Audience** | Learners and Classroom Teachers | Educational researchers and platform architects |
| **Curriculum Source** | Bound to production curriculum hierarchy | Unconstrained (synthetic, manual, or optional snapshot) |
| **RAG / Knowledge Base** | Injected via Qdrant (`eduvia_knowledge`) | **OFF by default** (zero automatic RAG queries) |
| **Content Bank** | Mandatory query & deduplication checks | **OFF by default** |
| **Learner Adaptation** | Phase 8 adaptive decision engine + learner profiles | **OFF by default** (no learner profiles or analysis) |
| **Artifact Lifecycle** | Published directly to learner practice sessions | Kept isolated as Research Artifacts; requires explicit admin promotion |
| **Question Constraints**| Homogeneous activities (3–10 questions) | Arbitrary question counts (1–50+), mixed modalities, freeform text |

---

## 3. The Research Workflow

```text
RESEARCHER
    ↓
Research Project (Hypothesis & Research Question)
    ↓
Experiment (Specific pedagogical variable under test)
    ↓
Variants (A, B, C... e.g., Worked Example vs Socratic vs Visual)
    ↓
Prompt Studio (Direct LLM generation with custom parameters)
    ↓
Gemini 2.5 Flash / Pro (Direct inference without production wrappers)
    ↓
Research Run + Research Artifact (Raw & structured outputs preserved)
    ↓
Comparative Analysis & Manual Metric Evaluation
    ↓
Export / Optional Admin Promotion to Production Draft
```

---

## 4. Prompt Studio Guide

The Prompt Studio is the primary experimentation workbench. It enables researchers to:

1. **Select / Create Experimental Variants**: Assign runs to distinct variant buckets for side-by-side comparison.
2. **Choose Output Targets**:
   - `freeform`: Open-ended explanations, pedagogical notes, research syntheses.
   - `instructional_content`: Narrative lessons, multi-modal instructional steps.
   - `question_set`: Item banks, formative probes, rubric items.
   - `activity`: Interactive exercises with custom question counts and mixed types.
   - `assessment`: Multi-section diagnostic exams with weighting.
   - `curriculum`: Scope-and-sequence outlines and learning trajectory maps.
   - `lesson_plan`: Teacher scripts, scaffolding guidelines, and pacing cues.
3. **Configure Hyperparameters**:
   - Model selection (`gemini-3.8-flash` [default], `gemini-3.5-flash-lite`, `gemini-2.5-flash`, `gemini-2.5-pro` from canonical catalog)
   - Temperature slider (`0.0` deterministic to `1.0` creative)
   - Max output tokens (`512` to `8192`)
   - Optional research system instructions
4. **Supply Manual Context**: Paste excerpts, research citations, or experimental stimuli directly into the prompt without triggering vector database lookups.
5. **Optional Production Compatibility Validation**: Verify whether an experimental artifact adheres to production schemas (`activity`, `instructional_content`) without modifying or truncating the research output.

---

## 5. Comparative Evaluation Framework

Research Mode does not rely on opaque "auto-judges" or biased single scores:
- **Custom Metrics**: Define experiment-specific evaluation metrics (e.g., *Cognitive Load*, *Scaffolding Depth*, *Lexical Simplicity*, *Distractor Plausibility*).
- **Human Evaluation**: Researchers score variants on continuous 1–5 scales and provide detailed qualitative notes.
- **Side-by-Side Matrix**: Compare prompt, system prompt, temperature, raw token count, execution latency, and metric averages across Variants A, B, and C simultaneously.

---

## 6. Access Control & Demo Credentials

Research Mode is strictly protected by role-based access control (RBAC):
- **Researcher Role** (`UserRole.researcher`): Complete access to create and manage own projects, experiments, variants, prompt studio runs, and evaluations.
- **Admin Role** (`UserRole.admin`): Platform-wide visibility and administrative authority to promote approved artifacts to Production Draft status.
- **Teacher & Learner Roles**: **Zero access** to Research Mode routes (`/research/*`) or API endpoints (`/api/v1/research/*`). Attempts return HTTP 403 Forbidden.

### Demo Accounts
- **Researcher**: `researcher@eduvia.app` (Password: `researcherpassword123`)
- **Admin**: `admin@eduvia.app` (Password: `adminpassword123`)
