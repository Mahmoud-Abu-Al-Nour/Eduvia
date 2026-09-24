"""
Eduvia — Content Bank Full Coverage & Quality Audit Tests

Strict verification covering:
1. Coverage across all 3 subjects, 13 units, and 70 curriculum learning objectives.
2. Every single learning objective has >= 3 authoritative items (minimum target)
   and >= 5 authoritative items (preferred target). Total items >= 350.
3. Content quality: No empty prompts, placeholder strings ("Item 1", "Item 2", "Correct representation"),
   missing correct answers, or broken payloads.
4. Schema validation: Every item's content_payload strictly validates against its respective Pydantic schema:
   - MultipleChoiceContent
   - MatchingContent
   - OrderingContent
   - VisualIdentificationContent
   - DragDropContent
5. Cross-domain representation: Mathematics, Literacy, Everyday Learning.
6. Modality coverage: All 5 activity types present and valid.
"""
from __future__ import annotations

import re
import pytest

from app.activities.schemas import (
    ActivityType,
    DragDropContent,
    MatchingContent,
    MultipleChoiceContent,
    OrderingContent,
    VisualIdentificationContent,
)
from app.content.bank import get_content_bank
from app.content.definitions import get_all_content_definitions
from app.curriculum.curriculum_catalog import (
    get_all_curriculum_objectives,
    get_target_curriculum_catalog,
)


@pytest.fixture(scope="module")
def content_bank():
    return get_content_bank()


@pytest.fixture(scope="module")
def all_items():
    return get_all_content_definitions()


@pytest.fixture(scope="module")
def curriculum_objectives():
    return get_all_curriculum_objectives()


def test_content_bank_total_item_count(all_items) -> None:
    """Audit Requirement 1: Content Bank must contain >= 350 authoritative items."""
    assert len(all_items) >= 350, f"Expected >= 350 items, got {len(all_items)}"


def test_content_bank_all_70_objectives_covered(all_items, curriculum_objectives) -> None:
    """Audit Requirement 1: Every one of the 70 learning objectives must have >= 5 items."""
    assert len(curriculum_objectives) == 70, f"Curriculum catalog must contain exactly 70 objectives, got {len(curriculum_objectives)}"

    # Group items by objective key
    by_obj: dict[str, list] = {}
    for item in all_items:
        by_obj.setdefault(item.objective_key, []).append(item)

    # Check coverage
    missing_objectives = []
    under_3_objectives = []
    under_5_objectives = []

    for obj in curriculum_objectives:
        key = obj["key"]
        items = by_obj.get(key, [])
        if len(items) == 0:
            missing_objectives.append(key)
        elif len(items) < 3:
            under_3_objectives.append((key, len(items)))
        elif len(items) < 5:
            under_5_objectives.append((key, len(items)))

    assert not missing_objectives, f"Objectives with 0 items: {missing_objectives}"
    assert not under_3_objectives, f"Objectives with < 3 items: {under_3_objectives}"
    assert not under_5_objectives, f"Objectives with < 5 items (preferred target): {under_5_objectives}"


def test_content_bank_cross_domain_distribution(all_items) -> None:
    """Audit Requirement 7: Math, Literacy, and Everyday Learning must all have rich content."""
    subjects = {item.subject_code for item in all_items}
    assert "math" in subjects
    assert "literacy" in subjects
    assert "everyday" in subjects

    math_count = sum(1 for item in all_items if item.subject_code == "math")
    lit_count = sum(1 for item in all_items if item.subject_code == "literacy")
    life_count = sum(1 for item in all_items if item.subject_code == "everyday")

    assert math_count >= 155, f"Expected >= 155 math items, got {math_count}"
    assert lit_count >= 100, f"Expected >= 100 literacy items, got {lit_count}"
    assert life_count >= 95, f"Expected >= 95 everyday learning items, got {life_count}"


def test_content_bank_all_five_modalities_represented(all_items) -> None:
    """Audit Requirement 4: All 5 modalities must be represented in the Content Bank."""
    modality_counts: dict[ActivityType, int] = {
        ActivityType.MULTIPLE_CHOICE: 0,
        ActivityType.MATCHING: 0,
        ActivityType.ORDERING: 0,
        ActivityType.VISUAL_IDENTIFICATION: 0,
        ActivityType.DRAG_DROP: 0,
    }

    for item in all_items:
        for mod in item.supported_modalities:
            if mod in modality_counts:
                modality_counts[mod] += 1

    for mod, count in modality_counts.items():
        assert count >= 10, f"Modality {mod.value} should have at least 10 items, got {count}"


