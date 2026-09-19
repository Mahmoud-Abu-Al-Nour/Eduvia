"""create_learner_tables

Revision ID: a3b8c9d0e1f2
Revises: 65b1ea98eb6f
Create Date: 2026-09-19 04:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a3b8c9d0e1f2"
down_revision: str | Sequence[str] | None = "65b1ea98eb6f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema to include Phase 3 Learner and LearnerProfile tables."""
    # learners table
    op.create_table(
        "learners",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("age_group", sa.String(length=50), nullable=False, server_default="primary"),
        sa.Column("learning_level", sa.String(length=50), nullable=False, server_default="beginner"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("teacher_id", sa.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_learners_id", "learners", ["id"], unique=False)
    op.create_index("ix_learners_name", "learners", ["name"], unique=False)
    op.create_index("ix_learners_teacher_id", "learners", ["teacher_id"], unique=False)

    # learner_profiles table
    op.create_table(
        "learner_profiles",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("learner_id", sa.UUID(as_uuid=True), sa.ForeignKey("learners.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("communication_preferences", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("current_skill_level", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("support_requirements", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("teacher_constraints", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("teacher_notes", sa.Text(), nullable=True),
        sa.Column("teacher_overrides", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("modality_effectiveness", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("strategy_effectiveness", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("activity_type_effectiveness", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("difficulty_tolerance", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("assistance_requirements", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("response_behavior", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("observations", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_learner_profiles_id", "learner_profiles", ["id"], unique=False)
    op.create_index("ix_learner_profiles_learner_id", "learner_profiles", ["learner_id"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_learner_profiles_learner_id", table_name="learner_profiles")
    op.drop_index("ix_learner_profiles_id", table_name="learner_profiles")
    op.drop_table("learner_profiles")

    op.drop_index("ix_learners_teacher_id", table_name="learners")
    op.drop_index("ix_learners_name", table_name="learners")
    op.drop_index("ix_learners_id", table_name="learners")
    op.drop_table("learners")
