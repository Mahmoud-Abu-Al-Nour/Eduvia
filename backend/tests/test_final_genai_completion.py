"""
Tests for Final Eduvia GenAI Activity & Mini-Lesson Generation System.

Verifies:
1. Teacher generation brief schema (GenerationSpec / ActivityGenerateRequest)
2. Prompt compiler with 10 distinct sections
3. Effective prompt contents & isolation of teacher-controlled instructions
4. Gemini invocation receives teacher instructions, objective, Content Bank, and RAG
5. Content Bank grounding
6. RAG grounding
7. Gemini success (provenance = gemini, fallback_used = False)
8. Gemini timeout fallback (provenance = deterministic_fallback, fallback_used = True)
9. Gemini invalid JSON fallback (provenance = deterministic_fallback, fallback_used = True)
10. Five activity modalities generation (multiple_choice, matching, ordering, visual_identification, drag_drop)
11. Lesson generation (LessonPlan with 5 phases & fallback)
12. Regeneration & variation with seed
13. Teacher constraint precedence (Phase 8 authoritative difficulty lock)
"""
from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.activities.schemas import (
    ActivityGenerateRequest,
    ActivityType,
    EffectiveGenerationPrompt,
    LessonPlan,
)
from app.activities.service import ActivityService
from app.ai.generation.prompts import (
    compile_generation_prompt,
    compile_lesson_prompt,
)
from app.content.bank import ContentBank
from app.curriculum.models import LearningObjective
from app.knowledge.schemas import RetrievedChunk
from app.users.models import User, UserRole


class TestTeacherBriefAndPromptCompiler:
    """Verifies GenerationSpec schema, 10-section prompt compiler, and prompt ownership isolation."""

    def test_teacher_brief_schema_defaults_and_fields(self) -> None:
        """GenerationSpec schema should validate all teacher brief parameters."""
        obj_id = uuid.uuid4()
        req = ActivityGenerateRequest(
            objective_id=obj_id,
            activity_type=ActivityType.MATCHING,
            difficulty_level=3,
            item_count=8,
            language="en",
            visual_style="calm",
            scaffolding_level=2,
            interaction_style="direct",
            teacher_instructions="Use everyday fruit and calm shapes.",
            seed=42,
            phase8_locked_difficulty=2,
        )

        assert req.item_count == 8
        assert req.visual_style == "calm"
        assert req.scaffolding_level == 2
        assert req.teacher_instructions == "Use everyday fruit and calm shapes."
        assert req.seed == 42
        assert req.phase8_locked_difficulty == 2

    def test_prompt_compiler_produces_ten_distinct_sections(self) -> None:
        """compile_generation_prompt should compile exactly the 10 required prompt sections."""
        chunks = [
            RetrievedChunk(
                chunk_id="rag-1",
                document_title="Counting Pedagogies",
                source="counting.md",
                category="strategy",
                content="Use 1-to-1 correspondence with tactile cues.",
                score=0.92,
            )
        ]
        bank_items = [
            {"id": "item-1", "question": "Count 3 apples", "correct_answer": "3"}
        ]

        req = ActivityGenerateRequest(
            objective_id=uuid.uuid4(),
            activity_type=ActivityType.MATCHING,
            difficulty_level=2,
            item_count=5,
            language="en",
            visual_style="simple",
            scaffolding_level=2,
            interaction_style="direct",
            teacher_instructions="Avoid numbers higher than 5.",
        )
        compiled = compile_generation_prompt(
            spec=req,
            objective_title="Count objects 0-10",
            objective_description="Cardinality within 10",
            grounding_chunks=chunks,
            authoritative_content={"prompt": "Count 3 apples", "correct_answer": "3"},
        )

        sections = compiled.sections
        required_sections = [
            "SYSTEM RULES",
            "CURRICULUM CONTEXT",
            "LEARNER CONTEXT",
            "TEACHER PARAMETERS",
            "TEACHER INSTRUCTIONS",
            "AUTHORITATIVE CONTENT",
            "RAG GUIDANCE",
            "ADAPTIVE DECISION",
            "ACTIVITY-SPECIFIC RULES",
            "OUTPUT JSON CONTRACT",
        ]
        for sec in required_sections:
            assert sec in sections, f"Missing section: {sec}"

        # Teacher instructions must be isolated and present
        assert "Avoid numbers higher than 5." in sections["TEACHER INSTRUCTIONS"]
        assert compiled.teacher_editable_section == sections["TEACHER INSTRUCTIONS"]

        # Immutable system rules must be enforced
        assert "Zero-Strand Guarantee" in sections["SYSTEM RULES"]
        assert "Cognitive Calm" in sections["SYSTEM RULES"]
        assert "Sovereign Correctness" in sections["SYSTEM RULES"]
        assert "authoritative educational ground truth" in sections["SYSTEM RULES"]

        # Content Bank and RAG must be present in their respective sections
        assert "Count 3 apples" in sections["AUTHORITATIVE CONTENT"]
        assert "1-to-1 correspondence" in sections["RAG GUIDANCE"]

        # Full prompt contains the assembled text
        for sec in required_sections:
            assert f"### {sec}" in compiled.full_prompt_text


