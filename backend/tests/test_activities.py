"""
Eduvia — Activity Generation Engine Tests (Phase 4)

Covers:
- Unit tests: Schema validation across all 5 activity modalities
- Unit tests: Deterministic fallback activity generator
- Unit tests: System prompt & context builder
- Service tests: ActivityService with mock AIOrchestrator (happy path, fallback path, constraints)
- API tests: GET /api/v1/activities/types and POST /api/v1/activities/generate
"""
import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.activities.fallbacks import create_fallback_activity
from app.activities.schemas import (
    Activity,
    ActivityGenerateRequest,
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
from app.activities.service import ActivityService
from app.ai.generation.prompts import build_activity_generation_messages
from app.ai.providers.base import LLMProvider, MessageRole
from app.auth.security import create_access_token, get_password_hash
from app.core.errors import AIProviderError, NotFoundError
from app.core.errors import ValidationError as EduviaValidationError
from app.curriculum.models import LearningObjective
from app.database.session import get_db_session
from app.learners.models import Learner, LearnerProfile
from app.main import app
from app.users.models import User, UserRole

client = TestClient(app)

now = datetime.now(UTC)
teacher_id = uuid.uuid4()
mock_teacher = User(
    id=teacher_id,
    email="teacher_act@eduvia.app",
    full_name="Teacher Activity",
    hashed_password=get_password_hash("password123"),
    role=UserRole.teacher,
    is_active=True,
    created_at=now,
    updated_at=now,
)

mock_objective_id = uuid.uuid4()
mock_objective = LearningObjective(
    id=mock_objective_id,
    lesson_id=uuid.uuid4(),
    title={"en": "Counting 1 to 5 with Visual Cues"},
    description={"en": "Learner counts objects up to 5 using concrete visual representations."},
    difficulty_level=2,
    assessment_criteria={"minimum_accuracy": 0.8, "maximum_assistance_level": 1},
    order_index=1,
    is_active=True,
)


@pytest.fixture(autouse=True)
def override_db():
    async def override_get_db_session():
        yield AsyncMock()

    app.dependency_overrides[get_db_session] = override_get_db_session
    yield
    app.dependency_overrides.pop(get_db_session, None)


# ── 1. Schema Validation Tests ────────────────────────────────────────────────


class TestActivitySchemas:
    """Validate Pydantic models for all 5 activity modalities."""

    def test_multiple_choice_schema_valid(self) -> None:
        content = MultipleChoiceContent(
            activity_type=ActivityType.MULTIPLE_CHOICE,
            question="Which group has 3 apples?",
            options=[
                MultipleChoiceOption(id="opt_1", text="3 apples", is_correct=True),
                MultipleChoiceOption(id="opt_2", text="2 apples", is_correct=False),
                MultipleChoiceOption(id="opt_3", text="5 apples", is_correct=False),
            ],
            correct_answer_id="opt_1",
            explanation="Well done! That group has exactly 3 apples.",
        )
        activity = Activity(
            objective_id=mock_objective_id,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            title="Counting Apples",
            instructions="Select the group that has 3 apples.",
            difficulty_level=1,
            content=content,
            hints=["Count each apple slowly."],
        )
        assert activity.activity_type == ActivityType.MULTIPLE_CHOICE
        assert activity.content.correct_answer_id == "opt_1"
        assert len(activity.content.options) == 3

    def test_multiple_choice_schema_rejects_insufficient_options(self) -> None:
        with pytest.raises(ValidationError):
            MultipleChoiceContent(
                activity_type=ActivityType.MULTIPLE_CHOICE,
                question="Only one option?",
                options=[
                    MultipleChoiceOption(id="opt_1", text="Only option", is_correct=True),
                ],
                correct_answer_id="opt_1",
                explanation="None",
            )

    def test_matching_schema_valid(self) -> None:
        content = MatchingContent(
            activity_type=ActivityType.MATCHING,
            prompt="Match the number to the word.",
            left_items=[
                MatchingItem(id="l1", label="1"),
                MatchingItem(id="l2", label="2"),
            ],
            right_items=[
                MatchingItem(id="r1", label="One"),
                MatchingItem(id="r2", label="Two"),
            ],
            pairs=[
                MatchingPair(left_id="l1", right_id="r1"),
                MatchingPair(left_id="l2", right_id="r2"),
            ],
        )
        activity = Activity(
            objective_id=mock_objective_id,
            activity_type=ActivityType.MATCHING,
            title="Match Numbers and Words",
            instructions="Draw lines connecting the matching pairs.",
            difficulty_level=1,
            content=content,
        )
        assert activity.activity_type == ActivityType.MATCHING
        assert len(activity.content.pairs) == 2

    def test_ordering_schema_valid(self) -> None:
        content = OrderingContent(
            activity_type=ActivityType.ORDERING,
            prompt="Put the numbers in order from smallest to biggest.",
            items=[
                OrderingItem(id="num_3", label="3"),
                OrderingItem(id="num_1", label="1"),
                OrderingItem(id="num_2", label="2"),
            ],
            correct_sequence=["num_1", "num_2", "num_3"],
            direction="ascending",
        )
        activity = Activity(
            objective_id=mock_objective_id,
            activity_type=ActivityType.ORDERING,
            title="Ordering Numbers",
            instructions="Arrange the cards from 1 to 3.",
            content=content,
        )
        assert activity.activity_type == ActivityType.ORDERING
        assert activity.content.correct_sequence == ["num_1", "num_2", "num_3"]

    def test_visual_identification_schema_valid(self) -> None:
        content = VisualIdentificationContent(
            activity_type=ActivityType.VISUAL_IDENTIFICATION,
            prompt="Find the triangle on the table.",
            scene_description="A sunny classroom table with geometric blocks.",
            elements=[
                VisualElement(id="el_1", label="Blue Triangle", is_target=True),
                VisualElement(id="el_2", label="Red Square", is_target=False),
            ],
            target_id="el_1",
            feedback_clue="Look for the three pointed corners.",
        )
        activity = Activity(
            objective_id=mock_objective_id,
            activity_type=ActivityType.VISUAL_IDENTIFICATION,
            title="Spot the Shape",
            instructions="Tap the shape that is a triangle.",
            content=content,
        )
        assert activity.activity_type == ActivityType.VISUAL_IDENTIFICATION
        assert activity.content.target_id == "el_1"

    def test_drag_drop_schema_valid(self) -> None:
        content = DragDropContent(
            activity_type=ActivityType.DRAG_DROP,
            prompt="Sort the shapes into the correct boxes.",
            items=[
                DragItem(id="d1", label="Round Ball"),
                DragItem(id="d2", label="Square Box"),
            ],
            zones=[
                DropZone(id="z_round", label="Round Things"),
                DropZone(id="z_square", label="Square Things"),
            ],
            correct_mapping={"d1": "z_round", "d2": "z_square"},
        )
        activity = Activity(
            objective_id=mock_objective_id,
            activity_type=ActivityType.DRAG_DROP,
            title="Sorting Shapes",
            instructions="Drag each item into its matching box.",
            content=content,
        )
        assert activity.activity_type == ActivityType.DRAG_DROP
        assert activity.content.correct_mapping["d1"] == "z_round"

    def test_difficulty_bounds(self) -> None:
        content = MultipleChoiceContent(
            activity_type=ActivityType.MULTIPLE_CHOICE,
            question="Valid question?",
            options=[
                MultipleChoiceOption(id="o1", text="A", is_correct=True),
                MultipleChoiceOption(id="o2", text="B", is_correct=False),
            ],
            correct_answer_id="o1",
            explanation="Explanation",
        )
        with pytest.raises(ValidationError):
            Activity(
                objective_id=mock_objective_id,
                activity_type=ActivityType.MULTIPLE_CHOICE,
                title="Invalid Difficulty",
                instructions="Instructions",
                difficulty_level=6,  # > 5
                content=content,
            )


# ── 2. Fallback Generator Tests ──────────────────────────────────────────────


class TestFallbackGenerator:
    """Verify deterministic fallback activities for all 5 types."""

    @pytest.mark.parametrize(
        "act_type",
        [
            ActivityType.MULTIPLE_CHOICE,
            ActivityType.MATCHING,
            ActivityType.ORDERING,
            ActivityType.VISUAL_IDENTIFICATION,
            ActivityType.DRAG_DROP,
        ],
    )
    def test_fallback_generates_valid_activity(self, act_type: ActivityType) -> None:
        fallback = create_fallback_activity(
            objective_id=mock_objective_id,
            objective_title="Counting 1 to 5",
            objective_description="Count 5 objects accurately",
            difficulty_level=2,
            activity_type=act_type,
            language="en",
        )
        assert fallback.objective_id == mock_objective_id
        assert fallback.activity_type == act_type
        assert fallback.difficulty_level == 2
        assert fallback.metadata.get("fallback_used") is True
        assert len(fallback.hints) >= 1


# ── 3. Prompt Builder Tests ──────────────────────────────────────────────────


class TestPromptBuilder:
    """Test message construction adhering to cognitive calm & educational guidelines."""

    def test_build_messages_structure(self) -> None:
        messages = build_activity_generation_messages(
            objective_title="Basic Addition",
            objective_description="Add two single-digit numbers.",
            difficulty_level=2,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            learner_context={
                "communication_preferences": {"primary_mode": "verbal"},
                "support_requirements": {"guidance_level": "moderate", "pacing": "relaxed"},
                "teacher_constraints": {"custom_guidelines": "Avoid red colored items"},
            },
            language="en",
        )
        assert len(messages) == 2
        assert messages[0].role == MessageRole.SYSTEM
        assert "Cognitive Calm" in messages[0].content
        assert messages[1].role == MessageRole.USER
        assert "Basic Addition" in messages[1].content
        assert "Avoid red colored items" in messages[1].content


# ── 4. Service Layer Tests ───────────────────────────────────────────────────


class TestActivityService:
    """Tests for ActivityService orchestration and fallback resilience."""

    @pytest.mark.asyncio
    async def test_service_generates_via_mock_orchestrator(self) -> None:
        # Mock orchestrator returning a valid MultipleChoice dict
        mock_provider = MagicMock(spec=LLMProvider)
        mock_provider.provider_name = "mock_gemini"
        mock_provider.is_available = True

        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        mock_orchestrator.provider = mock_provider
        mock_orchestrator.generate_structured = AsyncMock(
            return_value={
                "id": str(uuid.uuid4()),
                "objective_id": str(mock_objective_id),
                "activity_type": "multiple_choice",
                "title": "Generated Apples",
                "instructions": "Pick the right basket.",
                "difficulty_level": 2,
                "content": {
                    "activity_type": "multiple_choice",
                    "question": "Which basket has 4 apples?",
                    "options": [
                        {"id": "opt_1", "text": "Basket with 4", "is_correct": True},
                        {"id": "opt_2", "text": "Basket with 2", "is_correct": False},
                    ],
                    "correct_answer_id": "opt_1",
                    "explanation": "Great job!",
                },
                "hints": ["Count the apples one by one."],
                "scaffolding_level": 1,
            }
        )

        session = AsyncMock()
        service = ActivityService(session=session, orchestrator=mock_orchestrator)

        with patch(
            "app.curriculum.service.CurriculumService.get_learning_objective",
            new_callable=AsyncMock,
            return_value=mock_objective,
        ):
            response = await service.generate_activity(
                request=ActivityGenerateRequest(
                    objective_id=mock_objective_id,
                    activity_type=ActivityType.MULTIPLE_CHOICE,
                ),
                current_user=mock_teacher,
            )

            assert response.fallback_used is False
            assert response.generation_source == "mock_gemini"
            assert response.activity.title == "Generated Apples"
            assert response.activity.activity_type == ActivityType.MULTIPLE_CHOICE

    @pytest.mark.asyncio
    async def test_service_gracefully_falls_back_on_orchestrator_failure(self) -> None:
        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        mock_orchestrator.generate_structured = AsyncMock(
            side_effect=AIProviderError("Gemini quota exceeded.")
        )

        session = AsyncMock()
        service = ActivityService(session=session, orchestrator=mock_orchestrator)

        with patch(
            "app.curriculum.service.CurriculumService.get_learning_objective",
            new_callable=AsyncMock,
            return_value=mock_objective,
        ):
            response = await service.generate_activity(
                request=ActivityGenerateRequest(
                    objective_id=mock_objective_id,
                    activity_type=ActivityType.MATCHING,
                ),
                current_user=mock_teacher,
            )

            assert response.fallback_used is True
            assert response.generation_source == "deterministic_fallback"
            assert response.activity.activity_type == ActivityType.MATCHING

    @pytest.mark.asyncio
    async def test_service_rejects_missing_objective(self) -> None:
        session = AsyncMock()
        service = ActivityService(session=session)

        with patch(
            "app.curriculum.service.CurriculumService.get_learning_objective",
            new_callable=AsyncMock,
            return_value=None,
        ):
            with pytest.raises(NotFoundError):
                await service.generate_activity(
                    request=ActivityGenerateRequest(objective_id=uuid.uuid4()),
                    current_user=mock_teacher,
                )

    @pytest.mark.asyncio
    async def test_service_enforces_teacher_modality_exclusion(self) -> None:
        session = AsyncMock()
        service = ActivityService(session=session)

        mock_learner_id = uuid.uuid4()
        learner = Learner(
            id=mock_learner_id,
            name="Restricted Learner",
            teacher_id=teacher_id,
        )
        profile = LearnerProfile(
            learner_id=mock_learner_id,
            teacher_constraints={"excluded_modalities": ["drag_drop"]},
        )
        learner.profile = profile

        with patch(
            "app.curriculum.service.CurriculumService.get_learning_objective",
            new_callable=AsyncMock,
            return_value=mock_objective,
        ), patch(
            "app.learners.service.LearnerService.get_by_id",
            new_callable=AsyncMock,
            return_value=learner,
        ):
            with pytest.raises(EduviaValidationError):
                await service.generate_activity(
                    request=ActivityGenerateRequest(
                        objective_id=mock_objective_id,
                        learner_id=mock_learner_id,
                        activity_type=ActivityType.DRAG_DROP,
                    ),
                    current_user=mock_teacher,
                )

    # ── Audit 1: Zero-Strand Guarantee Failure Mode Verifications ─────────────

    @pytest.mark.asyncio
    async def test_zero_strand_timeout_failure(self) -> None:
        """Verify timeout/service failure triggers valid deterministic fallback."""
        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        mock_orchestrator.generate_structured = AsyncMock(
            side_effect=TimeoutError("Request to Gemini API timed out after 30s")
        )

        service = ActivityService(session=AsyncMock(), orchestrator=mock_orchestrator)
        with patch(
            "app.curriculum.service.CurriculumService.get_learning_objective",
            new_callable=AsyncMock,
            return_value=mock_objective,
        ):
            response = await service.generate_activity(
                request=ActivityGenerateRequest(
                    objective_id=mock_objective_id,
                    activity_type=ActivityType.ORDERING,
                ),
                current_user=mock_teacher,
            )
            assert response.fallback_used is True
            assert response.generation_source == "deterministic_fallback"
            assert response.activity.activity_type == ActivityType.ORDERING
            # Verify fallback validates strictly against Pydantic Activity schema
            validated = Activity.model_validate(response.activity.model_dump())
            assert validated.id == response.activity.id

    @pytest.mark.asyncio
    async def test_zero_strand_invalid_json_non_dict(self) -> None:
        """Verify non-dict/unparseable structured response triggers valid fallback."""
        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        mock_orchestrator.generate_structured = AsyncMock(
            return_value="not a dictionary output"
        )

        service = ActivityService(session=AsyncMock(), orchestrator=mock_orchestrator)
        with patch(
            "app.curriculum.service.CurriculumService.get_learning_objective",
            new_callable=AsyncMock,
            return_value=mock_objective,
        ):
            response = await service.generate_activity(
                request=ActivityGenerateRequest(
                    objective_id=mock_objective_id,
                    activity_type=ActivityType.VISUAL_IDENTIFICATION,
                ),
                current_user=mock_teacher,
            )
            assert response.fallback_used is True
            assert response.activity.activity_type == ActivityType.VISUAL_IDENTIFICATION
            Activity.model_validate(response.activity.model_dump())

    @pytest.mark.asyncio
    async def test_zero_strand_valid_json_with_invalid_schema(self) -> None:
        """Verify valid JSON with nonsensical schema triggers valid fallback."""
        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        mock_orchestrator.generate_structured = AsyncMock(
            return_value={
                "unrelated_key": 999,
                "wrong_format": True,
            }
        )

        service = ActivityService(session=AsyncMock(), orchestrator=mock_orchestrator)
        with patch(
            "app.curriculum.service.CurriculumService.get_learning_objective",
            new_callable=AsyncMock,
            return_value=mock_objective,
        ):
            response = await service.generate_activity(
                request=ActivityGenerateRequest(
                    objective_id=mock_objective_id,
                    activity_type=ActivityType.DRAG_DROP,
                ),
                current_user=mock_teacher,
            )
            assert response.fallback_used is True
            assert response.activity.activity_type == ActivityType.DRAG_DROP
            Activity.model_validate(response.activity.model_dump())

    @pytest.mark.asyncio
    async def test_zero_strand_missing_required_fields(self) -> None:
        """Verify missing critical fields (e.g. content) triggers fallback."""
        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        mock_orchestrator.generate_structured = AsyncMock(
            return_value={
                "title": "A Title Without Content",
                "instructions": "Instructions only",
            }
        )

        service = ActivityService(session=AsyncMock(), orchestrator=mock_orchestrator)
        with patch(
            "app.curriculum.service.CurriculumService.get_learning_objective",
            new_callable=AsyncMock,
            return_value=mock_objective,
        ):
            response = await service.generate_activity(
                request=ActivityGenerateRequest(
                    objective_id=mock_objective_id,
                    activity_type=ActivityType.MULTIPLE_CHOICE,
                ),
                current_user=mock_teacher,
            )
            assert response.fallback_used is True
            assert response.activity.activity_type == ActivityType.MULTIPLE_CHOICE
            Activity.model_validate(response.activity.model_dump())

    @pytest.mark.asyncio
    async def test_zero_strand_empty_null_model_response(self) -> None:
        """Verify empty dict or None from LLM triggers fallback."""
        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        mock_orchestrator.generate_structured = AsyncMock(return_value={})

        service = ActivityService(session=AsyncMock(), orchestrator=mock_orchestrator)
        with patch(
            "app.curriculum.service.CurriculumService.get_learning_objective",
            new_callable=AsyncMock,
            return_value=mock_objective,
        ):
            response = await service.generate_activity(
                request=ActivityGenerateRequest(
                    objective_id=mock_objective_id,
                    activity_type=ActivityType.MATCHING,
                ),
                current_user=mock_teacher,
            )
            assert response.fallback_used is True
            assert response.activity.activity_type == ActivityType.MATCHING
            Activity.model_validate(response.activity.model_dump())

    def test_zero_strand_unsupported_activity_type_fallback(self) -> None:
        """Verify fallback gracefully recovers if passed an unsupported activity type."""
        fallback = create_fallback_activity(
            objective_id=mock_objective_id,
            objective_title="Test Objective",
            activity_type="unsupported_quantum_teleportation",  # type: ignore[arg-type]
        )
        assert fallback.activity_type == ActivityType.MULTIPLE_CHOICE
        Activity.model_validate(fallback.model_dump())



# ── 5. API Endpoint Tests ────────────────────────────────────────────────────


class TestActivityAPI:
    """HTTP API integration tests for /activities endpoints."""

    def test_list_activity_types(self) -> None:
        response = client.get("/api/v1/activities/types")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        types = [item["type"] for item in data]
        assert "multiple_choice" in types
        assert "matching" in types
        assert "ordering" in types
        assert "visual_identification" in types
        assert "drag_drop" in types

    def test_generate_activity_unauthenticated(self) -> None:
        response = client.post(
            "/api/v1/activities/generate",
            json={"objective_id": str(mock_objective_id)},
        )
        assert response.status_code == 401

    def test_generate_activity_with_auth_success(self) -> None:
        token = create_access_token(subject=str(teacher_id))
        headers = {"Authorization": f"Bearer {token}"}

        from app.auth.dependencies import get_current_user
        app.dependency_overrides[get_current_user] = lambda: mock_teacher

        try:
            with patch(
                "app.curriculum.service.CurriculumService.get_learning_objective",
                new_callable=AsyncMock,
                return_value=mock_objective,
            ):
                response = client.post(
                    "/api/v1/activities/generate",
                    json={
                        "objective_id": str(mock_objective_id),
                        "activity_type": "multiple_choice",
                    },
                    headers=headers,
                )
                assert response.status_code == 200
                data = response.json()
                assert "activity" in data
                assert data["activity"]["activity_type"] == "multiple_choice"
                assert data["objective_id"] == str(mock_objective_id)
                assert "fallback_used" in data
        finally:
            app.dependency_overrides.pop(get_current_user, None)
