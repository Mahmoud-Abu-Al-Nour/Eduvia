# Eduvia Research Mode: Data Model & Schema Reference

## 1. Entity Relationship Diagram

```text
┌────────────────────────────────────────────────────────────────┐
│                         User (Researcher)                      │
│                id: UUID, role: 'researcher' | 'admin'          │
└───────────────────────────────┬────────────────────────────────┘
                                │ 1:N
                                ▼
┌────────────────────────────────────────────────────────────────┐
│                       ResearchProject                          │
│  id: UUID, owner_id: UUID, name: str, hypothesis: text         │
└───────────────────────────────┬────────────────────────────────┘
                                │ 1:N
                                ▼
┌────────────────────────────────────────────────────────────────┐
│                      ResearchExperiment                        │
│  id: UUID, project_id: UUID, name: str, research_question: text│
└───────────────┬───────────────────────────────┬────────────────┘
                │ 1:N                           │ 1:N
                ▼                               ▼
┌───────────────────────────────┐ ┌──────────────────────────────┐
│        ResearchVariant        │ │        ResearchMetric        │
│ id: UUID, experiment_id: UUID │ │ id: UUID, name: str          │
│ parent_variant_id: UUID (null)│ │ metric_type: 'scale_1_5'     │
│ configuration: JSONB          │ └──────────────┬───────────────┘
└───────────────┬───────────────┘                │
                │ 1:N                            │
                ▼                                │
┌───────────────────────────────┐                │
│          ResearchRun          │                │
│ id: UUID, variant_id: UUID    │                │
│ prompt: text, model: str      │                │
│ model_config: JSONB           │                │
│ raw_output: text              │                │
│ status: str                   │                │
└───────────────┬───────────────┘                │
                │ 1:1                            │
                ▼                                │
┌───────────────────────────────┐                │
│        ResearchArtifact       │                │
│ id: UUID, run_id: UUID        │                │
│ artifact_type: str            │                │
│ payload: JSONB / text         │                │
│ is_production_compatible: bool│                │
└───────────────┬───────────────┘                │
                │ 1:N                            │
                ▼                                ▼
┌────────────────────────────────────────────────────────────────┐
│                      ResearchEvaluation                        │
│ id: UUID, artifact_id: UUID, metric_id: UUID                   │
│ value: float, notes: text, evaluator_type: 'manual'            │
└────────────────────────────────────────────────────────────────┘
```

---

## 2. Table Specifications

### 2.1 `research_projects`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | Primary Key | Canonical UUIDv4 identifier |
| `owner_id` | UUID | Foreign Key (`users.id`), Index | Researcher owner ID |
| `name` | VARCHAR(255) | Not Null | Project title |
| `description` | TEXT | Nullable | Overview of project goals |
| `research_question`| TEXT | Nullable | Primary research inquiry |
| `hypothesis` | TEXT | Nullable | Falsifiable experimental hypothesis |
| `status` | VARCHAR(50) | Not Null, Default `'active'` | `'draft'`, `'active'`, `'completed'`, `'archived'` |
| `created_at` | TIMESTAMPTZ | Not Null, Server Default | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | Not Null, Server Default | Last modification timestamp |

### 2.2 `research_experiments`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | Primary Key | Canonical identifier |
| `project_id` | UUID | Foreign Key (`research_projects.id`), Cascade | Parent project |
| `name` | VARCHAR(255) | Not Null | Experiment name |
| `research_question`| TEXT | Nullable | Specific variable question |
| `hypothesis` | TEXT | Nullable | Target prediction |
| `description` | TEXT | Nullable | Methodology notes |
| `status` | VARCHAR(50) | Not Null, Default `'active'` | Lifecycle status |

### 2.3 `research_variants`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | Primary Key | Canonical identifier |
| `experiment_id` | UUID | Foreign Key (`research_experiments.id`), Cascade | Parent experiment |
| `parent_variant_id`| UUID | Foreign Key (`research_variants.id`), Nullable | Lineage tracking for cloned variants |
| `name` | VARCHAR(255) | Not Null | Variant title (e.g. "Worked Example A") |
| `description` | TEXT | Nullable | Experimental condition details |
| `configuration` | JSONB | Not Null, Default `{}` | Flexible variable dictionary |

### 2.4 `research_runs`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | Primary Key | Run identifier |
| `variant_id` | UUID | Foreign Key (`research_variants.id`), Cascade | Target variant |
| `parent_run_id` | UUID | Foreign Key (`research_runs.id`), Nullable | Re-run lineage pointer |
| `model` | VARCHAR(100) | Not Null | LLM identifier (e.g. `gemini-2.5-flash`) |
| `model_configuration`| JSONB| Not Null, Default `{}` | Temperature, tokens, seeds, etc. |
| `system_prompt` | TEXT | Nullable | Optional system instructions |
| `user_prompt` | TEXT | Not Null | Exact researcher prompt |
| `input_snapshot` | JSONB | Nullable | Snapshot of explicit manual context |
| `raw_output` | TEXT | Nullable | Exact unparsed model response string |
| `status` | VARCHAR(50) | Not Null | `'running'`, `'completed'`, `'failed'` |
| `error_message` | TEXT | Nullable | Safe diagnostic details if run failed |
| `execution_duration_ms`| INT | Nullable | Execution wall-clock latency |

### 2.5 `research_artifacts`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | Primary Key | Artifact identifier |
| `run_id` | UUID | Foreign Key (`research_runs.id`), Cascade | Originating run |
| `artifact_type` | VARCHAR(100)| Not Null | `assessment`, `activity`, `freeform`, etc. |
| `schema_version`| VARCHAR(50) | Not Null, Default `'research.v1'`| Schema contract version |
| `payload` | JSONB | Not Null | Structured JSON or wrapped text payload |
| `metadata` | JSONB | Not Null, Default `{}` | Parsing status, raw output link, metrics |
| `is_production_compatible`| BOOL| Not Null, Default `false` | Compatibility flag |

### 2.6 `research_metrics`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | Primary Key | Metric identifier |
| `experiment_id` | UUID | Foreign Key (`research_experiments.id`), Cascade | Parent experiment |
| `name` | VARCHAR(255) | Not Null | Metric name (e.g. "Cognitive Load") |
| `description` | TEXT | Nullable | Evaluation rubric guidance |
| `metric_type` | VARCHAR(50) | Not Null, Default `'scale_1_5'` | Evaluation scale type |

### 2.7 `research_evaluations`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | Primary Key | Evaluation identifier |
| `artifact_id` | UUID | Foreign Key (`research_artifacts.id`), Cascade | Scored artifact |
| `metric_id` | UUID | Foreign Key (`research_metrics.id`), Cascade | Rubric dimension |
| `evaluator_id` | UUID | Foreign Key (`users.id`) | Researcher user |
| `value` | FLOAT | Not Null | Assigned numerical score |
| `evaluator_type`| VARCHAR(50) | Not Null, Default `'manual'` | `'manual'` or `'model_assisted'` |
| `notes` | TEXT | Nullable | Qualitative critique and rationale |

### 2.8 `research_snapshots`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | Primary Key | Snapshot identifier |
| `project_id` | UUID | Foreign Key (`research_projects.id`), Cascade | Host research project |
| `source_type` | VARCHAR(100)| Not Null | `'curriculum_objective'`, `'activity'` |
| `source_reference`| VARCHAR(255)| Not Null | Original database reference ID |
| `snapshot_version`| INT | Not Null, Default `1` | Snapshot sequence |
| `snapshot_data` | JSONB | Not Null | Read-only static payload |
