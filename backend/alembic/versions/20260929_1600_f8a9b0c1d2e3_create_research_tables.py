"""create_research_tables

Revision ID: f8a9b0c1d2e3
Revises: e7f8a9b0c1d2
Create Date: 2026-09-29 16:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f8a9b0c1d2e3"
down_revision: str | Sequence[str] | None = "e7f8a9b0c1d2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema for Research Mode and Sandbox experimentation."""
    # 1. Add researcher role to user_role_enum safely
    op.execute("ALTER TYPE user_role_enum ADD VALUE IF NOT EXISTS 'researcher'")

    # 2. research_projects
    op.create_table(
        "research_projects",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("research_question", sa.Text(), nullable=True),
        sa.Column("hypothesis", sa.Text(), nullable=True),
        sa.Column(
            "owner_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("metadata_info", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_research_projects_owner_id", "research_projects", ["owner_id"])
    op.create_index("ix_research_projects_status", "research_projects", ["status"])

    # 3. research_experiments
    op.create_table(
        "research_experiments",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "project_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("research_projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("research_question", sa.Text(), nullable=True),
        sa.Column("hypothesis", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("metadata_info", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_research_experiments_project_id", "research_experiments", ["project_id"])
    op.create_index("ix_research_experiments_status", "research_experiments", ["status"])

    # 4. research_variants
    op.create_table(
        "research_variants",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "experiment_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("research_experiments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("configuration", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column(
            "parent_variant_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("research_variants.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("metadata_info", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_research_variants_experiment_id", "research_variants", ["experiment_id"])

    # 5. research_runs
    op.create_table(
        "research_runs",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "variant_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("research_variants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("model", sa.String(length=100), nullable=False, server_default="gemini-2.5-flash"),
        sa.Column("model_configuration", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("system_prompt", sa.Text(), nullable=True),
        sa.Column("user_prompt", sa.Text(), nullable=False),
        sa.Column("input_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("raw_output", sa.Text(), nullable=True),
        sa.Column("normalized_output", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="draft"),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column(
            "parent_run_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("research_runs.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("metadata_info", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_research_runs_variant_id", "research_runs", ["variant_id"])
    op.create_index("ix_research_runs_status", "research_runs", ["status"])

    # 6. research_artifacts
    op.create_table(
        "research_artifacts",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "run_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("research_runs.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("artifact_type", sa.String(length=50), nullable=False),
        sa.Column("schema_version", sa.String(length=20), nullable=False, server_default="1.0"),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("is_production_compatible", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("compatibility_validation", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("promoted_to_production", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("production_entity_id", sa.UUID(as_uuid=True), nullable=True),
        sa.Column("metadata_info", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_research_artifacts_run_id", "research_artifacts", ["run_id"], unique=True)
    op.create_index("ix_research_artifacts_artifact_type", "research_artifacts", ["artifact_type"])
    op.create_index("ix_research_artifacts_is_production_compatible", "research_artifacts", ["is_production_compatible"])

    # 7. research_metrics
    op.create_table(
        "research_metrics",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "experiment_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("research_experiments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("metric_type", sa.String(length=50), nullable=False, server_default="rating"),
        sa.Column("configuration", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_research_metrics_experiment_id", "research_metrics", ["experiment_id"])

    # 8. research_evaluations
    op.create_table(
        "research_evaluations",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "artifact_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("research_artifacts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "metric_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("research_metrics.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("metric_name", sa.String(length=100), nullable=False),
        sa.Column("value", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("evaluator_type", sa.String(length=50), nullable=False, server_default="manual"),
        sa.Column(
            "evaluator_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_research_evaluations_artifact_id", "research_evaluations", ["artifact_id"])

    # 9. research_snapshots
    op.create_table(
        "research_snapshots",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "project_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("research_projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("source_reference", sa.String(length=255), nullable=False),
        sa.Column("snapshot_version", sa.String(length=50), nullable=False, server_default="1.0"),
        sa.Column("snapshot_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_research_snapshots_project_id", "research_snapshots", ["project_id"])


def downgrade() -> None:
    """Downgrade schema by dropping research tables in reverse order."""
    op.drop_index("ix_research_snapshots_project_id", table_name="research_snapshots")
    op.drop_table("research_snapshots")

    op.drop_index("ix_research_evaluations_artifact_id", table_name="research_evaluations")
    op.drop_table("research_evaluations")

    op.drop_index("ix_research_metrics_experiment_id", table_name="research_metrics")
    op.drop_table("research_metrics")

    op.drop_index("ix_research_artifacts_is_production_compatible", table_name="research_artifacts")
    op.drop_index("ix_research_artifacts_artifact_type", table_name="research_artifacts")
    op.drop_index("ix_research_artifacts_run_id", table_name="research_artifacts")
    op.drop_table("research_artifacts")

    op.drop_index("ix_research_runs_status", table_name="research_runs")
    op.drop_index("ix_research_runs_variant_id", table_name="research_runs")
    op.drop_table("research_runs")

    op.drop_index("ix_research_variants_experiment_id", table_name="research_variants")
    op.drop_table("research_variants")

    op.drop_index("ix_research_experiments_status", table_name="research_experiments")
    op.drop_index("ix_research_experiments_project_id", table_name="research_experiments")
    op.drop_table("research_experiments")

    op.drop_index("ix_research_projects_status", table_name="research_projects")
    op.drop_index("ix_research_projects_owner_id", table_name="research_projects")
    op.drop_table("research_projects")
