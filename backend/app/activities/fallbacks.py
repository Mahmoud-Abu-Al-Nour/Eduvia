"""
Eduvia — Deterministic Fallback Activity & Lesson Generator (Phase 4 & Phase 8)

Provides deterministic, schema-compliant fallback activities and structured mini-lessons
when LLM generation is unavailable, times out, or fails schema validation.

Guarantees that a learner is NEVER blocked from instructional engagement due to
an AI provider outage or malformed JSON (Zero-Strand Guarantee).
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
    LessonPlan,
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
    item_count: int = 4,
    seed: int = 0,
) -> Activity:
    """
    Generate a robust, deterministic activity guaranteed to validate against Pydantic schemas.
    Leverages the authoritative ContentBank for real, curriculum-aligned educational content.
    Supports item_count and seed for variation across regenerations.
    """
    if not isinstance(activity_type, ActivityType):
        try:
            activity_type = ActivityType(activity_type)
        except (ValueError, KeyError):
            activity_type = ActivityType.MULTIPLE_CHOICE

    from app.content.bank import get_content_bank
    bank = get_content_bank()

    # Retrieve all matches and select using seed for variation
    matching_items = bank.get_all_by_objective(objective_id, activity_type=activity_type)
    if matching_items:
        selected_item = matching_items[seed % len(matching_items)]
        activity = bank.create_activity_from_content(
            selected_item,
            target_modality=activity_type,
            language=language,
            objective_id=objective_id,
            difficulty_level=difficulty_level,
        )
    else:
        # Fall back to any objective item or dynamic synthesis
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
    activity.metadata["seed"] = seed
    activity.metadata["source"] = "deterministic_fallback"
    return activity


def create_fallback_lesson(
    objective_id: uuid.UUID,
    objective_title: str = "Foundational Practice",
    objective_description: str | None = None,
    difficulty_level: int = 1,
    language: str = "en",
    suggested_activity_type: ActivityType = ActivityType.MULTIPLE_CHOICE,
    seed: int = 0,
) -> LessonPlan:
    """
    Generate a structured, curriculum-aligned 10-minute mini-lesson plan deterministically.
    Adheres strictly to the Gradual Release of Responsibility (I Do, We Do, You Do) framework.
    """
    embedded_act = create_fallback_activity(
        objective_id=objective_id,
        objective_title=objective_title,
        objective_description=objective_description,
        difficulty_level=difficulty_level,
        activity_type=suggested_activity_type,
        language=language,
        seed=seed,
    )

    is_arabic = (language or "").lower().startswith("ar")

    if is_arabic:
        title = f"درس مصغر: {objective_title}"
        intro = f"التمهيد (دقيقتان): نربط مهارة '{objective_title}' بأمثلة مألوفة من الحياة اليومية لجذب انتباه الطالب."
        demo = f"النمذجة 'أنا أعمل' (3 دقائق): يشرح المعلم المفهوم الأساسي خطوة بخطوة باستخدام وسائل بصرية واضحة."
        guided = f"الممارسة الموجهة 'نحن نعمل' (3 دقائق): نشاط تفاعلي تعاوني مع تقديم تلميحات تشجيعية وتصحيح هادئ."
        independent = f"الممارسة المستقلة 'أنت تعمل' (دقيقتان): يكمل الطالب النشاط التفاعلي المرفق لتعزيز الاستيعاب."
        scaffolding = "الدعم المتدرج: توفير تلميحات بصرية، استخدام عبارات تشجيعية، ومنح وقت كافٍ للاستجابة."
        notes = "ملاحظات المعلم: مراقبة دقة الإجابة وتقديم التغذية الراجعة الفورية بدون تشتيت."
        recap = f"الخلاصة: تلخيص سريع ومحفز لما تم إنجازه اليوم حول '{objective_title}'."
    else:
        title = f"Guided Mini-Lesson: {objective_title}"
        intro = f"Warm-up (2 min): Connect '{objective_title}' with everyday real-world examples to activate prior knowledge."
        demo = f"Modeling / 'I Do' (3 min): Explicitly demonstrate the core concept step-by-step using clear, calming visual cues."
        guided = f"Guided Practice / 'We Do' (3 min): Collaborative interactive check with positive, scaffolded prompts."
        independent = f"Independent Application / 'You Do' (2 min): Learner engages with the embedded interactive practice task."
        scaffolding = "Tiered Scaffolding: Provide gentle visual prompts, allow adequate processing time, and avoid high-stakes framing."
        notes = "Teacher Observations: Watch for common approximations and validate foundational reasoning."
        recap = f"Closure & Recap: Quick celebratory check consolidating mastery of '{objective_title}'."

    return LessonPlan(
        id=uuid.uuid4(),
        objective_id=objective_id,
        title=title,
        objective=objective_title,
        duration_minutes=10,
        introduction=intro,
        demonstration=demo,
        guided_practice=guided,
        independent_practice=independent,
        scaffolding=scaffolding,
        teacher_notes=notes,
        recap=recap,
        suggested_activity_type=suggested_activity_type,
        activity=embedded_act,
        generation_source="deterministic_fallback",
        fallback_used=True,
        grounding_sources=[],
    )