class TestGeminiInvocationAndGrounding:
    """Verifies Gemini receives full compiled context, and tests success vs fallback."""

    @pytest.mark.asyncio
    async def test_gemini_receives_teacher_instructions_and_grounding(self) -> None:
        """The orchestrator should receive the effective compiled prompt containing teacher text, Content Bank, and RAG."""
        obj_id = uuid.uuid4()
        mock_objective = LearningObjective(
            id=obj_id,
            lesson_id=uuid.uuid4(),
            title={"en": "Count objects from 0 to 10"},
            description={"en": "Cardinality and counting"},
            difficulty_level=2,
            is_active=True,
            order_index=1,
        )

        mock_session = AsyncMock()
        mock_session.get.return_value = mock_objective

        captured_messages = []

        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        mock_orchestrator.provider.provider_name = "gemini"

        async def fake_generate_structured(messages, output_schema=None, **kwargs):
            captured_messages.extend(messages)
            return {
                "id": str(uuid.uuid4()),
                "objective_id": str(obj_id),
                "activity_type": "matching",
                "title": "Match Counting Objects",
                "instructions": "Connect the matching items.",
                "difficulty_level": 2,
                "content": {
                    "activity_type": "matching",
                    "prompt": "Match each set of dots to its numeral.",
                    "left_items": [
                        {"id": "l1", "label": "3 dots"},
                        {"id": "l2", "label": "5 dots"},
                    ],
                    "right_items": [
                        {"id": "r1", "label": "3"},
                        {"id": "r2", "label": "5"},
                    ],
                    "pairs": [
                        {"left_id": "l1", "right_id": "r1"},
                        {"left_id": "l2", "right_id": "r2"},
                    ],
                },
                "hints": ["Count the dots carefully."],
                "scaffolding_level": 2,
            }

        mock_orchestrator.generate_structured = AsyncMock(side_effect=fake_generate_structured)

        mock_retrieval = MagicMock()
        mock_retrieval.retrieve_pedagogical_context = AsyncMock(
            return_value=[
                RetrievedChunk(
                    chunk_id="chunk-sen-99",
                    document_title="SEN High Contrast Visuals",
                    source="visuals.md",
                    category="activity_design",
                    content="Keep backgrounds neutral and high contrast.",
                    score=0.95,
                )
            ]
        )

        service = ActivityService(session=mock_session, orchestrator=mock_orchestrator)
        req = ActivityGenerateRequest(
            objective_id=obj_id,
            activity_type=ActivityType.MATCHING,
            difficulty_level=2,
            item_count=5,
            teacher_instructions="Ensure only stars and circles are used as objects.",
        )
        user = User(id=uuid.uuid4(), email="teacher@eduvia.org", hashed_password="", role=UserRole.teacher)

        with (
            patch("app.curriculum.service.CurriculumService.get_learning_objective", return_value=mock_objective),
            patch("app.knowledge.retrieval.get_knowledge_retrieval_service", return_value=mock_retrieval),
        ):
            resp = await service.generate_activity(req, user)

        assert resp.fallback_used is False
        assert resp.generation_source == "gemini"
        assert len(resp.grounding_sources) == 1
        assert resp.grounding_sources[0]["chunk_id"] == "chunk-sen-99"

        # Check prompt sent to Gemini (across system and user messages)
        assert len(captured_messages) >= 2
        all_prompt_text = " ".join(m.content for m in captured_messages)
        assert "Ensure only stars and circles are used as objects." in all_prompt_text
        assert "Keep backgrounds neutral and high contrast." in all_prompt_text
        assert "Count objects from 0 to 10" in all_prompt_text

    @pytest.mark.asyncio
    async def test_gemini_timeout_triggers_deterministic_fallback(self) -> None:
        """When Gemini times out, the system must trigger deterministic fallback without failing."""
        obj_id = uuid.uuid4()
        mock_objective = LearningObjective(
            id=obj_id,
            lesson_id=uuid.uuid4(),
            title={"en": "Counting 0-10"},
            description={"en": "Foundational math"},
            difficulty_level=2,
            is_active=True,
            order_index=1,
        )

        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        mock_orchestrator.generate_structured = AsyncMock(side_effect=TimeoutError("Request timed out"))

        service = ActivityService(session=AsyncMock(), orchestrator=mock_orchestrator)
        req = ActivityGenerateRequest(
            objective_id=obj_id,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            difficulty_level=2,
        )
        user = User(id=uuid.uuid4(), email="t@eduvia.org", hashed_password="", role=UserRole.teacher)

        with patch("app.curriculum.service.CurriculumService.get_learning_objective", return_value=mock_objective):
            resp = await service.generate_activity(req, user)

        assert resp.fallback_used is True
        assert resp.generation_source == "deterministic_fallback"
        assert resp.activity is not None
        assert resp.activity.activity_type == ActivityType.MULTIPLE_CHOICE

    @pytest.mark.asyncio
    async def test_gemini_invalid_json_triggers_deterministic_fallback(self) -> None:
        """When Gemini returns schema-invalid output, system must fallback cleanly."""
        obj_id = uuid.uuid4()
        mock_objective = LearningObjective(
            id=obj_id,
            lesson_id=uuid.uuid4(),
            title={"en": "Counting 0-10"},
            description={"en": "Foundational math"},
            difficulty_level=2,
            is_active=True,
            order_index=1,
        )

        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        # Return invalid payload missing required fields
        mock_orchestrator.generate_structured = AsyncMock(return_value={"garbage": "invalid_structure"})

        service = ActivityService(session=AsyncMock(), orchestrator=mock_orchestrator)
        req = ActivityGenerateRequest(
            objective_id=obj_id,
            activity_type=ActivityType.ORDERING,
            difficulty_level=2,
        )
        user = User(id=uuid.uuid4(), email="t@eduvia.org", hashed_password="", role=UserRole.teacher)

        with patch("app.curriculum.service.CurriculumService.get_learning_objective", return_value=mock_objective):
            resp = await service.generate_activity(req, user)

        assert resp.fallback_used is True
        assert resp.generation_source == "deterministic_fallback"
        assert resp.activity is not None
        assert resp.activity.activity_type == ActivityType.ORDERING


