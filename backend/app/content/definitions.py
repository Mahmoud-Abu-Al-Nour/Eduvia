"""
Eduvia — Authoritative Content Bank Definitions

Provides rich, structured educational items for all learning objectives across:
- Foundational Mathematics
- Early Literacy
- Everyday Learning Skills

Covers all 5 modalities:
1. multiple_choice
2. matching
3. ordering
4. visual_identification
5. drag_drop

Every item contains authoritative question prompts, options/elements, answer keys,
and pedagogical explanations in English and Arabic.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from app.activities.schemas import ActivityType
from app.curriculum.curriculum_catalog import get_curriculum_uuid

CONTENT_NAMESPACE = uuid.UUID("44444444-5555-6666-7777-888888888888")


def get_content_uuid(content_key: str) -> uuid.UUID:
    return uuid.uuid5(CONTENT_NAMESPACE, content_key)


@dataclass(frozen=True)
class ContentItemDef:
    content_key: str
    objective_key: str
    subject_code: str
    unit_code: str
    difficulty_level: int
    supported_modalities: list[ActivityType]
    prompt: dict[str, str]
    content_payload: dict[str, Any]
    correct_answer: dict[str, Any]
    explanation: dict[str, str]
    hints: list[dict[str, str]] = field(default_factory=list)
    metadata_info: dict[str, Any] = field(default_factory=dict)
    language: str = "en"

    @property
    def id(self) -> uuid.UUID:
        return get_content_uuid(self.content_key)

    @property
    def objective_id(self) -> uuid.UUID:
        return get_curriculum_uuid(self.objective_key)

    def get_prompt(self, lang: str = "en") -> str:
        return self.prompt.get(lang, self.prompt.get("en", ""))


def get_all_content_definitions() -> list[ContentItemDef]:
    """Return the authoritative list of educational content bank items."""
    items: list[ContentItemDef] = []

    # ══════════════════════════════════════════════════════════════════════════
    # MATHEMATICS - UNIT 1: NUMBER SENSE & COUNTING
    # ══════════════════════════════════════════════════════════════════════════

    # 1. obj.math.count_0_5
    items.append(
        ContentItemDef(
            content_key="math.cnt05.mc.num3",
            objective_key="obj.math.count_0_5",
            subject_code="math",
            unit_code="unit.math.number_sense",
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "Which number shows the numeral 3?", "ar": "أي رقم يمثل الرقم ٣؟"},
            content_payload={
                "question": "Which number shows the numeral 3?",
                "options": [
                    {"id": "opt_1", "text": "1", "visual_cue": "1️⃣", "is_correct": False, "distractor_rationale": "Single unit"},
                    {"id": "opt_2", "text": "3", "visual_cue": "3️⃣", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_3", "text": "5", "visual_cue": "5️⃣", "is_correct": False, "distractor_rationale": "Upper boundary of 0-5"},
                ],
                "correct_answer_id": "opt_2",
                "explanation": "Great job! This is the numeral 3.",
            },
            correct_answer={"correct_answer_id": "opt_2"},
            explanation={"en": "Great job! This is the numeral 3.", "ar": "أحسنت! هذا هو الرقم ٣."},
            hints=[
                {"en": "Look for the numeral with two rounded loops.", "ar": "ابحث عن الرقم الذي يحتوي على انحناءين."},
                {"en": "It comes right after 2.", "ar": "إنه يأتي مباشرة بعد الرقم ٢."},
            ],
            metadata_info={"domain": "numeracy", "numeral": 3},
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.cnt05.match.dot_cards",
            objective_key="obj.math.count_0_5",
            subject_code="math",
            unit_code="unit.math.number_sense",
            difficulty_level=1,
            supported_modalities=[ActivityType.MATCHING],
            prompt={"en": "Match each numeral to its count of stars.", "ar": "طابق كل رقم بعدد النجوم."},
            content_payload={
                "prompt": "Match each numeral to its count of stars.",
                "left_items": [
                    {"id": "left_1", "label": "1", "visual_cue": "1️⃣"},
                    {"id": "left_2", "label": "2", "visual_cue": "2️⃣"},
                    {"id": "left_3", "label": "4", "visual_cue": "4️⃣"},
                ],
                "right_items": [
                    {"id": "right_1", "label": "⭐", "visual_cue": "One star"},
                    {"id": "right_2", "label": "⭐⭐", "visual_cue": "Two stars"},
                    {"id": "right_3", "label": "⭐⭐⭐⭐", "visual_cue": "Four stars"},
                ],
                "pairs": [
                    {"left_id": "left_1", "right_id": "right_1"},
                    {"left_id": "left_2", "right_id": "right_2"},
                    {"left_id": "left_3", "right_id": "right_3"},
                ],
            },
            correct_answer={"pairs": [{"left_id": "left_1", "right_id": "right_1"}, {"left_id": "left_2", "right_id": "right_2"}, {"left_id": "left_3", "right_id": "right_3"}]},
            explanation={"en": "Excellent matching! 1 star matches 1, 2 stars match 2, and 4 stars match 4.", "ar": "مطابقة ممتازة! نجمة واحدة لـ ١، ونجمتان لـ ٢، وأربع نجوم لـ ٤."},
            hints=[
                {"en": "Count the stars in each card one by one.", "ar": "قم بعد النجوم في كل بطاقة واحدة تلو الأخرى."},
            ],
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.cnt05.vis.find_num4",
            objective_key="obj.math.count_0_5",
            subject_code="math",
            unit_code="unit.math.number_sense",
            difficulty_level=1,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={"en": "Find the numeral 4 on the board.", "ar": "ابحث عن الرقم ٤ على اللوحة."},
            content_payload={
                "prompt": "Find the numeral 4 on the board.",
                "scene_description": "A calm classroom chalkboard displaying numerals 1, 4, and 5.",
                "elements": [
                    {"id": "elem_1", "label": "Numeral 1", "category": "number", "is_target": False, "bounding_hint": "left"},
                    {"id": "elem_4", "label": "Numeral 4", "category": "number", "is_target": True, "bounding_hint": "center"},
                    {"id": "elem_5", "label": "Numeral 5", "category": "number", "is_target": False, "bounding_hint": "right"},
                ],
                "target_id": "elem_4",
                "feedback_clue": "Look in the center for the number four.",
            },
            correct_answer={"target_id": "elem_4"},
            explanation={"en": "Wonderful observation! You spotted the number 4.", "ar": "ملاحظة رائعة! لقد حددت الرقم ٤."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.cnt05.order.seq123",
            objective_key="obj.math.count_0_5",
            subject_code="math",
            unit_code="unit.math.number_sense",
            difficulty_level=1,
            supported_modalities=[ActivityType.ORDERING],
            prompt={"en": "Put the numbers in order from 1 to 3.", "ar": "رتب الأرقام من ١ إلى ٣."},
            content_payload={
                "prompt": "Put the numbers in order from 1 to 3.",
                "items": [
                    {"id": "ord_2", "label": "2", "visual_cue": "2️⃣"},
                    {"id": "ord_1", "label": "1", "visual_cue": "1️⃣"},
                    {"id": "ord_3", "label": "3", "visual_cue": "3️⃣"},
                ],
                "correct_sequence": ["ord_1", "ord_2", "ord_3"],
                "direction": "ascending",
            },
            correct_answer={"correct_sequence": ["ord_1", "ord_2", "ord_3"]},
            explanation={"en": "Spot on! Counting order is 1, then 2, then 3.", "ar": "ممتاز! تسلسل العد هو ١، ثم ٢، ثم ٣."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.cnt05.drag.sort_1and2",
            objective_key="obj.math.count_0_5",
            subject_code="math",
            unit_code="unit.math.number_sense",
            difficulty_level=1,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={"en": "Sort the items: put single items in 'One' and pairs in 'Two'.", "ar": "فرز العناصر: ضع العناصر الفردية في 'واحد' والأزواج في 'اثنان'."},
            content_payload={
                "prompt": "Sort the items: put single items in 'One' and pairs in 'Two'.",
                "items": [
                    {"id": "drag_apple_1", "label": "Single Apple 🍎", "visual_cue": "🍎"},
                    {"id": "drag_apple_2", "label": "Two Apples 🍎🍎", "visual_cue": "🍎🍎"},
                    {"id": "drag_star_1", "label": "Single Star ⭐", "visual_cue": "⭐"},
                ],
                "zones": [
                    {"id": "zone_one", "label": "Group: 1 Item", "capacity": 3},
                    {"id": "zone_two", "label": "Group: 2 Items", "capacity": 3},
                ],
                "correct_mapping": {
                    "drag_apple_1": "zone_one",
                    "drag_apple_2": "zone_two",
                    "drag_star_1": "zone_one",
                },
            },
            correct_answer={"correct_mapping": {"drag_apple_1": "zone_one", "drag_apple_2": "zone_two", "drag_star_1": "zone_one"}},
            explanation={"en": "Perfect sorting! Single items in group 1, pairs in group 2.", "ar": "فرز مثالي! العناصر الفردية في مجموعة ١، والأزواج في مجموعة ٢."},
        )
    )

    # 2. obj.math.count_6_10
    items.append(
        ContentItemDef(
            content_key="math.cnt610.mc.num7",
            objective_key="obj.math.count_6_10",
            subject_code="math",
            unit_code="unit.math.number_sense",
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "Which numeral represents 7?", "ar": "أي رقم يمثل ٧؟"},
            content_payload={
                "question": "Which numeral represents 7?",
                "options": [
                    {"id": "opt_6", "text": "6", "visual_cue": "6️⃣", "is_correct": False, "distractor_rationale": "One less than seven"},
                    {"id": "opt_7", "text": "7", "visual_cue": "7️⃣", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_9", "text": "9", "visual_cue": "9️⃣", "is_correct": False, "distractor_rationale": "Larger digit"},
                ],
                "correct_answer_id": "opt_7",
                "explanation": "Correct! That is the numeral 7.",
            },
            correct_answer={"correct_answer_id": "opt_7"},
            explanation={"en": "Correct! That is the numeral 7.", "ar": "صحيح! هذا هو الرقم ٧."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.cnt610.order.seq678",
            objective_key="obj.math.count_6_10",
            subject_code="math",
            unit_code="unit.math.number_sense",
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={"en": "Put the numbers in order from 6 to 9.", "ar": "رتب الأرقام من ٦ إلى ٩."},
            content_payload={
                "prompt": "Put the numbers in order from 6 to 9.",
                "items": [
                    {"id": "ord_8", "label": "8", "visual_cue": "8️⃣"},
                    {"id": "ord_6", "label": "6", "visual_cue": "6️⃣"},
                    {"id": "ord_7", "label": "7", "visual_cue": "7️⃣"},
                    {"id": "ord_9", "label": "9", "visual_cue": "9️⃣"},
                ],
                "correct_sequence": ["ord_6", "ord_7", "ord_8", "ord_9"],
                "direction": "ascending",
            },
            correct_answer={"correct_sequence": ["ord_6", "ord_7", "ord_8", "ord_9"]},
            explanation={"en": "Terrific! 6, 7, 8, 9 is the correct sequence.", "ar": "رائع! ٦، ٧، ٨، ٩ هو التسلسل الصحيح."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.cnt610.match.num_dots",
            objective_key="obj.math.count_6_10",
            subject_code="math",
            unit_code="unit.math.number_sense",
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={"en": "Connect numerals 6, 8, 10 to their dot cards.", "ar": "طابق الأرقام ٦، ٨، ١٠ ببطاقات النقاط المناسبة."},
            content_payload={
                "prompt": "Connect numerals 6, 8, 10 to their dot cards.",
                "left_items": [
                    {"id": "left_6", "label": "6", "visual_cue": "6️⃣"},
                    {"id": "left_8", "label": "8", "visual_cue": "8️⃣"},
                    {"id": "left_10", "label": "10", "visual_cue": "🔟"},
                ],
                "right_items": [
                    {"id": "right_6", "label": "●●●●●●", "visual_cue": "6 dots"},
                    {"id": "right_8", "label": "●●●●●●●●", "visual_cue": "8 dots"},
                    {"id": "right_10", "label": "●●●●●●●●●●", "visual_cue": "10 dots"},
                ],
                "pairs": [
                    {"left_id": "left_6", "right_id": "right_6"},
                    {"left_id": "left_8", "right_id": "right_8"},
                    {"left_id": "left_10", "right_id": "right_10"},
                ],
            },
            correct_answer={"pairs": [{"left_id": "left_6", "right_id": "right_6"}, {"left_id": "left_8", "right_id": "right_8"}, {"left_id": "left_10", "right_id": "right_10"}]},
            explanation={"en": "All pairs connected accurately!", "ar": "جميع الأزواج متصلة بدقة!"},
        )
    )

    # 3. obj.math.count_objects_0_5
    items.append(
        ContentItemDef(
            content_key="math.cntobj05.mc.count_apples",
            objective_key="obj.math.count_objects_0_5",
            subject_code="math",
            unit_code="unit.math.number_sense",
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "How many apples are shown: 🍎 🍎 🍎?", "ar": "كم تفاحة معروضة: 🍎 🍎 🍎؟"},
            content_payload={
                "question": "How many apples are shown: 🍎 🍎 🍎?",
                "options": [
                    {"id": "opt_2", "text": "2", "visual_cue": "2", "is_correct": False, "distractor_rationale": "Under-count"},
                    {"id": "opt_3", "text": "3", "visual_cue": "3", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_4", "text": "4", "visual_cue": "4", "is_correct": False, "distractor_rationale": "Over-count by 1"},
                ],
                "correct_answer_id": "opt_3",
                "explanation": "Spot on! There are 3 apples.",
            },
            correct_answer={"correct_answer_id": "opt_3"},
            explanation={"en": "Spot on! There are 3 apples.", "ar": "ممتاز! هناك ٣ تفاحات."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.cntobj05.vis.group_of_5",
            objective_key="obj.math.count_objects_0_5",
            subject_code="math",
            unit_code="unit.math.number_sense",
            difficulty_level=1,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={"en": "Select the basket that has exactly 5 oranges.", "ar": "اختر السلة التي تحتوي على ٥ برتقالات بالضبط."},
            content_payload={
                "prompt": "Select the basket that has exactly 5 oranges.",
                "scene_description": "Three fruit baskets placed on a wooden table.",
                "elements": [
                    {"id": "basket_2", "label": "Basket with 2 oranges", "category": "basket", "is_target": False, "bounding_hint": "left"},
                    {"id": "basket_5", "label": "Basket with 5 oranges", "category": "basket", "is_target": True, "bounding_hint": "center"},
                    {"id": "basket_3", "label": "Basket with 3 oranges", "category": "basket", "is_target": False, "bounding_hint": "right"},
                ],
                "target_id": "basket_5",
                "feedback_clue": "Look in the middle basket and count 1, 2, 3, 4, 5.",
            },
            correct_answer={"target_id": "basket_5"},
            explanation={"en": "Great counting! The center basket holds 5 oranges.", "ar": "عد رائع! السلة الوسطى تحتوي على ٥ برتقالات."},
        )
    )

    # 4. obj.math.count_objects_6_10
    items.append(
        ContentItemDef(
            content_key="math.cntobj610.mc.eight_stars",
            objective_key="obj.math.count_objects_6_10",
            subject_code="math",
            unit_code="unit.math.number_sense",
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "Count the stars: ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐. How many are there?", "ar": "عد النجوم: ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐. كم عددها؟"},
            content_payload={
                "question": "Count the stars: ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐. How many are there?",
                "options": [
                    {"id": "opt_7", "text": "7", "visual_cue": "7", "is_correct": False, "distractor_rationale": "One less"},
                    {"id": "opt_8", "text": "8", "visual_cue": "8", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_9", "text": "9", "visual_cue": "9", "is_correct": False, "distractor_rationale": "One more"},
                ],
                "correct_answer_id": "opt_8",
                "explanation": "Exactly right! There are 8 stars.",
            },
            correct_answer={"correct_answer_id": "opt_8"},
            explanation={"en": "Exactly right! There are 8 stars.", "ar": "صحيح تماماً! هناك ٨ نجوم."},
        )
    )

    # 5. obj.math.numeral_qty_match
    items.append(
        ContentItemDef(
            content_key="math.matchqty.pairs_357",
            objective_key="obj.math.numeral_qty_match",
            subject_code="math",
            unit_code="unit.math.number_sense",
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={"en": "Match each numeral to its matching quantity.", "ar": "طابق كل رقم بالكمية المطابقة له."},
            content_payload={
                "prompt": "Match each numeral to its matching quantity.",
                "left_items": [
                    {"id": "num_3", "label": "3", "visual_cue": "3️⃣"},
                    {"id": "num_5", "label": "5", "visual_cue": "5️⃣"},
                    {"id": "num_7", "label": "7", "visual_cue": "7️⃣"},
                ],
                "right_items": [
                    {"id": "qty_3", "label": "🟢🟢🟢", "visual_cue": "Three circles"},
                    {"id": "qty_5", "label": "🟢🟢🟢🟢🟢", "visual_cue": "Five circles"},
                    {"id": "qty_7", "label": "🟢🟢🟢🟢🟢🟢🟢", "visual_cue": "Seven circles"},
                ],
                "pairs": [
                    {"left_id": "num_3", "right_id": "qty_3"},
                    {"left_id": "num_5", "right_id": "qty_5"},
                    {"left_id": "num_7", "right_id": "qty_7"},
                ],
            },
            correct_answer={"pairs": [{"left_id": "num_3", "right_id": "qty_3"}, {"left_id": "num_5", "right_id": "qty_5"}, {"left_id": "num_7", "right_id": "qty_7"}]},
            explanation={"en": "Super job! All quantities match their numerals.", "ar": "عمل رائع! كل الكميات تطابق أرقامها."},
        )
    )

    # 6. obj.math.compare_quantities
    items.append(
        ContentItemDef(
            content_key="math.cmp.more_less",
            objective_key="obj.math.compare_quantities",
            subject_code="math",
            unit_code="unit.math.number_sense",
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "Group A has 6 balls ⚽. Group B has 3 balls ⚽. Which group has MORE?", "ar": "المجموعة أ بها ٦ كرات ⚽. المجموعة ب بها ٣ كرات ⚽. أي مجموعة بها أكثر؟"},
            content_payload={
                "question": "Group A has 6 balls ⚽. Group B has 3 balls ⚽. Which group has MORE?",
                "options": [
                    {"id": "opt_a", "text": "Group A (6 balls)", "visual_cue": "⚽x6", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_b", "text": "Group B (3 balls)", "visual_cue": "⚽x3", "is_correct": False, "distractor_rationale": "Fewer count"},
                    {"id": "opt_eq", "text": "They are equal", "visual_cue": "=", "is_correct": False, "distractor_rationale": "Unequal quantities"},
                ],
                "correct_answer_id": "opt_a",
                "explanation": "6 is greater than 3, so Group A has more!",
            },
            correct_answer={"correct_answer_id": "opt_a"},
            explanation={"en": "6 is greater than 3, so Group A has more!", "ar": "٦ أكبر من ٣، إذن المجموعة أ تحتوي على عدد أكبر!"},
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # MATHEMATICS - UNIT 2: NUMBER SEQUENCE
    # ══════════════════════════════════════════════════════════════════════════
    items.append(
        ContentItemDef(
            content_key="math.seq.before_5",
            objective_key="obj.math.number_before",
            subject_code="math",
            unit_code="unit.math.number_sequence",
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "Which number comes right BEFORE 5?", "ar": "ما هو الرقم الذي يأتي مباشرة قبل الرقم ٥؟"},
            content_payload={
                "question": "Which number comes right BEFORE 5?",
                "options": [
                    {"id": "opt_3", "text": "3", "visual_cue": "3", "is_correct": False, "distractor_rationale": "Two before"},
                    {"id": "opt_4", "text": "4", "visual_cue": "4", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_6", "text": "6", "visual_cue": "6", "is_correct": False, "distractor_rationale": "Comes after"},
                ],
                "correct_answer_id": "opt_4",
                "explanation": "4 comes immediately before 5 when counting.",
            },
            correct_answer={"correct_answer_id": "opt_4"},
            explanation={"en": "4 comes immediately before 5 when counting.", "ar": "الرقم ٤ يأتي مباشرة قبل الرقم ٥ عند العد."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.seq.after_6",
            objective_key="obj.math.number_after",
            subject_code="math",
            unit_code="unit.math.number_sequence",
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "Which number comes right AFTER 6?", "ar": "ما هو الرقم الذي يأتي مباشرة بعد الرقم ٦؟"},
            content_payload={
                "question": "Which number comes right AFTER 6?",
                "options": [
                    {"id": "opt_5", "text": "5", "visual_cue": "5", "is_correct": False, "distractor_rationale": "Predecessor"},
                    {"id": "opt_7", "text": "7", "visual_cue": "7", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_8", "text": "8", "visual_cue": "8", "is_correct": False, "distractor_rationale": "Two after"},
                ],
                "correct_answer_id": "opt_7",
                "explanation": "7 comes immediately after 6.",
            },
            correct_answer={"correct_answer_id": "opt_7"},
            explanation={"en": "7 comes immediately after 6.", "ar": "الرقم ٧ يأتي مباشرة بعد الرقم ٦."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.seq.order_asc_1to5",
            objective_key="obj.math.order_smallest_largest",
            subject_code="math",
            unit_code="unit.math.number_sequence",
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={"en": "Order from smallest to largest: 2, 4, 1, 5, 3", "ar": "رتب من الأصغر إلى الأكبر: ٢، ٤، ١، ٥، ٣"},
            content_payload={
                "prompt": "Order from smallest to largest: 2, 4, 1, 5, 3",
                "items": [
                    {"id": "item_4", "label": "4", "visual_cue": "4️⃣"},
                    {"id": "item_1", "label": "1", "visual_cue": "1️⃣"},
                    {"id": "item_5", "label": "5", "visual_cue": "5️⃣"},
                    {"id": "item_2", "label": "2", "visual_cue": "2️⃣"},
                    {"id": "item_3", "label": "3", "visual_cue": "3️⃣"},
                ],
                "correct_sequence": ["item_1", "item_2", "item_3", "item_4", "item_5"],
                "direction": "ascending",
            },
            correct_answer={"correct_sequence": ["item_1", "item_2", "item_3", "item_4", "item_5"]},
            explanation={"en": "Awesome! 1, 2, 3, 4, 5 is the correct ascending order.", "ar": "رائع! ١، ٢، ٣، ٤، ٥ هو الترتيب التصاعدي الصحيح."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.seq.missing_num",
            objective_key="obj.math.complete_missing_sequence",
            subject_code="math",
            unit_code="unit.math.number_sequence",
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "Complete the sequence: 2, 3, [ ? ], 5, 6", "ar": "أكمل التسلسل: ٢، ٣، [ ؟ ]، ٥، ٦"},
            content_payload={
                "question": "Complete the sequence: 2, 3, [ ? ], 5, 6",
                "options": [
                    {"id": "opt_1", "text": "1", "visual_cue": "1", "is_correct": False, "distractor_rationale": "Before sequence"},
                    {"id": "opt_4", "text": "4", "visual_cue": "4", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_7", "text": "7", "visual_cue": "7", "is_correct": False, "distractor_rationale": "After sequence"},
                ],
                "correct_answer_id": "opt_4",
                "explanation": "4 fills the gap between 3 and 5.",
            },
            correct_answer={"correct_answer_id": "opt_4"},
            explanation={"en": "4 fills the gap between 3 and 5.", "ar": "الرقم ٤ يملأ الفراغ بين ٣ و ٥."},
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # MATHEMATICS - UNIT 3: ADDITION WITHIN 10
    # ══════════════════════════════════════════════════════════════════════════
    items.append(
        ContentItemDef(
            content_key="math.add.combine_2_plus_3",
            objective_key="obj.math.combine_two_groups",
            subject_code="math",
            unit_code="unit.math.addition_within_10",
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "Combine 2 blue stars ⭐⭐ and 3 gold stars ⭐⭐⭐. How many stars in all?", "ar": "ضم نجمتين زرقاوين ⭐⭐ و ٣ نجوم ذهبية ⭐⭐⭐. كم المجموع الكلي؟"},
            content_payload={
                "question": "Combine 2 blue stars ⭐⭐ and 3 gold stars ⭐⭐⭐. How many stars in all?",
                "options": [
                    {"id": "opt_4", "text": "4", "visual_cue": "4", "is_correct": False, "distractor_rationale": "Undercount by 1"},
                    {"id": "opt_5", "text": "5", "visual_cue": "5", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_6", "text": "6", "visual_cue": "6", "is_correct": False, "distractor_rationale": "Overcount by 1"},
                ],
                "correct_answer_id": "opt_5",
                "explanation": "2 plus 3 equals 5 total stars!",
            },
            correct_answer={"correct_answer_id": "opt_5"},
            explanation={"en": "2 plus 3 equals 5 total stars!", "ar": "٢ زائد ٣ يساوي ٥ نجوم في المجموع!"},
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.add.eq_4_plus_2",
            objective_key="obj.math.solve_addition_equations_10",
            subject_code="math",
            unit_code="unit.math.addition_within_10",
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "What is 4 + 2?", "ar": "ما هو ناتج ٤ + ٢؟"},
            content_payload={
                "question": "What is 4 + 2?",
                "options": [
                    {"id": "opt_5", "text": "5", "visual_cue": "5", "is_correct": False, "distractor_rationale": "Close neighbor"},
                    {"id": "opt_6", "text": "6", "visual_cue": "6", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_7", "text": "7", "visual_cue": "7", "is_correct": False, "distractor_rationale": "4 + 3"},
                ],
                "correct_answer_id": "opt_6",
                "explanation": "4 + 2 = 6.",
            },
            correct_answer={"correct_answer_id": "opt_6"},
            explanation={"en": "4 + 2 = 6.", "ar": "٤ + ٢ = ٦."},
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # MATHEMATICS - UNIT 4: SUBTRACTION WITHIN 10
    # ══════════════════════════════════════════════════════════════════════════
    items.append(
        ContentItemDef(
            content_key="math.sub.remain_5_minus_2",
            objective_key="obj.math.identify_remaining_objects",
            subject_code="math",
            unit_code="unit.math.subtraction_within_10",
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "There are 5 birds on a branch 🐦. 2 fly away. How many remain?", "ar": "هناك ٥ عصافير على الغصن 🐦. طار اثنان منها. كم عصفوراً بقي؟"},
            content_payload={
                "question": "There are 5 birds on a branch 🐦. 2 fly away. How many remain?",
                "options": [
                    {"id": "opt_2", "text": "2", "visual_cue": "2", "is_correct": False, "distractor_rationale": "Count removed"},
                    {"id": "opt_3", "text": "3", "visual_cue": "3", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_4", "text": "4", "visual_cue": "4", "is_correct": False, "distractor_rationale": "Only one removed"},
                ],
                "correct_answer_id": "opt_3",
                "explanation": "5 take away 2 leaves 3 birds.",
            },
            correct_answer={"correct_answer_id": "opt_3"},
            explanation={"en": "5 take away 2 leaves 3 birds.", "ar": "٥ ناقص ٢ يتبقى ٣ عصافير."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.sub.eq_7_minus_3",
            objective_key="obj.math.solve_subtraction_equations_10",
            subject_code="math",
            unit_code="unit.math.subtraction_within_10",
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "What is 7 - 3?", "ar": "ما هو ناتج ٧ - ٣؟"},
            content_payload={
                "question": "What is 7 - 3?",
                "options": [
                    {"id": "opt_3", "text": "3", "visual_cue": "3", "is_correct": False, "distractor_rationale": "Subtrahend"},
                    {"id": "opt_4", "text": "4", "visual_cue": "4", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_5", "text": "5", "visual_cue": "5", "is_correct": False, "distractor_rationale": "Over-estimate"},
                ],
                "correct_answer_id": "opt_4",
                "explanation": "7 minus 3 equals 4.",
            },
            correct_answer={"correct_answer_id": "opt_4"},
            explanation={"en": "7 minus 3 equals 4.", "ar": "٧ ناقص ٣ يساوي ٤."},
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # MATHEMATICS - UNIT 5: BASIC SHAPES & CLASSIFICATION
    # ══════════════════════════════════════════════════════════════════════════
    items.append(
        ContentItemDef(
            content_key="math.shape.id_circle",
            objective_key="obj.math.identify_circle",
            subject_code="math",
            unit_code="unit.math.shapes_classification",
            difficulty_level=1,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={"en": "Which shape is a circle?", "ar": "أي شكل هو دائرة؟"},
            content_payload={
                "prompt": "Which shape is a circle?",
                "scene_description": "Geometric shapes resting on an easel: a square, a circle, and a triangle.",
                "elements": [
                    {"id": "shape_sq", "label": "Square", "category": "shape", "is_target": False, "bounding_hint": "left"},
                    {"id": "shape_circ", "label": "Circle", "category": "shape", "is_target": True, "bounding_hint": "center"},
                    {"id": "shape_tri", "label": "Triangle", "category": "shape", "is_target": False, "bounding_hint": "right"},
                ],
                "target_id": "shape_circ",
                "feedback_clue": "Look for the round shape with no corners.",
            },
            correct_answer={"target_id": "shape_circ"},
            explanation={"en": "A circle is perfectly round with no straight sides or corners.", "ar": "الدائرة مستديرة بالكامل وليس لها أضلاع مستقيمة أو زوايا."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.shape.match_shapes",
            objective_key="obj.math.match_identical_shapes",
            subject_code="math",
            unit_code="unit.math.shapes_classification",
            difficulty_level=1,
            supported_modalities=[ActivityType.MATCHING],
            prompt={"en": "Match each shape to its identical partner.", "ar": "طابق كل شكل بمثيله المتطابق."},
            content_payload={
                "prompt": "Match each shape to its identical partner.",
                "left_items": [
                    {"id": "left_circ", "label": "Circle", "visual_cue": "⚪"},
                    {"id": "left_sq", "label": "Square", "visual_cue": "🟦"},
                    {"id": "left_tri", "label": "Triangle", "visual_cue": "🔺"},
                ],
                "right_items": [
                    {"id": "right_circ", "label": "Round Ring", "visual_cue": "⚪"},
                    {"id": "right_sq", "label": "Box Block", "visual_cue": "🟦"},
                    {"id": "right_tri", "label": "Roof Shape", "visual_cue": "🔺"},
                ],
                "pairs": [
                    {"left_id": "left_circ", "right_id": "right_circ"},
                    {"left_id": "left_sq", "right_id": "right_sq"},
                    {"left_id": "left_tri", "right_id": "right_tri"},
                ],
            },
            correct_answer={"pairs": [{"left_id": "left_circ", "right_id": "right_circ"}, {"left_id": "left_sq", "right_id": "right_sq"}, {"left_id": "left_tri", "right_id": "right_tri"}]},
            explanation={"en": "Great matching! Circle pairs with circle, square with square, triangle with triangle.", "ar": "مطابقة ممتازة! الدائرة مع الدائرة، والمربع مع المربع، والمثلث مع المثلث."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="math.shape.drag_sort",
            objective_key="obj.math.sort_objects_by_shape",
            subject_code="math",
            unit_code="unit.math.shapes_classification",
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={"en": "Sort objects into Circles and Squares.", "ar": "فرز الأشياء إلى دوائر ومربعات."},
            content_payload={
                "prompt": "Sort objects into Circles and Squares.",
                "items": [
                    {"id": "item_clock", "label": "Clock ⏰", "visual_cue": "⏰"},
                    {"id": "item_box", "label": "Gift Box 📦", "visual_cue": "📦"},
                    {"id": "item_wheel", "label": "Coin 🪙", "visual_cue": "🪙"},
                    {"id": "item_window", "label": "Window Pane 🪟", "visual_cue": "🪟"},
                ],
                "zones": [
                    {"id": "zone_circles", "label": "Round / Circles", "capacity": 3},
                    {"id": "zone_squares", "label": "Boxy / Squares", "capacity": 3},
                ],
                "correct_mapping": {
                    "item_clock": "zone_circles",
                    "item_box": "zone_squares",
                    "item_wheel": "zone_circles",
                    "item_window": "zone_squares",
                },
            },
            correct_answer={"correct_mapping": {"item_clock": "zone_circles", "item_box": "zone_squares", "item_wheel": "zone_circles", "item_window": "zone_squares"}},
            explanation={"en": "All objects sorted accurately into circles and squares!", "ar": "تم فرز جميع الأشياء بدقة إلى دوائر ومربعات!"},
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # LITERACY - UNIT 1: LETTER RECOGNITION
    # ══════════════════════════════════════════════════════════════════════════
    items.append(
        ContentItemDef(
            content_key="lit.letter.mc_upper_a",
            objective_key="obj.lit.identify_uppercase",
            subject_code="literacy",
            unit_code="unit.lit.letter_recognition",
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "Which letter is uppercase 'A'?", "ar": "أي حرف هو الحرف الكبير 'A'؟"},
            content_payload={
                "question": "Which letter is uppercase 'A'?",
                "options": [
                    {"id": "opt_a", "text": "A", "visual_cue": "A", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_b", "text": "B", "visual_cue": "B", "is_correct": False, "distractor_rationale": "Next letter"},
                    {"id": "opt_d", "text": "D", "visual_cue": "D", "is_correct": False, "distractor_rationale": "Different shape"},
                ],
                "correct_answer_id": "opt_a",
                "explanation": "Correct! That is uppercase letter A.",
            },
            correct_answer={"correct_answer_id": "opt_a"},
            explanation={"en": "Correct! That is uppercase letter A.", "ar": "صحيح! هذا هو الحرف الكبير A."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="lit.letter.match_upper_lower",
            objective_key="obj.lit.match_upper_to_lower",
            subject_code="literacy",
            unit_code="unit.lit.letter_recognition",
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={"en": "Match uppercase letters to their lowercase forms.", "ar": "طابق الحروف الكبيرة بالحروف الصغيرة المقابلة لها."},
            content_payload={
                "prompt": "Match uppercase letters to their lowercase forms.",
                "left_items": [
                    {"id": "upper_A", "label": "A", "visual_cue": "A"},
                    {"id": "upper_B", "label": "B", "visual_cue": "B"},
                    {"id": "upper_C", "label": "C", "visual_cue": "C"},
                ],
                "right_items": [
                    {"id": "lower_a", "label": "a", "visual_cue": "a"},
                    {"id": "lower_b", "label": "b", "visual_cue": "b"},
                    {"id": "lower_c", "label": "c", "visual_cue": "c"},
                ],
                "pairs": [
                    {"left_id": "upper_A", "right_id": "lower_a"},
                    {"left_id": "upper_B", "right_id": "lower_b"},
                    {"left_id": "upper_C", "right_id": "lower_c"},
                ],
            },
            correct_answer={"pairs": [{"left_id": "upper_A", "right_id": "lower_a"}, {"left_id": "upper_B", "right_id": "lower_b"}, {"left_id": "upper_C", "right_id": "lower_c"}]},
            explanation={"en": "Terrific! A↔a, B↔b, C↔c.", "ar": "رائع! A↔a، B↔b، C↔c."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="lit.letter.vis_find_s",
            objective_key="obj.lit.identify_letter_distractors",
            subject_code="literacy",
            unit_code="unit.lit.letter_recognition",
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={"en": "Find the letter 'S' among the letters.", "ar": "ابحث عن الحرف 'S' بين الحروف المعروضة."},
            content_payload={
                "prompt": "Find the letter 'S' among the letters.",
                "scene_description": "A reading banner showing letters M, S, and T.",
                "elements": [
                    {"id": "let_m", "label": "Letter M", "category": "letter", "is_target": False, "bounding_hint": "left"},
                    {"id": "let_s", "label": "Letter S", "category": "letter", "is_target": True, "bounding_hint": "center"},
                    {"id": "let_t", "label": "Letter T", "category": "letter", "is_target": False, "bounding_hint": "right"},
                ],
                "target_id": "let_s",
                "feedback_clue": "Look for the curvy snake-shaped letter in the center.",
            },
            correct_answer={"target_id": "let_s"},
            explanation={"en": "Well done! You found the curvy letter S.", "ar": "أحسنت! لقد وجدت الحرف S."},
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # LITERACY - UNIT 2: LETTER SOUNDS
    # ══════════════════════════════════════════════════════════════════════════
    items.append(
        ContentItemDef(
            content_key="lit.sound.initial_b",
            objective_key="obj.lit.initial_sound_word",
            subject_code="literacy",
            unit_code="unit.lit.letter_sounds",
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "What initial sound does 'Ball' start with?", "ar": "ما هو الصوت الأولي لكلمة 'Ball' (كرة)؟"},
            content_payload={
                "question": "What initial sound does 'Ball' start with?",
                "options": [
                    {"id": "snd_b", "text": "/b/ (Letter B)", "visual_cue": "⚽", "is_correct": True, "distractor_rationale": None},
                    {"id": "snd_s", "text": "/s/ (Letter S)", "visual_cue": "🐍", "is_correct": False, "distractor_rationale": "Different sound"},
                    {"id": "snd_m", "text": "/m/ (Letter M)", "visual_cue": "🌙", "is_correct": False, "distractor_rationale": "Different sound"},
                ],
                "correct_answer_id": "snd_b",
                "explanation": "'Ball' starts with the /b/ sound, spelled with the letter B.",
            },
            correct_answer={"correct_answer_id": "snd_b"},
            explanation={"en": "'Ball' starts with the /b/ sound, spelled with the letter B.", "ar": "كلمة 'Ball' تبدأ بصوت /b/ المكتوب بالحرف B."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="lit.sound.match_letters_sounds",
            objective_key="obj.lit.match_letter_initial_sound",
            subject_code="literacy",
            unit_code="unit.lit.letter_sounds",
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={"en": "Match each letter to the word that starts with its sound.", "ar": "طابق كل حرف بالكلمة التي تبدأ بصوته."},
            content_payload={
                "prompt": "Match each letter to the word that starts with its sound.",
                "left_items": [
                    {"id": "let_S", "label": "S", "visual_cue": "S"},
                    {"id": "let_C", "label": "C", "visual_cue": "C"},
                    {"id": "let_D", "label": "D", "visual_cue": "D"},
                ],
                "right_items": [
                    {"id": "word_sun", "label": "Sun ☀️", "visual_cue": "☀️"},
                    {"id": "word_cat", "label": "Cat 🐱", "visual_cue": "🐱"},
                    {"id": "word_dog", "label": "Dog 🐶", "visual_cue": "🐶"},
                ],
                "pairs": [
                    {"left_id": "let_S", "right_id": "word_sun"},
                    {"left_id": "let_C", "right_id": "word_cat"},
                    {"left_id": "let_D", "right_id": "word_dog"},
                ],
            },
            correct_answer={"pairs": [{"left_id": "let_S", "right_id": "word_sun"}, {"left_id": "let_C", "right_id": "word_cat"}, {"left_id": "let_D", "right_id": "word_dog"}]},
            explanation={"en": "Great phonics! S is for Sun, C is for Cat, D is for Dog.", "ar": "أصوات رائعة! S للشمس، C للقطة، D للكلب."},
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # LITERACY - UNIT 3: WORD RECOGNITION
    # ══════════════════════════════════════════════════════════════════════════
    items.append(
        ContentItemDef(
            content_key="lit.word.match_word_picture",
            objective_key="obj.lit.match_word_to_image",
            subject_code="literacy",
            unit_code="unit.lit.word_recognition",
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={"en": "Match each printed word to its picture.", "ar": "طابق كل كلمة مكتوبة بصورتها."},
            content_payload={
                "prompt": "Match each printed word to its picture.",
                "left_items": [
                    {"id": "w_cat", "label": "Cat", "visual_cue": "🐱"},
                    {"id": "w_sun", "label": "Sun", "visual_cue": "☀️"},
                    {"id": "w_tree", "label": "Tree", "visual_cue": "🌳"},
                ],
                "right_items": [
                    {"id": "p_cat", "label": "Picture: Friendly Cat", "visual_cue": "🐱"},
                    {"id": "p_sun", "label": "Picture: Bright Sun", "visual_cue": "☀️"},
                    {"id": "p_tree", "label": "Picture: Green Tree", "visual_cue": "🌳"},
                ],
                "pairs": [
                    {"left_id": "w_cat", "right_id": "p_cat"},
                    {"left_id": "w_sun", "right_id": "p_sun"},
                    {"left_id": "w_tree", "right_id": "p_tree"},
                ],
            },
            correct_answer={"pairs": [{"left_id": "w_cat", "right_id": "p_cat"}, {"left_id": "w_sun", "right_id": "p_sun"}, {"left_id": "w_tree", "right_id": "p_tree"}]},
            explanation={"en": "Excellent reading! All words are paired with their pictures.", "ar": "قراءة ممتازة! كل الكلمات متطابقة مع صورها."},
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # LITERACY - UNIT 4: SEQUENCING & COMPREHENSION
    # ══════════════════════════════════════════════════════════════════════════
    items.append(
        ContentItemDef(
            content_key="lit.seq.order_plant_flower",
            objective_key="obj.lit.order_three_events",
            subject_code="literacy",
            unit_code="unit.lit.sequencing_comprehension",
            difficulty_level=3,
            supported_modalities=[ActivityType.ORDERING],
            prompt={"en": "Put the story steps in order from start to finish.", "ar": "رتب خطوات القصة بالتسلسل من البداية للنهاية."},
            content_payload={
                "prompt": "Put the story steps in order from start to finish.",
                "items": [
                    {"id": "step_water", "label": "Water the soil 💧", "visual_cue": "💧"},
                    {"id": "step_seed", "label": "Plant the tiny seed 🌱", "visual_cue": "🌱"},
                    {"id": "step_flower", "label": "A beautiful flower blooms 🌸", "visual_cue": "🌸"},
                ],
                "correct_sequence": ["step_seed", "step_water", "step_flower"],
                "direction": "chronological",
            },
            correct_answer={"correct_sequence": ["step_seed", "step_water", "step_flower"]},
            explanation={"en": "First we plant the seed, then water it, and finally the flower blooms!", "ar": "أولاً نزرع البذرة، ثم نسقيها بالماء، وأخيراً تتفتح الزهرة!"},
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # EVERYDAY LEARNING - UNIT 1: DAILY ROUTINES
    # ══════════════════════════════════════════════════════════════════════════
    items.append(
        ContentItemDef(
            content_key="life.routine.order_morning",
            objective_key="obj.life.order_morning_routines",
            subject_code="everyday",
            unit_code="unit.life.daily_routines",
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={"en": "Put the morning routine steps in chronological order.", "ar": "رتب خطوات الروتين الصباحي بالترتيب الزمني الصحيح."},
            content_payload={
                "prompt": "Put the morning routine steps in chronological order.",
                "items": [
                    {"id": "m_breakfast", "label": "Eat healthy breakfast 🥣", "visual_cue": "🥣"},
                    {"id": "m_wake", "label": "Wake up in bed ⏰", "visual_cue": "⏰"},
                    {"id": "m_teeth", "label": "Brush teeth 🪥", "visual_cue": "🪥"},
                ],
                "correct_sequence": ["m_wake", "m_teeth", "m_breakfast"],
                "direction": "chronological",
            },
            correct_answer={"correct_sequence": ["m_wake", "m_teeth", "m_breakfast"]},
            explanation={"en": "Great sequence! Wake up, brush teeth, then eat breakfast.", "ar": "تسلسل رائع! الاستيقاظ، ثم غسل الأسنان، ثم تناول الإفطار."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="life.routine.drag_routine_stages",
            objective_key="obj.life.match_activity_to_stage",
            subject_code="everyday",
            unit_code="unit.life.daily_routines",
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={"en": "Sort activities into Morning and Bedtime.", "ar": "صنف الأنشطة إلى الصباح ووقت النوم."},
            content_payload={
                "prompt": "Sort activities into Morning and Bedtime.",
                "items": [
                    {"id": "act_sun", "label": "Open Curtains ☀️", "visual_cue": "☀️"},
                    {"id": "act_pajamas", "label": "Put on Pajamas 🛌", "visual_cue": "🛌"},
                    {"id": "act_backpack", "label": "Pack Backpack 🎒", "visual_cue": "🎒"},
                    {"id": "act_story", "label": "Read Bedtime Story 📖", "visual_cue": "📖"},
                ],
                "zones": [
                    {"id": "zone_morning", "label": "Morning Routine 🌅", "capacity": 3},
                    {"id": "zone_bedtime", "label": "Bedtime Routine 🌙", "capacity": 3},
                ],
                "correct_mapping": {
                    "act_sun": "zone_morning",
                    "act_backpack": "zone_morning",
                    "act_pajamas": "zone_bedtime",
                    "act_story": "zone_bedtime",
                },
            },
            correct_answer={"correct_mapping": {"act_sun": "zone_morning", "act_backpack": "zone_morning", "act_pajamas": "zone_bedtime", "act_story": "zone_bedtime"}},
            explanation={"en": "Well organized! Morning and bedtime activities are separated correctly.", "ar": "تنظيم رائع! تم فصل أنشطة الصباح والمساء بدقة."},
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # EVERYDAY LEARNING - UNIT 2: OBJECT RECOGNITION
    # ══════════════════════════════════════════════════════════════════════════
    items.append(
        ContentItemDef(
            content_key="life.obj.classroom_mc",
            objective_key="obj.life.identify_classroom_objects",
            subject_code="everyday",
            unit_code="unit.life.object_recognition",
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "Which item is used for writing or drawing?", "ar": "أي أداة تُستخدم للكتابة أو الرسم؟"},
            content_payload={
                "question": "Which item is used for writing or drawing?",
                "options": [
                    {"id": "opt_pencil", "text": "Pencil ✏️", "visual_cue": "✏️", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_chair", "text": "Chair 🪑", "visual_cue": "🪑", "is_correct": False, "distractor_rationale": "Used for sitting"},
                    {"id": "opt_cup", "text": "Cup 🥤", "visual_cue": "🥤", "is_correct": False, "distractor_rationale": "Used for drinking"},
                ],
                "correct_answer_id": "opt_pencil",
                "explanation": "A pencil is the tool we use for writing and drawing.",
            },
            correct_answer={"correct_answer_id": "opt_pencil"},
            explanation={"en": "A pencil is the tool we use for writing and drawing.", "ar": "القلم هو الأداة التي نستخدمها للكتابة والرسم."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="life.obj.vis_find_backpack",
            objective_key="obj.life.identify_classroom_objects",
            subject_code="everyday",
            unit_code="unit.life.object_recognition",
            difficulty_level=1,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={"en": "Find the student's backpack in the classroom.", "ar": "ابحث عن حقيبة المدرسة في الفصل."},
            content_payload={
                "prompt": "Find the student's backpack in the classroom.",
                "scene_description": "A quiet classroom cubby area with a desk, backpack, and coat hook.",
                "elements": [
                    {"id": "el_desk", "label": "Wooden Desk", "category": "furniture", "is_target": False, "bounding_hint": "left"},
                    {"id": "el_pack", "label": "Blue Backpack 🎒", "category": "bag", "is_target": True, "bounding_hint": "center"},
                    {"id": "el_clock", "label": "Wall Clock", "category": "fixture", "is_target": False, "bounding_hint": "right"},
                ],
                "target_id": "el_pack",
                "feedback_clue": "Look in the center for the blue backpack with zipper straps.",
            },
            correct_answer={"target_id": "el_pack"},
            explanation={"en": "Great observation! You located the backpack.", "ar": "ملاحظة رائعة! لقد حددت موقع الحقيبة."},
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # EVERYDAY LEARNING - UNIT 3: SORTING & CLASSIFICATION
    # ══════════════════════════════════════════════════════════════════════════
    items.append(
        ContentItemDef(
            content_key="life.sort.type_food_clothes",
            objective_key="obj.life.sort_by_type",
            subject_code="everyday",
            unit_code="unit.life.sorting_classification",
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={"en": "Sort items into 'Food' and 'Clothes'.", "ar": "صنف العناصر إلى 'طعام' و 'ملابس'."},
            content_payload={
                "prompt": "Sort items into 'Food' and 'Clothes'.",
                "items": [
                    {"id": "item_apple", "label": "Apple 🍎", "visual_cue": "🍎"},
                    {"id": "item_shirt", "label": "T-Shirt 👕", "visual_cue": "👕"},
                    {"id": "item_banana", "label": "Banana 🍌", "visual_cue": "🍌"},
                    {"id": "item_socks", "label": "Socks 🧦", "visual_cue": "🧦"},
                ],
                "zones": [
                    {"id": "zone_food", "label": "Food 🍎", "capacity": 3},
                    {"id": "zone_clothes", "label": "Clothing 👕", "capacity": 3},
                ],
                "correct_mapping": {
                    "item_apple": "zone_food",
                    "item_banana": "zone_food",
                    "item_shirt": "zone_clothes",
                    "item_socks": "zone_clothes",
                },
            },
            correct_answer={"correct_mapping": {"item_apple": "zone_food", "item_banana": "zone_food", "item_shirt": "zone_clothes", "item_socks": "zone_clothes"}},
            explanation={"en": "Apples and bananas are food. Shirts and socks are clothing!", "ar": "التفاح والموز من الأطعمة، والقميص والجوارب من الملابس!"},
        )
    )
    items.append(
        ContentItemDef(
            content_key="life.sort.belong_pairs",
            objective_key="obj.life.match_objects_belong_together",
            subject_code="everyday",
            unit_code="unit.life.sorting_classification",
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={"en": "Match the objects that belong together.", "ar": "طابق الأدوات التي تُستخدم معاً."},
            content_payload={
                "prompt": "Match the objects that belong together.",
                "left_items": [
                    {"id": "tool_brush", "label": "Toothbrush 🪥", "visual_cue": "🪥"},
                    {"id": "tool_lock", "label": "Key 🔑", "visual_cue": "🔑"},
                    {"id": "tool_shoe", "label": "Shoe 👟", "visual_cue": "👟"},
                ],
                "right_items": [
                    {"id": "match_paste", "label": "Toothpaste", "visual_cue": "🧴"},
                    {"id": "match_lock", "label": "Lock 🔒", "visual_cue": "🔒"},
                    {"id": "match_sock", "label": "Sock 🧦", "visual_cue": "🧦"},
                ],
                "pairs": [
                    {"left_id": "tool_brush", "right_id": "match_paste"},
                    {"left_id": "tool_lock", "right_id": "match_lock"},
                    {"left_id": "tool_shoe", "right_id": "match_sock"},
                ],
            },
            correct_answer={"pairs": [{"left_id": "tool_brush", "right_id": "match_paste"}, {"left_id": "tool_lock", "right_id": "match_lock"}, {"left_id": "tool_shoe", "right_id": "match_sock"}]},
            explanation={"en": "Toothbrush goes with toothpaste, key with lock, shoe with sock!", "ar": "فرشاة الأسنان مع المعجون، والمفتاح مع القفل، والحذاء مع الجورب!"},
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # EVERYDAY LEARNING - UNIT 4: EVERYDAY DECISIONS & BASIC SAFETY
    # ══════════════════════════════════════════════════════════════════════════
    items.append(
        ContentItemDef(
            content_key="life.safe.cross_street",
            objective_key="obj.life.before_crossing_road",
            subject_code="everyday",
            unit_code="unit.life.everyday_safety",
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={"en": "What is the safe rule before crossing the street?", "ar": "ما هي القاعدة الآمنة قبل عبور الشارع؟"},
            content_payload={
                "question": "What is the safe rule before crossing the street?",
                "options": [
                    {"id": "opt_run", "text": "Run across as fast as possible", "visual_cue": "🏃", "is_correct": False, "distractor_rationale": "Unsafe practice"},
                    {"id": "opt_stop", "text": "Stop, look both ways, and hold an adult's hand", "visual_cue": "🛑", "is_correct": True, "distractor_rationale": None},
                    {"id": "opt_close", "text": "Close your eyes", "visual_cue": "🙈", "is_correct": False, "distractor_rationale": "Dangerous action"},
                ],
                "correct_answer_id": "opt_stop",
                "explanation": "Always stop at the curb, look both ways, and stay with an adult.",
            },
            correct_answer={"correct_answer_id": "opt_stop"},
            explanation={"en": "Always stop at the curb, look both ways, and stay with an adult.", "ar": "توقف دائماً عند حافة الرصيف، وانظر في الاتجاهين، وابق مع شخص بالغ."},
        )
    )
    items.append(
        ContentItemDef(
            content_key="life.safe.order_handwash",
            objective_key="obj.life.sequence_safe_routine",
            subject_code="everyday",
            unit_code="unit.life.everyday_safety",
            difficulty_level=3,
            supported_modalities=[ActivityType.ORDERING],
            prompt={"en": "Put the steps of washing hands in order.", "ar": "رتب خطوات غسل اليدين بالتسلسل الصحيح."},
            content_payload={
                "prompt": "Put the steps of washing hands in order.",
                "items": [
                    {"id": "hw_rinse", "label": "Rinse with clean water 🚿", "visual_cue": "🚿"},
                    {"id": "hw_soap", "label": "Apply soap and lather 🧼", "visual_cue": "🧼"},
                    {"id": "hw_wet", "label": "Wet hands with water 💧", "visual_cue": "💧"},
                    {"id": "hw_dry", "label": "Dry hands with clean towel 🧻", "visual_cue": "🧻"},
                ],
                "correct_sequence": ["hw_wet", "hw_soap", "hw_rinse", "hw_dry"],
                "direction": "chronological",
            },
            correct_answer={"correct_sequence": ["hw_wet", "hw_soap", "hw_rinse", "hw_dry"]},
            explanation={"en": "Perfect handwashing routine: Wet hands, add soap, rinse clean, and dry!", "ar": "روتين مثالي لغسل اليدين: بلل اليدين، ضع الصابون، اشطف بالماء، ثم جفف!"},
        )
    )
    items.append(
        ContentItemDef(
            content_key="life.safe.drag_safe_unsafe",
            objective_key="obj.life.distinguish_safe_vs_unsafe",
            subject_code="everyday",
            unit_code="unit.life.everyday_safety",
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={"en": "Sort the actions into 'Safe Choice' and 'Unsafe Choice'.", "ar": "صنف التصرفات إلى 'خيار آمن' و 'خيار غير آمن'."},
            content_payload={
                "prompt": "Sort the actions into 'Safe Choice' and 'Unsafe Choice'.",
                "items": [
                    {"id": "act_walk_stairs", "label": "Walking down stairs holding handrail 🚶", "visual_cue": "🚶"},
                    {"id": "act_touch_stove", "label": "Touching hot stove burner ⚠️", "visual_cue": "⚠️"},
                    {"id": "act_helmet", "label": "Wearing helmet while cycling 🚴", "visual_cue": "🚴"},
                    {"id": "act_run_scissors", "label": "Running with sharp scissors ❌", "visual_cue": "❌"},
                ],
                "zones": [
                    {"id": "zone_safe", "label": "Safe Choice ✅", "capacity": 3},
                    {"id": "zone_unsafe", "label": "Unsafe Choice ⚠️", "capacity": 3},
                ],
                "correct_mapping": {
                    "act_walk_stairs": "zone_safe",
                    "act_helmet": "zone_safe",
                    "act_touch_stove": "zone_unsafe",
                    "act_run_scissors": "zone_unsafe",
                },
            },
            correct_answer={"correct_mapping": {"act_walk_stairs": "zone_safe", "act_helmet": "zone_safe", "act_touch_stove": "zone_unsafe", "act_run_scissors": "zone_unsafe"}},
            explanation={"en": "Great safety awareness! Handrails and helmets keep us safe.", "ar": "وعي ممتاز بالسلامة! التمسك بالدرابزين وارتداء الخوذة يحمياننا."},
        )
    )

    from app.content.items_math import get_expanded_math_items
    from app.content.items_literacy import get_expanded_literacy_items
    from app.content.items_everyday import get_expanded_everyday_items

    items.extend(get_expanded_math_items())
    items.extend(get_expanded_literacy_items())
    items.extend(get_expanded_everyday_items())

    return items


ALL_CONTENT_ITEMS: list[ContentItemDef] = get_all_content_definitions()
