"""add_learner_role_and_user_id

Revision ID: e7f8a9b0c1d2
Revises: d6e7f8a9b0c1
Create Date: 2026-09-29 14:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e7f8a9b0c1d2"
down_revision: str | Sequence[str] | None = "d6e7f8a9b0c1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """
    Upgrade schema:
    1. Add 'learner' to user_role_enum.
    2. Add nullable unique user_id to learners table.
    """
    # 1. Update user_role_enum safely
    op.execute("ALTER TYPE user_role_enum ADD VALUE IF NOT EXISTS 'learner'")

    # 2. Add user_id column to learners
    op.add_column(
        "learners",
        sa.Column(
            "user_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
            unique=True,
        ),
    )
    op.create_index("ix_learners_user_id", "learners", ["user_id"], unique=True)


def downgrade() -> None:
    """
    Downgrade schema:
    Drop user_id column and index from learners table.
    """
    op.drop_index("ix_learners_user_id", table_name="learners")
    op.drop_column("learners", "user_id")
