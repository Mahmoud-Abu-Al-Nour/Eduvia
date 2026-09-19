# Phase 2 — Curriculum & Learning Objectives

## Goal
Establish the standardized curriculum hierarchy and learning objectives engine independent from AI or adaptive delivery logic.

## Scope
- 5-tier relational data models: `Curriculum`, `Subject`, `Unit`, `Lesson`, `LearningObjective`.
- Objective prerequisites association table.
- Localization support using PostgreSQL JSONB.
- Alembic migration `65b1ea98eb6f` (`create_curriculum_tables`).
- Full CRUD service with eager-loading `selectinload` queries.
- REST API router for curricula browsing and admin creation.
- Frontend `CurriculumBrowser.tsx` component.
- Seeding scripts for demonstration curriculum.
