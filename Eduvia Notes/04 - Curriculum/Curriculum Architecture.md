# Curriculum Architecture

Eduvia structures educational content into a strict 5-tier relational hierarchy.

---

## The 5-Tier Hierarchy

```text
Level 1: Curriculum           (e.g., "National Grade 1 Mathematics")
   │
   └── Level 2: Subject       (e.g., "Foundational Mathematics")
          │
          └── Level 3: Unit   (e.g., "Number Sense & Counting")
                 │
                 └── Level 4: Lesson  (e.g., "Number Recognition 1–10")
                        │
                        └── Level 5: Learning Objective (e.g., "Recognize numbers 1–5")
```

---

## Database Realization
- Stored across tables: `curricula`, `subjects`, `units`, `lessons`, `learning_objectives`.
- Connected via cascading foreign keys (`ondelete="CASCADE"`).
- Ordered explicitly via `order_index` integers on every tier.
- Eagerly loadable via SQLAlchemy `selectinload` for high-speed API delivery.
