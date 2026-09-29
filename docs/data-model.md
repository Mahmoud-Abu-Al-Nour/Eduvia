# Eduvia — Data Model

## Domain Overview

```
User (Teacher / Admin)
    │
    └── Learner ─────────────────────────────── LearnerProfile
           │                                          │
    LearningSession                              ModalityScore × 5
           │                                    StrategyScore × N
    ActivityAttempt ─── Activity ─── LearningObjective ─── InstructionalContent
           │                               │
    PerformanceEvent              Lesson → Unit → Subject → Curriculum
     (question_id)                         │
                                     KnowledgeDocument → KnowledgeChunk
                                           │
                                        (Qdrant)
```

---

## Core Entities

### User

```
User
├── id: UUID (PK)
├── email: str (unique)
├── full_name: str
├── hashed_password: str
├── role: enum[admin, teacher]
├── is_active: bool
├── created_at: datetime
└── updated_at: datetime
```

### Learner

```
Learner
├── id: UUID (PK)
├── display_name: str              # No real names required
├── teacher_id: UUID (FK → User)
├── age_group: enum[early_childhood, childhood, adolescent, adult]
├── learning_level: enum[foundation, developing, emerging, established]
├── communication_preference: enum[verbal, visual, augmentative, mixed]
├── support_requirements: str[]    # Teacher-provided tags
├── teacher_notes: str
├── is_active: bool
├── created_at: datetime
└── updated_at: datetime
```

**Note:** No medical diagnoses stored. Only educational support descriptors.

### LearnerProfile

```
LearnerProfile
├── id: UUID (PK)
├── learner_id: UUID (FK → Learner, unique)
├── modality_scores: JSONB         # ModalityScore per modality
├── strategy_scores: JSONB         # StrategyScore per strategy
├── total_activities: int
├── exploration_phase: bool
├── exploration_activities_remaining: int
├── last_updated: datetime
├── created_at: datetime
└── updated_at: datetime
```

ModalityScore (JSONB structure):
```json
{
  "visual": { "score": 0.82, "confidence": 0.91, "evidence_count": 27 },
  "reading": { "score": 0.34, "confidence": 0.88, "evidence_count": 21 },
  "audio": { "score": 0.61, "confidence": 0.75, "evidence_count": 14 },
  "interactive": { "score": 0.78, "confidence": 0.85, "evidence_count": 19 },
  "writing": { "score": 0.22, "confidence": 0.60, "evidence_count": 8 }
}
```

---

## Curriculum Entities

### Curriculum

```
Curriculum
├── id: UUID (PK)
├── title: str
├── description: str
├── version: str
├── is_active: bool
├── created_by: UUID (FK → User)
├── created_at: datetime
└── updated_at: datetime
```

### Subject

```
Subject
├── id: UUID (PK)
├── curriculum_id: UUID (FK → Curriculum)
├── title: str
├── description: str
├── order_index: int
├── created_at: datetime
└── updated_at: datetime
```

### Unit

```
Unit
├── id: UUID (PK)
├── subject_id: UUID (FK → Subject)
├── title: str
├── description: str
├── order_index: int
├── created_at: datetime
└── updated_at: datetime
```

### Lesson

```
Lesson
├── id: UUID (PK)
├── unit_id: UUID (FK → Unit)
├── title: str
├── description: str
├── order_index: int
├── created_at: datetime
└── updated_at: datetime
```

### LearningObjective

```
LearningObjective
├── id: UUID (PK)
├── lesson_id: UUID (FK → Lesson)
├── title: str                     # e.g., "Recognize numbers 1–10"
├── description: str
├── difficulty_level: int (1–5)
├── tags: str[]
├── is_active: bool
├── order_index: int
├── created_at: datetime
└── updated_at: datetime
```

**Key Principle:** Learning objectives are stable. Only delivery method changes.

---

## Instructional Entities

### InstructionalContent

```
InstructionalContent
├── id: UUID (PK)
├── objective_id: UUID (FK → LearningObjective)
├── title: str
├── explanation_method: enum[visual_explanation, step_by_step, worked_example, text_explanation]
├── difficulty_level: int (1–5)
├── language: str ("en", "ar")
├── blocks: JSONB                  # Array of InstructionalBlock objects
├── summary: str | null            # Optional summary/takeaway
├── status: enum[draft, review_required, approved, published, archived]
├── teacher_notes: str | null
├── created_by: UUID | null        # Teacher ID if manual/approved
├── metadata_info: JSONB           # Generation context / RAG provenance
├── created_at: datetime
└── updated_at: datetime
```

InstructionalBlock (JSONB structure):
```json
{
  "id": "blk-step-1",
  "block_type": "step",
  "title": "Count the first group",
  "body": "Look at the red apples on the left. Tap each one as you count: 1, 2, 3.",
  "visual_cue": "🍎 🍎 🍎",
  "order_index": 1,
  "metadata": {}
}
```