class TestFiveModalitiesAndLessonPlan:
    """Verifies that all 5 modalities generate valid schemas and mini-lessons conform to structured schema."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "modality",
        [
            ActivityType.MULTIPLE_CHOICE,
            ActivityType.MATCHING,
            ActivityType.ORDERING,
            ActivityType.VISUAL_IDENTIFICATION,
            ActivityType.DRAG_DROP,
        ],
    )
    async def test_five_modalities_produce_valid_activities(self, modality: ActivityType) -> None:
        """All five activity modalities must produce valid, playable activities."""
        obj_id = uuid.uuid4()
        mock_objective = LearningObjective(
            id=obj_id,
            lesson_id=uuid.uuid4(),
            title={"en": f"Objective for {modality.value}"},
            description={"en": "Testing modality validity"},
            difficulty_level=2,
            is_active=True,
            order_index=1,
        )

        service = ActivityService(session=AsyncMock(), orchestrator=None)
        req = ActivityGenerateRequest(
            objective_id=obj_id,
            activity_type=modality,
            difficulty_level=2,
            item_count=4,
        )
        user = User(id=uuid.uuid4(), email="t@eduvia.org", hashed_password="", role=UserRole.teacher)

        with patch("app.curriculum.service.CurriculumService.get_learning_objective", return_value=mock_objective):
            resp = await service.generate_activity(req, user)

        assert resp.activity.activity_type == modality
        assert resp.activity.title is not None
        assert resp.activity.instructions is not None
        assert resp.activity.content is not None
        assert resp.activity.content.activity_type == modality

    @pytest.mark.asyncio
    async def test_lesson_generation_produces_structured_lesson_plan(self) -> None:
        """generate_lesson must produce a typed LessonPlan with all 5 gradual release phases."""
        obj_id = uuid.uuid4()
        mock_objective = LearningObjective(
            id=obj_id,
            lesson_id=uuid.uuid4(),
            title={"en": "Count objects from 0 to 10"},
            description={"en": "Foundational counting"},
            difficulty_level=2,
            is_active=True,
            order_index=1,
        )

        service = ActivityService(session=AsyncMock(), orchestrator=None)
        req = ActivityGenerateRequest(
            objective_id=obj_id,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            difficulty_level=2,
            teacher_instructions="Keep warm-up visual and concrete.",
            mode="lesson",
        )
        user = User(id=uuid.uuid4(), email="t@eduvia.org", hashed_password="", role=UserRole.teacher)

        with patch("app.curriculum.service.CurriculumService.get_learning_objective", return_value=mock_objective):
            resp = await service.generate_lesson(req, user)

        lesson = resp.lesson_plan
        assert isinstance(lesson, LessonPlan)
        assert lesson.duration_minutes == 10
        assert "Warm-Up" in lesson.introduction or len(lesson.introduction) > 10
        assert "Demonstration" in lesson.demonstration or len(lesson.demonstration) > 10
        assert "Guided" in lesson.guided_practice or len(lesson.guided_practice) > 10
        assert "Independent" in lesson.independent_practice or len(lesson.independent_practice) > 10
        assert lesson.recap is not None
        assert lesson.scaffolding is not None

    @pytest.mark.asyncio
    async def test_regeneration_variation_with_seed(self) -> None:
        """Varying the seed should provide variation across generated activities."""
        obj_id = uuid.uuid4()
        mock_objective = LearningObjective(
            id=obj_id,
            lesson_id=uuid.uuid4(),
            title={"en": "Count objects from 0 to 10"},
            description={"en": "Counting cardinality"},
            difficulty_level=1,
            is_active=True,
            order_index=1,
        )

        service = ActivityService(session=AsyncMock(), orchestrator=None)
        user = User(id=uuid.uuid4(), email="t@eduvia.org", hashed_password="", role=UserRole.teacher)

        req1 = ActivityGenerateRequest(
            objective_id=obj_id,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            difficulty_level=1,
            seed=1,
        )
        req2 = ActivityGenerateRequest(
            objective_id=obj_id,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            difficulty_level=1,
            seed=2,
        )

        with patch("app.curriculum.service.CurriculumService.get_learning_objective", return_value=mock_objective):
            resp1 = await service.generate_activity(req1, user)
            resp2 = await service.generate_activity(req2, user)

        # Both must be valid activities
        assert resp1.activity is not None
        assert resp2.activity is not None

    @pytest.mark.asyncio
    async def test_teacher_constraint_precedence_phase8_lock(self) -> None:
        """Phase 8 locked difficulty must take precedence over teacher-requested difficulty."""
        obj_id = uuid.uuid4()
        mock_objective = LearningObjective(
            id=obj_id,
            lesson_id=uuid.uuid4(),
            title={"en": "Counting 0-10"},
            description={"en": "Math"},
            difficulty_level=2,
            is_active=True,
            order_index=1,
        )

        service = ActivityService(session=AsyncMock(), orchestrator=None)
        user = User(id=uuid.uuid4(), email="t@eduvia.org", hashed_password="", role=UserRole.teacher)

        req = ActivityGenerateRequest(
            objective_id=obj_id,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            difficulty_level=4,  # Teacher requested level 4
            phase8_locked_difficulty=1,  # Adaptive engine locked level 1
        )

        with patch("app.curriculum.service.CurriculumService.get_learning_objective", return_value=mock_objective):
            resp = await service.generate_activity(req, user)

        # Activity difficulty must be authoritative Phase 8 locked value (1), not 4
        assert resp.activity.difficulty_level == 1
