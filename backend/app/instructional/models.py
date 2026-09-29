"""
Eduvia — Instructional Content Models

Stores dedicated instructional content, modeling explanations, and worked examples
linked directly to Learning Objectives, strictly separated from assessment activities.
"""
from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.curriculum.models import LearningObjective
from app.database.base import EduviaBase


class InstructionalContent(EduviaBase):
    """
    Authoritative instructional content entity designed to explain or demonstrate
    a learning objective prior to practice.
    """
    __tablename__ = "instructional_contents"

    objective_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("learning_objectives.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    explanation_method: Mapped[str] = mapped_column(String(50), nullable=False, default="visual_explanation", index=True)
    difficulty_level: Mapped[int] = mapped_column(Integer, default=1)
    language: Mapped[str] = mapped_column(String(10), default="en")

    # Structured list of content blocks (heading, text, visual_cue, step, worked_example, callout, audio_script)
    blocks: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, nullable=False, default=list)

    # Concise summary / takeaway
    summary: Mapped[str] = mapped_column(Text, nullable=False)

    # Teacher review status: draft, review_required, approved, published, archived
    status: Mapped[str] = mapped_column(String(30), default="review_required", index=True)
    teacher_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    metadata_info: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)

    # Relationships
    objective: Mapped["LearningObjective"] = relationship(lazy="selectin")
