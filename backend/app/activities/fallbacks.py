"""
Eduvia — Deterministic Fallback Activity Generator (Phase 4)

Provides deterministic, schema-compliant fallback activities when LLM generation
is unavailable, times out, or fails schema validation.

Guarantees that a learner is NEVER blocked from instructional engagement due to
an AI provider outage or malformed JSON.
"""
from __future__ import annotations

import uuid
from typing import Any

from app.activities.schemas import (
    Activity,
    ActivityContent,
    ActivityType,
    DragDropContent,
    DragItem,
    DropZone,
    MatchingContent,
    MatchingItem,
    MatchingPair,
    MultipleChoiceContent,
    MultipleChoiceOption,
    OrderingContent,
    OrderingItem,
    VisualElement,
    VisualIdentificationContent,
)


def create_fallback_activity(
    objective_id: uuid.UUID,
    objective_title: str = "Learning Activity",
    objective_description: str | None = None,
    difficulty_level: int = 1,
    activity_type: ActivityType = ActivityType.MULTIPLE_CHOICE,
    language: str = "en",
) -> Activity:
    """
    Generate a robust, deterministic activity guaranteed to validate against Pydantic schemas.
    Leverages the authoritative ContentBank for real, curriculum-aligned educational content.
    """
    if not isinstance(activity_type, ActivityType):
        try:
            activity_type = ActivityType(activity_type)
        except (ValueError, KeyError):
            activity_type = ActivityType.MULTIPLE_CHOICE

    from app.content.bank import get_content_bank
    bank = get_content_bank()
    activity = bank.create_fallback_activity_for_objective(
        objective_id=objective_id,
        objective_title=objective_title,
        activity_type=activity_type,
        difficulty_level=difficulty_level,
        language=language,
    )
    if activity.metadata is None:
        activity.metadata = {}
    activity.metadata["fallback_used"] = True
    return activity

    return Activity(
        id=uuid.uuid4(),
        objective_id=objective_id,
        activity_type=activity_type,
        title=clean_title,
        instructions=desc,
        difficulty_level=difficulty_level,
        content=content,
        hints=[
            "Take your time and look carefully at the choices.",
            "Compare each item with what you have learned.",
        ],
        scaffolding_level=1,
        metadata={
            "fallback_used": True,
            "source": "deterministic_fallback",
            "language": language,
        },
    )
