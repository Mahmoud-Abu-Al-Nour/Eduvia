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

## 3. Multi-Question Activity Assembly & Provenance

To support homogeneous multi-question activities (3–10 questions, default 5), the Content Bank maintains canonical content families for every learning objective across Mathematics, Literacy, and Everyday Learning.

```text
Learning Objective
       ↓
Canonical Content Family
       ├── Source 1 (e.g. Count 3 apples)
       ├── Source 2 (e.g. Count 5 stars)
       ├── Source 3 (e.g. Count 2 birds)
       ├── Source 4 (e.g. Count 4 fish)
       └── Source 5 (e.g. Count 6 flowers)
             ↓
      Modality Renderer
       ├── MCQ
       ├── Matching
       ├── Ordering
       ├── Visual Identification
       └── Drag & Drop
```

Key guarantees:
1. **Distinct Items**: Activities assemble 5 distinct source items without repeating the exact same item within an activity.
2. **Provenance Traceability**: Every question generated or assembled carries `content_source_key` and `objective_id` linking directly to the authoritative content item.
3. **Cross-Modality Support**: Items support multiple modalities through deterministic modality transformers in `ContentBank.create_question_from_content()`.

---

## 4. Fallback Generation & Zero-Strand Guarantee
When LLM generation is unavailable or fails schema validation, the system falls back to `ContentBank.assemble_multi_question_activity(...)` or `ContentBank.create_fallback_activity_for_objective(...)`.
This guarantees that learners always receive an authentic, educationally sound, multi-question activity aligned with their target objective, difficulty level, and assigned modality.
