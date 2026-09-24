"""create_content_items_table

Revision ID: c5d6e7f8a9b0
Revises: b4c5d6e7f8a9
Create Date: 2026-09-24 18:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c5d6e7f8a9b0"
down_revision: str | Sequence[str] | None = "b4c5d6e7f8a9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema to include content_items table for authoritative Content / Question Bank."""
    op.create_table(
        "content_items",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "objective_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("learning_objectives.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("subject_code", sa.String(length=50), nullable=False),
        sa.Column("unit_code", sa.String(length=50), nullable=False),
        sa.Column("content_key", sa.String(length=100), nullable=False, unique=True),
        sa.Column("difficulty_level", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("supported_modalities", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("language", sa.String(length=10), nullable=False, server_default="en"),
        sa.Column("prompt", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("content_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("correct_answer", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("explanation", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("hints", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("metadata_info", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_index("ix_content_items_objective_id", "content_items", ["objective_id"])
    op.create_index("ix_content_items_subject_code", "content_items", ["subject_code"])
    op.create_index("ix_content_items_content_key", "content_items", ["content_key"])
    op.create_index("ix_content_items_difficulty_level", "content_items", ["difficulty_level"])


def downgrade() -> None:
    """Downgrade schema by dropping content_items table."""
    op.drop_index("ix_content_items_difficulty_level", table_name="content_items")
    op.drop_index("ix_content_items_content_key", table_name="content_items")
    op.drop_index("ix_content_items_subject_code", table_name="content_items")
    op.drop_index("ix_content_items_objective_id", table_name="content_items")
    op.drop_table("content_items")
