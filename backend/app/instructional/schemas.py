"""
Eduvia — Instructional Content Schemas

Pydantic validation schemas for dedicated instructional content, modeling explanations,
and worked examples.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ExplanationMethod(StrEnum):
    """Supported explanation methods for instructional content."""
    VISUAL_EXPLANATION = "visual_explanation"
    STEP_BY_STEP = "step_by_step"
    WORKED_EXAMPLE = "worked_example"
    TEXT_EXPLANATION = "text_explanation"


class ContentBlockType(StrEnum):
    """Structured presentation block types for instructional display."""
    HEADING = "heading"
    TEXT = "text"
    VISUAL_CUE = "visual_cue"
    STEP = "step"
    WORKED_EXAMPLE = "worked_example"
    CALLOUT = "callout"
    AUDIO_SCRIPT = "audio_script"


class InstructionalStatus(StrEnum):
    """Lifecycle status for teacher review and learner publication."""
    DRAFT = "draft"
    REVIEW_REQUIRED = "review_required"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class InstructionalBlock(BaseModel):
    """Discrete, ordered presentation block in an instructional explanation."""
    model_config = ConfigDict(frozen=True)

    id: str = Field(default_factory=lambda: f"blk_{uuid.uuid4().hex[:8]}")
    block_type: ContentBlockType
    title: str | None = None
    body: str = Field(default="", description="Accessible explanatory text or guidance")
    visual_cue: str | None = Field(default=None, description="Visual symbol, emoji, icon, or pattern")
    order_index: int = Field(default=0, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class InstructionalContentRead(BaseModel):
    """Read DTO for complete instructional content entity."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    objective_id: uuid.UUID | str
    title: str
    explanation_method: ExplanationMethod
    difficulty_level: int
    language: str
    blocks: list[InstructionalBlock]
    summary: str
    status: InstructionalStatus
    teacher_notes: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class InstructionalGenerateRequest(BaseModel):
    """Request payload to generate instructional content."""
    objective_id: uuid.UUID | str = Field(..., description="Target learning objective identifier")
    explanation_method: ExplanationMethod = Field(
        default=ExplanationMethod.VISUAL_EXPLANATION,
        description="Core pedagogical explanation method",
    )
    difficulty_level: int = Field(default=1, ge=1, le=5)
    language: str = Field(default="en")
    teacher_instructions: str | None = Field(default=None, description="Custom teacher guidance or context")


class InstructionalContentUpdate(BaseModel):
    """Payload for teacher modifications and status transitions."""
    title: str | None = None
    blocks: list[InstructionalBlock] | None = None
    summary: str | None = None
    status: InstructionalStatus | None = None
    teacher_notes: str | None = None


class InstructionalGenerateResponse(BaseModel):
    """Response returned upon generating instructional content."""
    content: InstructionalContentRead
    fallback_used: bool
    generation_source: str
    objective_id: uuid.UUID | str
    grounding_sources: list[dict[str, Any]] = Field(default_factory=list)
