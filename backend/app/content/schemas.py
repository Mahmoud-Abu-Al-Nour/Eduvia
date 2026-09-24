"""
Eduvia — Content / Question Bank Schemas

Pydantic validation contracts for authoritative content items.
"""
from __future__ import annotations

import uuid
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.activities.schemas import ActivityType


class ContentItemBase(BaseModel):
    objective_id: uuid.UUID
    subject_code: str
    unit_code: str
    content_key: str
    difficulty_level: int = Field(default=1, ge=1, le=5)
    supported_modalities: list[ActivityType]
    language: str = "en"
    prompt: dict[str, str]
    content_payload: dict[str, Any]
    correct_answer: dict[str, Any]
    explanation: dict[str, str] | None = None
    hints: list[dict[str, str]] = Field(default_factory=list)
    metadata_info: dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True


class ContentItemCreate(ContentItemBase):
    pass


class ContentItemRead(ContentItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
