# Database Architecture

Eduvia utilizes PostgreSQL 16 managed by Alembic database migrations.

---

## Migration History Chain

```text
[Base]
  │
  ▼
[268264a74567] create_users_table (Phase 1)
  │ - Creates user_role_enum ('admin', 'teacher')
  │ - Creates users table (id, email, full_name, hashed_password, role, is_active, timestamps)
  │ - Unique index on ix_users_email
  ▼
[65b1ea98eb6f] create_curriculum_tables (Phase 2)
  │ - Creates curricula (JSONB titles/desc, version, created_by_id)
  │ - Creates subjects (curriculum_id FK CASCADE)
  │ - Creates units (subject_id FK CASCADE)
  │ - Creates lessons (unit_id FK CASCADE)
  │ - Creates learning_objectives (lesson_id FK CASCADE, difficulty, assessment_criteria JSONB)
  │ - Creates objective_prerequisites (association table for self-referential graph)
```

## Optimization & Integrity Rules
- **Foreign Keys**: Cascade delete on children (`ondelete="CASCADE"`) to avoid orphan educational records.
- **JSONB Localization**: Localized strings stored as `JSONB` allow arbitrary language additions without table alterations.
- **Eager Loading**: `CurriculumService` uses `selectinload()` chains to fetch full hierarchy trees in single batch queries, preventing N+1 performance bottlenecks.
