"""add_question_id_and_instructional_contents

Revision ID: d6e7f8a9b0c1
Revises: c5d6e7f8a9b0
Create Date: 2026-09-28 22:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "d6e7f8a9b0c1"
down_revision: str | Sequence[str] | None = "c5d6e7f8a9b0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """
    Upgrade schema:
    1. Add nullable question_id to performance_events for multi-question telemetry.
    2. Create instructional_contents table for dedicated modeling and explanations.
    """
    # 1. Performance events question_id
    op.add_column(
        "performance_events",
        sa.Column("question_id", sa.String(length=100), nullable=True),
    )
    op.create_index("ix_performance_events_question_id", "performance_events", ["question_id"])

    # 2. Instructional contents table
    op.create_table(
        "instructional_contents",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "objective_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("learning_objectives.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("explanation_method", sa.String(length=50), nullable=False, server_default="visual_explanation"),
        sa.Column("difficulty_level", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("language", sa.String(length=10), nullable=False, server_default="en"),
        sa.Column("blocks", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="review_required"),
        sa.Column("teacher_notes", sa.Text(), nullable=True),
        sa.Column(
            "created_by",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("metadata_info", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_index("ix_instructional_contents_objective_id", "instructional_contents", ["objective_id"])
    op.create_index("ix_instructional_contents_explanation_method", "instructional_contents", ["explanation_method"])
    op.create_index("ix_instructional_contents_status", "instructional_contents", ["status"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_instructional_contents_status", table_name="instructional_contents")
    op.drop_index("ix_instructional_contents_explanation_method", table_name="instructional_contents")
    op.drop_index("ix_instructional_contents_objective_id", table_name="instructional_contents")
    op.drop_table("instructional_contents")

    op.drop_index("ix_performance_events_question_id", table_name="performance_events")
    op.drop_column("performance_events", "question_id")
