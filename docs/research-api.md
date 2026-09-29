# Eduvia Research Mode: API Reference

All research endpoints are prefixed with `/api/v1/research` and require Bearer token authentication with either `researcher` or `admin` role.

---

## 1. Research Projects

### `GET /api/v1/research/projects`
List all research projects owned by the authenticated researcher (or all projects if admin).
- **Status**: `200 OK`
- **Response**: `List[ResearchProjectRead]`

### `POST /api/v1/research/projects`
Create a new research project.
- **Status**: `201 Created`
- **Request Body**:
  ```json
  {
    "name": "Adaptive Scaffolding in Fractions",
    "description": "Investigating worked-example fading vs direct retrieval practice",
    "research_question": "Does dynamic hint fading increase transfer test accuracy?",
    "hypothesis": "Learners receiving faded worked examples will outperform retrieval-only by 15%."
  }
  ```
- **Response**: `ResearchProjectRead`

### `GET /api/v1/research/projects/{project_id}`
Retrieve project details and its child experiments.
- **Status**: `200 OK`
- **Response**: `ResearchProjectRead`

### `PATCH /api/v1/research/projects/{project_id}`
Update project title, description, or status (`draft`, `active`, `completed`, `archived`).
- **Status**: `200 OK`
- **Response**: `ResearchProjectRead`

### `DELETE /api/v1/research/projects/{project_id}`
Permanently delete project and its cascade hierarchy.
- **Status**: `204 No Content`

---

## 2. Experiments & Variants

### `POST /api/v1/research/projects/{project_id}/experiments`
Create an experiment within a project.
- **Status**: `201 Created`
- **Request Body**:
  ```json
  {
    "name": "Exp 1: Visual vs Textual Representations",
    "research_question": "Does visual fraction bar identification improve subsequent ordering speed?",
    "hypothesis": "Visual grounding accelerates ordering tasks.",
    "description": "Testing visual ordering questions vs numeric multiple choice."
  }
  ```
- **Response**: `ResearchExperimentRead`

### `GET /api/v1/research/experiments/{experiment_id}`
Retrieve experiment details and list of variants.
- **Status**: `200 OK`
- **Response**: `ResearchExperimentRead`

### `POST /api/v1/research/experiments/{experiment_id}/variants`
Add a new experimental condition/variant.
- **Status**: `201 Created`
- **Request Body**:
  ```json
  {
    "name": "Variant A: Concrete Fraction Bars",
    "description": "Visual identification with tap-to-match",
    "configuration": {
      "modality": "visual_identification",
      "question_count": 8,
      "scaffolding": "high"
    }
  }
  ```
- **Response**: `ResearchVariantRead`

### `POST /api/v1/research/variants/{variant_id}/clone`
Clone an existing variant, capturing parent lineage.
- **Status**: `201 Created`
- **Request Body**:
  ```json
  {
    "new_name": "Variant A (High Temp Clone)",
    "configuration_override": {
      "temperature": 0.95
    }
  }
  ```
- **Response**: `ResearchVariantRead` (`parent_variant_id` populated)

---

## 3. Prompt Studio & Generation

### `POST /api/v1/research/prompt-studio/execute`
Execute direct unconstrained LLM generation within a project and variant.
- **Status**: `200 OK`
- **Request Body**:
  ```json
  {
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "experiment_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "variant_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "prompt": "Create an experimental 15-question mixed assessment on ecosystems.",
    "system_prompt": "You are an educational assessment researcher.",
    "output_target": "assessment",
    "model": "gemini-2.5-flash",
    "model_configuration": {
      "temperature": 0.7,
      "max_output_tokens": 4096
    },
    "explicit_context": {
      "manual_context": "Focus on trophic levels, biomass pyramids, and nitrogen cycles."
    },
    "production_compatibility_mode": false
  }
  ```
- **Response**: `ResearchRunRead` (includes child `ResearchArtifactRead`, `raw_output`, and execution metadata).

### `POST /api/v1/research/runs/{run_id}/clone`
Re-run a historical execution with optional hyperparameter overrides.
- **Status**: `201 Created`
- **Request Body**:
  ```json
  {
    "temperature_override": 0.2
  }
  ```
- **Response**: `ResearchRunRead` (`parent_run_id` populated)

---

## 4. Artifacts, Evaluations & Promotion

### `GET /api/v1/research/artifacts/{artifact_id}`
Retrieve a research artifact including structured JSON payload and raw LLM text.
- **Status**: `200 OK`
- **Response**: `ResearchArtifactRead`

### `POST /api/v1/research/artifacts/{artifact_id}/evaluations`
Submit a researcher evaluation for an artifact.
- **Status**: `201 Created`
- **Request Body**:
  ```json
  {
    "metric_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "value": 4.5,
    "evaluator_type": "manual",
    "notes": "Excellent distractors and clean cognitive progression."
  }
  ```
- **Response**: `ResearchEvaluationRead`

### `GET /api/v1/research/experiments/{experiment_id}/compare`
Get comparative analysis matrix across all variants and recent runs in an experiment.
- **Status**: `200 OK`
- **Response**:
  ```json
  {
    "experiment_id": "...",
    "experiment_name": "...",
    "variants": [
      {
        "variant_id": "...",
        "variant_name": "...",
        "latest_run": { ... },
        "latest_artifact": { ... },
        "evaluations": [ ... ],
        "average_score": 4.25
      }
    ],
    "metrics": [ ... ]
  }
  ```

### `POST /api/v1/research/artifacts/{artifact_id}/promote`
Promote a verified compatible research artifact to Production Draft status.
- **Permission**: Admin only (`research.promote` / `admin`)
- **Status**: `200 OK`
- **Request Body**:
  ```json
  {
    "target_production_type": "activity",
    "review_notes": "Validated by research team for Grade 4 cohort."
  }
  ```
- **Response**:
  ```json
  {
    "status": "promoted_to_draft",
    "production_draft_id": "draft-...",
    "artifact_id": "...",
    "promoted_by": "admin@eduvia.app"
  }
  ```
