"""
Eduvia — Content Bank Domain Layer Verification Tests

Validates:
- ContentBank initialization and indexing
- Objective-linked content item retrieval
- Modality-specific conversion from ContentItem to ActivityContent models
- Deterministic fallback activity generation via ContentBank
- Multilingual prompt support (EN/AR)
"""
from __future__ import annotations

import uuid

import pytest

from app.activities.schemas import (
    Activity,
    ActivityType,
    DragDropContent,
    MatchingContent,
    MultipleChoiceContent,
    OrderingContent,
    VisualIdentificationContent,
)
from app.content.bank import ContentBank, get_content_bank
from app.content.definitions import ALL_CONTENT_ITEMS


def test_content_bank_initialization() -> None:
    """Verify ContentBank initializes and indexes items properly."""
    bank = get_content_bank()
    assert len(bank.items) >= 40
    assert len(bank.by_objective) >= 15


def test_content_bank_retrieval_by_objective() -> None:
    """Verify retrieving content items linked to counting objective."""
    bank = get_content_bank()
    counting_obj_id = uuid.UUID("77777777-7777-7777-7777-777777777777")

    # Multiple Choice
    mc_item = bank.get_by_objective(counting_obj_id, ActivityType.MULTIPLE_CHOICE)
    assert mc_item is not None
    assert "multiple_choice" in mc_item.supported_modalities
    assert mc_item.get_prompt("en") is not None
    assert mc_item.get_prompt("ar") is not None

    # Matching
    match_item = bank.get_by_objective(counting_obj_id, ActivityType.MATCHING)
    assert match_item is not None
    assert "matching" in match_item.supported_modalities

    # Ordering
    order_item = bank.get_by_objective(counting_obj_id, ActivityType.ORDERING)
    assert order_item is not None
    assert "ordering" in order_item.supported_modalities

    # Visual Identification
    vis_item = bank.get_by_objective(counting_obj_id, ActivityType.VISUAL_IDENTIFICATION)
    assert vis_item is not None
    assert "visual_identification" in vis_item.supported_modalities

    # Drag and Drop
    drag_item = bank.get_by_objective(counting_obj_id, ActivityType.DRAG_DROP)
    assert drag_item is not None
    assert "drag_drop" in drag_item.supported_modalities


def test_convert_to_activity_content_multiple_choice() -> None:
    """Verify converting ContentItem to MultipleChoiceContent."""
    bank = get_content_bank()
    counting_obj_id = uuid.UUID("77777777-7777-7777-7777-777777777777")
    item = bank.get_by_objective(counting_obj_id, ActivityType.MULTIPLE_CHOICE)
    assert item is not None

    content = bank.convert_to_activity_content(item, ActivityType.MULTIPLE_CHOICE, "en")
    assert isinstance(content, MultipleChoiceContent)
    assert content.activity_type == ActivityType.MULTIPLE_CHOICE
    assert len(content.options) >= 2
    assert content.correct_answer_id in {opt.id for opt in content.options}


def test_convert_to_activity_content_matching() -> None:
    """Verify converting ContentItem to MatchingContent."""
    bank = get_content_bank()
    counting_obj_id = uuid.UUID("77777777-7777-7777-7777-777777777777")
    item = bank.get_by_objective(counting_obj_id, ActivityType.MATCHING)
    assert item is not None

    content = bank.convert_to_activity_content(item, ActivityType.MATCHING, "en")
    assert isinstance(content, MatchingContent)
    assert content.activity_type == ActivityType.MATCHING
    assert len(content.left_items) >= 2
    assert len(content.right_items) >= 2
    assert len(content.pairs) >= 2


def test_convert_to_activity_content_ordering() -> None:
    """Verify converting ContentItem to OrderingContent."""
    bank = get_content_bank()
    counting_obj_id = uuid.UUID("77777777-7777-7777-7777-777777777777")
    item = bank.get_by_objective(counting_obj_id, ActivityType.ORDERING)
    assert item is not None

    content = bank.convert_to_activity_content(item, ActivityType.ORDERING, "en")
    assert isinstance(content, OrderingContent)
    assert content.activity_type == ActivityType.ORDERING
    assert len(content.items) >= 3
    assert len(content.correct_sequence) == len(content.items)


def test_convert_to_activity_content_visual_identification() -> None:
    """Verify converting ContentItem to VisualIdentificationContent."""
    bank = get_content_bank()
    counting_obj_id = uuid.UUID("77777777-7777-7777-7777-777777777777")
    item = bank.get_by_objective(counting_obj_id, ActivityType.VISUAL_IDENTIFICATION)
    assert item is not None

    content = bank.convert_to_activity_content(item, ActivityType.VISUAL_IDENTIFICATION, "en")
    assert isinstance(content, VisualIdentificationContent)
    assert content.activity_type == ActivityType.VISUAL_IDENTIFICATION
    assert len(content.elements) >= 2
    assert content.target_id in {el.id for el in content.elements}


def test_convert_to_activity_content_drag_drop() -> None:
    """Verify converting ContentItem to DragDropContent."""
    bank = get_content_bank()
    counting_obj_id = uuid.UUID("77777777-7777-7777-7777-777777777777")
    item = bank.get_by_objective(counting_obj_id, ActivityType.DRAG_DROP)
    assert item is not None

    content = bank.convert_to_activity_content(item, ActivityType.DRAG_DROP, "en")
    assert isinstance(content, DragDropContent)
    assert content.activity_type == ActivityType.DRAG_DROP
    assert len(content.items) >= 2
    assert len(content.zones) >= 2
    assert len(content.correct_mapping) == len(content.items)


def test_create_fallback_activity_for_all_modalities() -> None:
    """Verify ContentBank creates a valid Pydantic Activity for every modality."""
    bank = get_content_bank()
    obj_id = uuid.UUID("77777777-7777-7777-7777-777777777777")

    for modality in ActivityType:
        activity = bank.create_fallback_activity_for_objective(
            objective_id=obj_id,
            activity_type=modality,
            difficulty_level=1,
            language="en",
        )
        assert isinstance(activity, Activity)
        assert activity.activity_type == modality
        assert activity.objective_id == obj_id
        assert len(activity.hints) >= 2
        # Validate that model re-validates cleanly
        Activity.model_validate(activity.model_dump())