def test_content_bank_quality_audit(all_items) -> None:
    """
    Audit Requirement 2: Automated validation test to detect:
    - empty prompts
    - placeholder strings ("Item 1", "Item 2", "Correct representation")
    - meaningless generic fallback content
    - missing correct answers
    - broken modality-specific payloads
    """
    forbidden_patterns = [
        re.compile(r"\bitem\s*\d+\b", re.IGNORECASE),
        re.compile(r"correct representation", re.IGNORECASE),
        re.compile(r"\bplaceholder\b", re.IGNORECASE),
        re.compile(r"lorem ipsum", re.IGNORECASE),
        re.compile(r"\b(foo|bar|baz)\b", re.IGNORECASE),
    ]

    quality_failures = []

    for item in all_items:
        # 1. Prompt check
        prompt_en = item.get_prompt("en")
        prompt_ar = item.get_prompt("ar")
        if not prompt_en or len(prompt_en.strip()) < 5:
            quality_failures.append(f"[{item.content_key}] Empty or trivial English prompt: '{prompt_en}'")
        if not prompt_ar or len(prompt_ar.strip()) < 3:
            quality_failures.append(f"[{item.content_key}] Empty or trivial Arabic prompt: '{prompt_ar}'")

        # Check for forbidden placeholder patterns in prompts
        for pat in forbidden_patterns:
            if pat.search(prompt_en):
                quality_failures.append(f"[{item.content_key}] Forbidden placeholder in prompt: '{prompt_en}'")

        # 2. Correct answer check
        if not item.correct_answer or len(item.correct_answer) == 0:
            quality_failures.append(f"[{item.content_key}] Missing correct_answer dict")

        # 3. Payload validation according to supported modality
        payload = item.content_payload
        for mod in item.supported_modalities:
            try:
                if mod == ActivityType.MULTIPLE_CHOICE:
                    mc_data = {
                        "activity_type": ActivityType.MULTIPLE_CHOICE,
                        "question": payload.get("question", prompt_en),
                        "options": payload.get("options", []),
                        "correct_answer_id": payload.get("correct_answer_id") or item.correct_answer.get("correct_answer_id"),
                        "explanation": payload.get("explanation", item.explanation.get("en", "Good job!")),
                    }
                    validated = MultipleChoiceContent(**mc_data)
                    # Check options quality
                    assert len(validated.options) >= 2
                    assert any(opt.id == validated.correct_answer_id for opt in validated.options)
                    for opt in validated.options:
                        for pat in forbidden_patterns:
                            if pat.search(opt.text):
                                quality_failures.append(f"[{item.content_key}] Placeholder in option text: '{opt.text}'")

                elif mod == ActivityType.MATCHING:
                    match_data = {
                        "activity_type": ActivityType.MATCHING,
                        "prompt": payload.get("prompt", prompt_en),
                        "left_items": payload.get("left_items", []),
                        "right_items": payload.get("right_items", []),
                        "pairs": payload.get("pairs") or item.correct_answer.get("pairs", []),
                    }
                    validated = MatchingContent(**match_data)
                    assert len(validated.left_items) >= 2
                    assert len(validated.right_items) >= 2
                    assert len(validated.pairs) >= 2

                elif mod == ActivityType.ORDERING:
                    order_data = {
                        "activity_type": ActivityType.ORDERING,
                        "prompt": payload.get("prompt", prompt_en),
                        "items": payload.get("items", []),
                        "correct_sequence": payload.get("correct_sequence") or item.correct_answer.get("correct_sequence", []),
                        "direction": payload.get("direction", "chronological"),
                    }
                    validated = OrderingContent(**order_data)
                    assert len(validated.items) >= 3
                    assert len(validated.correct_sequence) >= 3

                elif mod == ActivityType.VISUAL_IDENTIFICATION:
                    vis_data = {
                        "activity_type": ActivityType.VISUAL_IDENTIFICATION,
                        "prompt": payload.get("prompt", prompt_en),
                        "scene_description": payload.get("scene_description", "Visual scene"),
                        "elements": payload.get("elements", []),
                        "target_id": payload.get("target_id") or item.correct_answer.get("target_id"),
                        "feedback_clue": payload.get("feedback_clue", "Look closely"),
                    }
                    validated = VisualIdentificationContent(**vis_data)
                    assert len(validated.elements) >= 2
                    assert any(e.id == validated.target_id for e in validated.elements)

                elif mod == ActivityType.DRAG_DROP:
                    dd_data = {
                        "activity_type": ActivityType.DRAG_DROP,
                        "prompt": payload.get("prompt", prompt_en),
                        "items": payload.get("items", []),
                        "zones": payload.get("zones", []),
                        "correct_mapping": payload.get("correct_mapping") or item.correct_answer.get("correct_mapping", {}),
                    }
                    validated = DragDropContent(**dd_data)
                    assert len(validated.items) >= 2
                    assert len(validated.zones) >= 2
                    assert len(validated.correct_mapping) >= 2

            except Exception as e:
                quality_failures.append(f"[{item.content_key}] Payload validation failed for {mod.value}: {e}")

    assert not quality_failures, f"Quality failures detected ({len(quality_failures)}):\n" + "\n".join(quality_failures[:20])
