"""create_curriculum_tables

Revision ID: 65b1ea98eb6f
Revises: 268264a74567
Create Date: 2026-09-18 23:47:07.583592

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "65b1ea98eb6f"
down_revision: str | Sequence[str] | None = "268264a74567"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # curricula table
    op.create_table(
        "curricula",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("description", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_by_id", sa.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
    )

    # subjects table
    op.create_table(
        "subjects",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("curriculum_id", sa.UUID(as_uuid=True), sa.ForeignKey("curricula.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("description", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
    )

    # units table
    op.create_table(
        "units",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("subject_id", sa.UUID(as_uuid=True), sa.ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("description", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
    )

    # lessons table
    op.create_table(
        "lessons",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("unit_id", sa.UUID(as_uuid=True), sa.ForeignKey("units.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("description", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
    )

    # learning_objectives table
    op.create_table(
        "learning_objectives",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("lesson_id", sa.UUID(as_uuid=True), sa.ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("description", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("difficulty_level", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("assessment_criteria", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )

    # objective_prerequisites association table
    op.create_table(
        "objective_prerequisites",
        sa.Column("objective_id", sa.UUID(as_uuid=True), sa.ForeignKey("learning_objectives.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("prerequisite_id", sa.UUID(as_uuid=True), sa.ForeignKey("learning_objectives.id", ondelete="CASCADE"), primary_key=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("objective_prerequisites")
    op.drop_table("learning_objectives")
    op.drop_table("lessons")
    op.drop_table("units")
    op.drop_table("subjects")
    op.drop_table("curricula")
