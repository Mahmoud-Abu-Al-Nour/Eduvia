# Eduvia — Content & Question Bank Architecture

## 1. Architectural Separation
Eduvia strictly separates:
- **Curriculum**: Defines **what** the student should learn (hierarchy of Subject -> Unit -> Lesson -> Learning Objective).
- **Content Bank**: Defines **authoritative educational content** (factual items, questions, correct answer keys, supported modalities, difficulty levels).
- **Knowledge Base (RAG)**: Defines **how to teach** (pedagogical strategies, scaffolding, accessibility accommodations, sensory calm).
- **Adaptive Engine**: Decides **what should change** (difficulty escalation/de-escalation, modality recommendations).
- **Gemini / GenAI**: Generates **variations in activity presentation** grounded in authoritative Content Bank items and RAG pedagogy.
- **Backend Service**: Authoritatively **evaluates** learner submissions and ingests telemetry.

```
+-------------------------------------------------------------+
|                     Learning Objective                      |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                 Authoritative Content Item                  |
|  - Prompt / Visual Item                                     |
|  - Correct Answer / Ground Truth                            |
|  - Modality Compatibility                                   |
|  - Difficulty Level                                         |
+---------------+------------------------------+--------------+
                |                              |
                v                              v
+-------------------------------+  +--------------------------+
| Deterministic Adaptation Rules|  |   RAG Pedagogical Base   |
+---------------+---------------+  +-----------+--------------+
                |                              |
                +--------------+---------------+
                               |
                               v
+-------------------------------------------------------------+
|              Gemini LLM Structured Generation               |
|            (or Deterministic Content Fallback)              |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                  Pydantic Schema Validation                 |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                     Frontend Player UI                      |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|             Authoritative Backend Evaluation                |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|               Telemetry -> Analytics Engine                 |
+-------------------------------------------------------------+
```

---

## 2. Content Item Schema (`content_items`)
Every authoritative item in the database contains:
- `id`: UUID (deterministic primary key)
- `objective_id`: UUID (foreign key linking directly to `learning_objectives.id`)
- `subject_code`: String identifier (e.g. `subj.foundational_math`, `subj.early_literacy`, `subj.everyday_learning`)
- `unit_code`: String identifier (e.g. `unit.math.counting`, `unit.lit.letters`, `unit.life.routines`)
- `content_key`: Human-readable identifier (e.g. `cnt.math.count_apples_5`)
- `difficulty_level`: Integer 1 to 5
- `supported_modalities`: JSONB array of strings (`["multiple_choice", "matching", "ordering", "visual_identification", "drag_drop"]`)
- `prompt`: JSONB localized dictionary (`{"en": "...", "ar": "..."}`)
- `content_payload`: JSONB dictionary containing modality-specific structural data
- `correct_answer`: JSONB authoritative answer truth
- `hints`: JSONB array of localized graded hints
- `metadata_info`: JSONB provenance metadata
- `is_active`: Boolean flag

---

## 3. Fallback Generation & Zero-Strand Guarantee
When LLM generation is unavailable or fails schema validation, the system falls back to `ContentBank.create_fallback_activity_for_objective(...)`.
This guarantees that learners always receive an authentic, educationally sound activity aligned with their target objective, difficulty level, and assigned modality.
