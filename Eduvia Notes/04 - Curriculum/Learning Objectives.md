# Learning Objectives

Learning Objectives (`learning_objectives` table) are the atomic units of mastery in Eduvia.

---

## Core Attributes

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Primary key. |
| `lesson_id` | UUID | Foreign key to parent lesson. |
| `title` | JSONB | Localized title (e.g., `{"en": "...", "ar": "..."}`). |
| `description` | JSONB | Localized pedagogical explanation. |
| `difficulty_level`| Integer | Validated range 1 to 5. |
| `assessment_criteria`| JSONB | Minimum accuracy, max assistance, completion flags. |
| `order_index` | Integer | Position within lesson. |
| `is_active` | Boolean | Publishing toggle. |
| `prerequisites` | Relation | Directed relationships to prerequisite objectives. |
