"""
Eduvia — Research Mode & Sandbox Models

Provides relational entities for isolated educational experimentation:
ResearchProject -> ResearchExperiment -> ResearchVariant -> ResearchRun -> ResearchArtifact.
Supports custom metrics, evaluations, optional snapshots, and promotion workflows.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import EduviaBase

if TYPE_CHECKING:
    from app.users.models import User


class ResearchProject(EduviaBase):
    """
    Top-level organizational unit for an educational research initiative.
    Strictly isolated per researcher (or platform-wide for administrators).
    """
    __tablename__ = "research_projects"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    research_question: Mapped[str | None] = mapped_column(Text, nullable=True)
    hypothesis: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False, index=True)
    metadata_info: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)

    # Relationships
    owner: Mapped["User"] = relationship(lazy="selectin")
    experiments: Mapped[list["ResearchExperiment"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    snapshots: Mapped[list["ResearchSnapshot"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ResearchExperiment(EduviaBase):
    """
    Specific experimental test setup comparing multiple pedagogical or generative variants.
    """
    __tablename__ = "research_experiments"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    research_question: Mapped[str | None] = mapped_column(Text, nullable=True)
    hypothesis: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False, index=True)
    metadata_info: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)

    # Relationships
    project: Mapped["ResearchProject"] = relationship(back_populates="experiments", lazy="selectin")
    variants: Mapped[list["ResearchVariant"]] = relationship(
        back_populates="experiment",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    metrics: Mapped[list["ResearchMetric"]] = relationship(
        back_populates="experiment",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ResearchVariant(EduviaBase):
    """
    Independent treatment condition / experimental branch (e.g. prompt template,
    temperature, explanation method, question format).
    """
    __tablename__ = "research_variants"

    experiment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_experiments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    configuration: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    parent_variant_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_variants.id", ondelete="SET NULL"),
        nullable=True,
    )
    metadata_info: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)

    # Relationships
    experiment: Mapped["ResearchExperiment"] = relationship(back_populates="variants", lazy="selectin")
    runs: Mapped[list["ResearchRun"]] = relationship(
        back_populates="variant",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ResearchRun(EduviaBase):
    """
    Concrete execution instance of a variant producing a generated research outcome.
    Preserves exact prompts, configuration, raw output, and execution telemetry.
    """
    __tablename__ = "research_runs"

    variant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_variants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    model: Mapped[str] = mapped_column(String(100), default="gemini-3.8-flash", nullable=False)
    model_configuration: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    system_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    input_snapshot: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    raw_output: Mapped[str | None] = mapped_column(Text, nullable=True)
    normalized_output: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_run_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_runs.id", ondelete="SET NULL"),
        nullable=True,
    )
    metadata_info: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    variant: Mapped["ResearchVariant"] = relationship(back_populates="runs", lazy="selectin")
    artifact: Mapped["ResearchArtifact | None"] = relationship(
        back_populates="run",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ResearchArtifact(EduviaBase):
    """
    Extracted educational or instructional asset resulting from a successful research run.
    Stores raw & normalized payload without forcing production schema adherence.
    """
    __tablename__ = "research_artifacts"

    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_runs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    artifact_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    schema_version: Mapped[str] = mapped_column(String(20), default="1.0")
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_production_compatible: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    compatibility_validation: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    promoted_to_production: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    production_entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    metadata_info: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)

    # Relationships
    run: Mapped["ResearchRun"] = relationship(back_populates="artifact", lazy="selectin")
    evaluations: Mapped[list["ResearchEvaluation"]] = relationship(
        back_populates="artifact",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ResearchMetric(EduviaBase):
    """
    Configurable evaluation criterion defined for an experiment (e.g. clarity, accuracy, formatting).
    """
    __tablename__ = "research_metrics"

    experiment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_experiments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    metric_type: Mapped[str] = mapped_column(String(50), default="rating", nullable=False)
    configuration: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)

    # Relationships
    experiment: Mapped["ResearchExperiment"] = relationship(back_populates="metrics", lazy="selectin")


class ResearchEvaluation(EduviaBase):
    """
    Quantitative or qualitative assessment scored against a research artifact.
    """
    __tablename__ = "research_evaluations"

    artifact_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_artifacts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    metric_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_metrics.id", ondelete="SET NULL"),
        nullable=True,
    )
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    evaluator_type: Mapped[str] = mapped_column(String(50), default="manual", nullable=False)
    evaluator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    artifact: Mapped["ResearchArtifact"] = relationship(back_populates="evaluations", lazy="selectin")


class ResearchSnapshot(EduviaBase):
    """
    Immutable read-only snapshot of production curriculum, content, or activity for research reference.
    Guarantees research does not hold live mutable connections to production databases.
    """
    __tablename__ = "research_snapshots"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("research_projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    source_reference: Mapped[str] = mapped_column(String(255), nullable=False)
    snapshot_version: Mapped[str] = mapped_column(String(50), default="1.0")
    snapshot_data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    # Relationships
    project: Mapped["ResearchProject"] = relationship(back_populates="snapshots", lazy="selectin")
