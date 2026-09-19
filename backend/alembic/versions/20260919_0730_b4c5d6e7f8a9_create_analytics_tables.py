"""create_analytics_tables

Revision ID: b4c5d6e7f8a9
Revises: a3b8c9d0e1f2
Create Date: 2026-09-19 07:30:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b4c5d6e7f8a9"
down_revision: str | Sequence[str] | None = "a3b8c9d0e1f2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema to include Phase 6 ActivityAttempt and PerformanceEvent tables."""
    # 1. activity_attempts table
    op.create_table(
        "activity_attempts",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("activity_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "learner_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("learners.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("session_id", sa.UUID(as_uuid=True), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("response_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("completed", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_activity_attempts_id", "activity_attempts", ["id"], unique=False)
    op.create_index("ix_activity_attempts_activity_id", "activity_attempts", ["activity_id"], unique=False)
    op.create_index("ix_activity_attempts_learner_id", "activity_attempts", ["learner_id"], unique=False)
    op.create_index("ix_activity_attempts_session_id", "activity_attempts", ["session_id"], unique=False)

    # 2. performance_events table
    op.create_table(
        "performance_events",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "learner_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("learners.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("activity_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "attempt_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("activity_attempts.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "objective_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("learning_objectives.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("activity_type", sa.String(length=50), nullable=False),
        sa.Column("modality", sa.String(length=50), nullable=False, server_default="visual"),
        sa.Column("strategy", sa.String(length=50), nullable=False, server_default="step_by_step"),
        sa.Column("correct", sa.Boolean(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("response_time_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("hints_used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("assistance_level", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("difficulty", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_performance_events_id", "performance_events", ["id"], unique=False)
    op.create_index("ix_performance_events_learner_id", "performance_events", ["learner_id"], unique=False)
    op.create_index("ix_performance_events_activity_id", "performance_events", ["activity_id"], unique=False)
    op.create_index("ix_performance_events_attempt_id", "performance_events", ["attempt_id"], unique=False)
    op.create_index("ix_performance_events_objective_id", "performance_events", ["objective_id"], unique=False)
    op.create_index("ix_performance_events_activity_type", "performance_events", ["activity_type"], unique=False)
    op.create_index("ix_performance_events_timestamp", "performance_events", ["timestamp"], unique=False)


def downgrade() -> None:
    """Downgrade schema removing Phase 6 tables."""
    op.drop_table("performance_events")
    op.drop_table("activity_attempts")
