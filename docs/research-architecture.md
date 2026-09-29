# Eduvia Research Mode: Architectural Specification

## 1. System Architecture Diagram

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Eduvia Unified Platform                         │
├──────────────────────────────────┬─────────────────────────────────────┤
│      PRODUCTION SUBSYSTEM        │          RESEARCH SANDBOX           │
├──────────────────────────────────┼─────────────────────────────────────┤
│ User Roles:                      │ User Roles:                         │
│ • TEACHER                        │ • RESEARCHER                        │
│ • LEARNER                        │ • ADMIN (Platform Governance)       │
│                                  │                                     │
│ Generation Pipeline:             │ Generation Pipeline:                │
│ Curriculum Objective             │ Researcher Custom Prompt            │
│       ↓                          │       +                             │
│ Content Bank (Deduplication)     │ Experimental Hyperparameters        │
│       ↓                          │       +                             │
│ Qdrant Vector RAG                │ Explicit Context (Manual Only)      │
│       ↓                          │       ↓                             │
│ Phase 8 Learner Adaptation       │ Direct Gemini LLM Provider          │
│       ↓                          │       ↓                             │
│ Gemini 2.5 Flash                 │ Raw LLM Output + Normalized Payload │
│       ↓                          │       ↓                             │
│ Validated Production Activity    │ Immutable Research Artifact         │
│ (Strict Homogeneous 3-10 Qs)     │ (Multi-question / Mixed Modalities) │
│       ↓                          │       ↓                             │
│ Active Learner Session           │ Comparative Matrix & Human Eval     │
│                                  │       ↓ (Explicit Admin Promotion)  │
│                                  │ Production Draft Queue              │
└──────────────────────────────────┴─────────────────────────────────────┘
```

---

## 2. Decoupling & Isolation Principles

### Principle 1: RAG Boundary Isolation
In Research Mode, the vector database client (`QdrantClient`) and knowledge retriever (`EduviaKnowledgeRetriever`) are **never called**.
- Production collection: `eduvia_knowledge`
- Research mode default: `RAG = OFF`.
- No embeddings are calculated, and no semantic similarity checks are injected into the research prompt.

### Principle 2: Content Bank & Curriculum Isolation
- Production activity generation queries the database for existing exercises matching `curriculum_objective_id`.
- Research Mode generation operates independently of curriculum hierarchies. Prompts are freeform and can address any grade, concept, or interdisciplinary subject without curriculum foreign keys.

### Principle 3: Learner Privacy & Zero Adaptation Contamination
- Research Mode does NOT access learner records (`LearnerProfile`, `ObservationEvidence`, `SensoryPreferences`).
- The Phase 8 adaptation engine (`AdaptationEngine.build_recommendation`) is completely bypassed.
- No learner identities or performance telemetry are leaked to the experimental sandbox.

---

## 3. Component Architecture

### 3.1 Backend Modules (`backend/app/research/`)

1. **`models.py`**:
   - `ResearchProject`: Top-level organizational unit with hypothesis and owner ID.
   - `ResearchExperiment`: Pedagogical experiment investigating a specific variable.
   - `ResearchVariant`: Distinct condition (configuration stored as JSONB for dynamic hyperparameter tracking).
   - `ResearchRun`: Execution instance capturing exact prompt, system prompt, temperature, tokens, raw output, and status.
   - `ResearchArtifact`: Generated educational asset with JSON or text payload, metadata, and optional compatibility flags.
   - `ResearchMetric`: Custom scoring dimension defined per experiment.
   - `ResearchEvaluation`: Continuous rating and qualitative notes assigned to an artifact.
   - `ResearchSnapshot`: Read-only, immutable capture of production references for baseline benchmarking.

2. **`generation.py` (`ResearchGenerationService`)**:
   - Direct, unconstrained interface to `GeminiProvider`.
   - Assembles minimal context: `prompt + system_prompt + explicit_context`.
   - Never alters model responses; preserves both `raw_output` and `normalized_payload`.
   - Provides optional schema validation (`validate_production_compatibility`).

3. **`service.py` (`ResearchService`)**:
   - Implements strict ownership verification and IDOR prevention (`check_access`).
   - Lineage preservation for variant cloning (`parent_variant_id`) and run re-execution (`parent_run_id`).
   - Tabular and markdown report export formatters.
   - Admin-gated promotion to Production Draft (`promote_artifact_to_production_draft`).

4. **`router.py`**:
   - Dedicated FastAPI router under `/api/v1/research`.
   - Guarded by `get_current_active_researcher` dependency (permits `researcher` and `admin`).

---

## 4. Lineage and Reproducibility

Every experiment variant can be cloned into descendant variants, capturing lineage:
```text
Variant A (Baseline 0.3 Temp)
    └── Variant A.1 (Cloned, 0.7 Temp, parent_variant_id="var-a")
            └── Variant A.2 (Cloned, 1.0 Temp, parent_variant_id="var-a.1")
```
Every completed `ResearchRun` permanently stores:
- Model name and configuration dictionary
- User prompt and system prompt
- Explicit manual context snapshot
- Execution timestamp and latency
- Complete raw LLM output text

This guarantees that every finding can be audited, cited, and re-executed with complete fidelity.
