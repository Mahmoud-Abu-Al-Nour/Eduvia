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
    objective_title: str,
    objective_description: str | None = None,
    difficulty_level: int = 1,
    activity_type: ActivityType = ActivityType.MULTIPLE_CHOICE,
    language: str = "en",
) -> Activity:
    """
    Generate a robust, deterministic activity guaranteed to validate against Pydantic schemas.
    """
    clean_title = objective_title or "Foundational Practice"
    desc = objective_description or "Complete the following practice step."
    content: ActivityContent

    if activity_type == ActivityType.MULTIPLE_CHOICE:
        content = MultipleChoiceContent(
            activity_type=ActivityType.MULTIPLE_CHOICE,
            question=f"Which option best represents: {clean_title}?",
            options=[
                MultipleChoiceOption(
                    id="opt_1",
                    text="Correct representation",
                    is_correct=True,
                    distractor_rationale=None,
                ),
                MultipleChoiceOption(
                    id="opt_2",
                    text="Alternative count or item",
                    is_correct=False,
                    distractor_rationale="Provides a common nearby estimate.",
                ),
                MultipleChoiceOption(
                    id="opt_3",
                    text="Unrelated quantity",
                    is_correct=False,
                    distractor_rationale="Clear distractor for confidence building.",
                ),
            ],
            correct_answer_id="opt_1",
            explanation="Excellent effort! That is the correct match.",
        )
    elif activity_type == ActivityType.MATCHING:
        content = MatchingContent(
            activity_type=ActivityType.MATCHING,
            prompt=f"Match each item to its corresponding pair for: {clean_title}",
            left_items=[
                MatchingItem(id="left_1", label="Item 1", visual_cue="circle"),
                MatchingItem(id="left_2", label="Item 2", visual_cue="square"),
                MatchingItem(id="left_3", label="Item 3", visual_cue="triangle"),
            ],
            right_items=[
                MatchingItem(id="right_1", label="Pair 1", visual_cue="circle"),
                MatchingItem(id="right_2", label="Pair 2", visual_cue="square"),
                MatchingItem(id="right_3", label="Pair 3", visual_cue="triangle"),
            ],
            pairs=[
                MatchingPair(left_id="left_1", right_id="right_1"),
                MatchingPair(left_id="left_2", right_id="right_2"),
                MatchingPair(left_id="left_3", right_id="right_3"),
            ],
        )
    elif activity_type == ActivityType.ORDERING:
        content = OrderingContent(
            activity_type=ActivityType.ORDERING,
            prompt=f"Arrange these items in sequential order: {clean_title}",
            items=[
                OrderingItem(id="ord_3", label="Step 3 / Number 3"),
                OrderingItem(id="ord_1", label="Step 1 / Number 1"),
                OrderingItem(id="ord_2", label="Step 2 / Number 2"),
            ],
            correct_sequence=["ord_1", "ord_2", "ord_3"],
            direction="ascending",
        )
    elif activity_type == ActivityType.VISUAL_IDENTIFICATION:
        content = VisualIdentificationContent(
            activity_type=ActivityType.VISUAL_IDENTIFICATION,
            prompt=f"Find the target item for: {clean_title}",
            scene_description=f"A calm workspace showing visual items related to {clean_title}.",
            elements=[
                VisualElement(
                    id="elem_target",
                    label="Target Element",
                    category="target",
                    is_target=True,
                    bounding_hint="center",
                ),
                VisualElement(
                    id="elem_distractor",
                    label="Background Object",
                    category="background",
                    is_target=False,
                    bounding_hint="left",
                ),
            ],
            target_id="elem_target",
            feedback_clue="Look towards the center of the display.",
        )
    elif activity_type == ActivityType.DRAG_DROP:
        content = DragDropContent(
            activity_type=ActivityType.DRAG_DROP,
            prompt=f"Sort items into their target groups: {clean_title}",
            items=[
                DragItem(id="drag_1", label="Element A"),
                DragItem(id="drag_2", label="Element B"),
                DragItem(id="drag_3", label="Element C"),
            ],
            zones=[
                DropZone(id="zone_1", label="Group 1", capacity=3),
                DropZone(id="zone_2", label="Group 2", capacity=3),
            ],
            correct_mapping={
                "drag_1": "zone_1",
                "drag_2": "zone_2",
                "drag_3": "zone_1",
            },
        )
    else:
        # Default fallback to multiple choice
        return create_fallback_activity(
            objective_id=objective_id,
            objective_title=objective_title,
            objective_description=objective_description,
            difficulty_level=difficulty_level,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            language=language,
        )

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
