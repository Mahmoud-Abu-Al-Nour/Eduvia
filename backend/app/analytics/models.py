"""
Eduvia — Analytics & Telemetry SQLAlchemy ORM Models (Phase 6)

Persists learner performance events, attempt counters, latency measurements,
and assistance levels resulting from authoritative Phase 5 evaluations.

Adheres to:
- docs/data-model.md Analytics Entities specifications
- Strict audit integrity (inherited from EduviaBase)
- Referential integrity with learners and curriculum objectives
- Zero Phase 7 (rolling mastery) or Phase 8 (adaptive intelligence) logic
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import EduviaBase

if TYPE_CHECKING:
    from app.curriculum.models import LearningObjective
    from app.learners.models import Learner


class ActivityAttempt(EduviaBase):
    """
    Records discrete attempts on learning activities during learner sessions.
    Captures raw interaction payloads, timing, and completion status.
    """
    __tablename__ = "activity_attempts"

    activity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
    learner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("learners.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    session_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    response_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Relationships
    learner: Mapped[Learner] = relationship(
        "Learner",
        backref="activity_attempts",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<ActivityAttempt id={self.id} learner_id={self.learner_id} score={self.score}>"


class PerformanceEvent(EduviaBase):
    """
    Authoritative telemetry event recorded upon activity evaluation or interaction milestones.
    Captures modality, strategy, correctness, latency, hints, and assistance levels.
    """
    __tablename__ = "performance_events"

    learner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("learners.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    activity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
    attempt_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("activity_attempts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    objective_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("learning_objectives.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    activity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    modality: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="visual",
    )
    strategy: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="step_by_step",
    )
    correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    attempts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    response_time_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    hints_used: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    assistance_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    difficulty: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    event_metadata: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        default=dict,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )

    # Relationships
    learner: Mapped[Learner] = relationship(
        "Learner",
        backref="performance_events",
        lazy="selectin",
    )
    objective: Mapped[LearningObjective] = relationship(
        "LearningObjective",
        lazy="selectin",
    )
    attempt: Mapped[ActivityAttempt | None] = relationship(
        "ActivityAttempt",
        backref="performance_events",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"<PerformanceEvent id={self.id} learner_id={self.learner_id} "
            f"type='{self.activity_type}' correct={self.correct} score={self.score}>"
        )