*Note: InstructionalContent is strictly non-evaluative. It contains no score, no pass/fail, and no answer truth keys.*

---

## Activity Entities

### Activity

```
Activity
├── id: UUID (PK)
├── objective_id: UUID (FK → LearningObjective)
├── activity_type: enum[matching, multiple_choice, ordering, visual_identification, drag_drop]
├── modality: enum[visual, reading, writing, audio, interactive]
├── strategy: enum[step_by_step, repetition, scaffolding, prompting, simplification, demonstration, positive_reinforcement, gradual_difficulty]
├── difficulty: int (1–5)
├── questions: ActivityQuestion[]   # 3–10 questions (default 5)
├── content: JSONB | null          # Legacy 1-question content (for backward compatibility)
├── audio_enabled: bool
├── generated_by: enum[ai, teacher]
├── generation_context: JSONB      # RAG context & ContentBank source keys
├── is_active: bool
├── created_at: datetime
└── updated_at: datetime
```

ActivityQuestion (Schema):
```json
{
  "id": "q-1",
  "question_number": 1,
  "content": { ... },              // Complete modality-specific interaction payload
  "question_type": "multiple_choice",
  "content_source_key": "cnt.math.count_apples_5",
  "hints": ["Count them one by one"],
  "explanation": "There are 5 apples.",
  "weight": 1.0
}
```

### ActivityAttempt

Represents **one learner attempt at one complete activity** (not per question).

```
ActivityAttempt
├── id: UUID (PK)
├── activity_id: UUID (FK → Activity)
├── learner_id: UUID (FK → Learner)
├── session_id: UUID
├── started_at: datetime
├── completed_at: datetime | null
├── response_data: JSONB          # Full submission with per-question answers
├── score: float | null           # Aggregate overall score across all questions
├── completed: bool               # Complete activity status
├── created_at: datetime
└── updated_at: datetime
```

---

## Analytics Entities

### PerformanceEvent

Represents an atomic interaction event. Question-level events belong to the parent `ActivityAttempt`.

```
PerformanceEvent
├── id: UUID (PK)
├── learner_id: UUID (FK → Learner)
├── activity_id: UUID (FK → Activity)
├── attempt_id: UUID (FK → ActivityAttempt)
├── question_id: UUID | null (indexed) # Question identity for item-level analysis
├── objective_id: UUID (FK → LearningObjective)
├── activity_type: enum
├── modality: enum
├── strategy: enum
├── correct: bool
├── attempts: int
├── response_time_ms: int
├── hints_used: int
├── assistance_level: int (0–3)
├── completed: bool
├── difficulty: int (1–5)
├── timestamp: datetime
└── created_at: datetime
```

*Note: Completed activity counts are derived strictly from `ActivityAttempt` or distinct activity events so that multiple question-level `PerformanceEvent`s never inflate completed activity counts.*

---

## Knowledge Entities

### KnowledgeDocument (PostgreSQL metadata)

```
KnowledgeDocument
├── id: UUID (PK)
├── title: str
├── source: str                   # File name or URL
├── category: enum[strategy, curriculum, accessibility, activity_design, ...]
├── chunk_count: int
├── embedded_at: datetime | null
├── created_at: datetime
└── updated_at: datetime
```

### KnowledgeChunk (PostgreSQL metadata + Qdrant vector)

```
KnowledgeChunk
├── id: UUID (PK)
├── document_id: UUID (FK → KnowledgeDocument)
├── content: str                  # Raw text chunk
├── chunk_index: int
├── qdrant_id: str                # ID in Qdrant collection
├── metadata: JSONB               # Tags, categories, etc.
├── created_at: datetime
└── updated_at: datetime
```

---

## Recommendation Entities

### Recommendation

```
Recommendation
├── id: UUID (PK)
├── learner_id: UUID (FK → Learner)
├── objective_id: UUID (FK → LearningObjective)
├── recommended_modality: enum
├── recommended_strategy: enum
├── recommended_activity_type: enum
├── confidence: float (0–1)
├── explanation: str
├── evidence_summary: JSONB
├── teacher_reviewed: bool
├── teacher_override: JSONB | null
├── created_at: datetime
└── updated_at: datetime
```

---

## Design Principles

1. **No medical data** — Only educational support descriptors
2. **UUID primary keys** — Globally unique, no sequential ID leaks
3. **JSONB for flexible schemas** — Activity content, modality scores, evidence
4. **Audit timestamps** — created_at + updated_at on all entities
5. **Soft deletes** — is_active flag where appropriate
6. **Foreign key integrity** — Enforced at database level
7. **Normalized curriculum** — Curriculum/Subject/Unit/Lesson/Objective hierarchy
8. **Learner profile updates** — Incremental updates, not full overwrites
