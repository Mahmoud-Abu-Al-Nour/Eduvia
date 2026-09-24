"""
Eduvia — Content / Question Bank Models

Provides authoritative educational facts, items, options, and answers
linked directly to Learning Objectives, separating content from curriculum
and pedagogical knowledge.
"""
from __future__ import annotations

import uuid
from typing import Any, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.curriculum.models import LearningObjective
from app.database.base import EduviaBase


class ContentItem(EduviaBase):
    """
    Authoritative educational content item linked to a specific learning objective.

    Serves as the ground-truth content bank for activity generation, deterministic
    fallbacks, and authoritative backend evaluation.
    """
    __tablename__ = "content_items"

    objective_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("learning_objectives.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    subject_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    unit_code: Mapped[str] = mapped_column(String(50), nullable=False)
    content_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)

    difficulty_level: Mapped[int] = mapped_column(Integer, default=1, index=True)
    supported_modalities: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="en")

    # Bilingual localized prompt: {"en": "...", "ar": "..."}
    prompt: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    # Modality-specific payload (options, pairs, sequence items, visual elements, zones)
    content_payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    # Authoritative ground-truth answer key evaluated server-side
    correct_answer: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    # Bilingual explanation: {"en": "...", "ar": "..."}
    explanation: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    # Scaffolding hints ordered from subtle to explicit
    hints: Mapped[list[dict[str, str]]] = mapped_column(JSONB, default=list)

    # Content metadata, tags, and provenance
    metadata_info: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    objective: Mapped["LearningObjective"] = relationship(lazy="selectin")
