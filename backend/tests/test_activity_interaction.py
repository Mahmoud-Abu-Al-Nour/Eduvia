"""
Eduvia — Phase 5: Activity Interaction & Authoritative Evaluation Tests

Tests:
1. Multiple Choice answer evaluation (correct, incorrect, invalid option).
2. Matching pairs answer evaluation (perfect match, partial match, invalid item).
3. Ordering sequence evaluation (correct order, partially correct, length mismatch, invalid ID).
4. Visual Identification evaluation (target match, distractor match with clue, invalid ID).
5. Drag and Drop evaluation (correct categorization, partial placement, invalid zone).
6. Scaffolding & Mastery determination based on LearningObjective assessment criteria.
7. Modality mismatch and payload rejection.
8. API endpoints (POST /api/v1/activities/evaluate and GET /api/v1/activities/{id}).
"""
import uuid
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.activities.fallbacks import create_fallback_activity
from app.activities.schemas import (
    ActivityEvaluationResponse,
    ActivitySubmissionRequest,
    ActivityType,
    DragDropContent,
    DragDropSubmission,
    MatchingContent,
    MatchingPair,
    MatchingSubmission,
    MultipleChoiceContent,
    MultipleChoiceSubmission,
    OrderingContent,
    OrderingSubmission,
    VisualIdentificationContent,
    VisualIdentificationSubmission,
)
from app.activities.service import ActivityService
from app.core.errors import NotFoundError, ValidationError
from app.main import app

client = TestClient(app)

OBJ_ID = uuid.UUID("77777777-7777-7777-7777-777777777777")
ACTIVITY_ID = uuid.UUID("99999999-9999-9999-9999-999999999999")


@pytest.fixture
def activity_service() -> ActivityService:
    mock_session = AsyncMock()
    mock_result = AsyncMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result
    return ActivityService(session=mock_session)


# ── Modality 1: Multiple Choice Evaluation ───────────────────────────────────


@pytest.mark.asyncio
async def test_evaluate_multiple_choice_correct(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Number recognition",
        activity_type=ActivityType.MULTIPLE_CHOICE,
    )
    content: MultipleChoiceContent = activity.content  # type: ignore

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.MULTIPLE_CHOICE,
        submission=MultipleChoiceSubmission(selected_option_id=content.correct_answer_id),
        hints_used=0,
        activity_content=content,
    )

    result = await activity_service.evaluate_submission(request)
    assert result.is_correct is True
    assert result.score == 1.0
    assert result.assistance_level == 0
    assert "Wonderful focus!" in result.feedback


@pytest.mark.asyncio
async def test_evaluate_multiple_choice_incorrect(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Number recognition",
        activity_type=ActivityType.MULTIPLE_CHOICE,
    )
    content: MultipleChoiceContent = activity.content  # type: ignore

    incorrect_opt = next(opt for opt in content.options if opt.id != content.correct_answer_id)

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.MULTIPLE_CHOICE,
        submission=MultipleChoiceSubmission(selected_option_id=incorrect_opt.id),
        hints_used=1,
        activity_content=content,
    )

    result = await activity_service.evaluate_submission(request)
    assert result.is_correct is False
    assert result.score == 0.0
    assert result.mastery_achieved is False
    assert "Good effort!" in result.feedback


@pytest.mark.asyncio
async def test_evaluate_multiple_choice_invalid_option_raises(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Number recognition",
        activity_type=ActivityType.MULTIPLE_CHOICE,
    )
    content: MultipleChoiceContent = activity.content  # type: ignore

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.MULTIPLE_CHOICE,
        submission=MultipleChoiceSubmission(selected_option_id="nonexistent_option"),
        hints_used=0,
        activity_content=content,
    )

    with pytest.raises(ValidationError) as exc_info:
        await activity_service.evaluate_submission(request)
    assert "does not exist in activity options" in str(exc_info.value)


# ── Modality 2: Matching Pairs Evaluation ────────────────────────────────────


@pytest.mark.asyncio
async def test_evaluate_matching_perfect(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Counting dots",
        activity_type=ActivityType.MATCHING,
    )
    content: MatchingContent = activity.content  # type: ignore

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.MATCHING,
        submission=MatchingSubmission(pairs=content.pairs),
        hints_used=0,
        activity_content=content,
    )

    result = await activity_service.evaluate_submission(request)
    assert result.is_correct is True
    assert result.score == 1.0
    assert "Brilliant matching!" in result.feedback


@pytest.mark.asyncio
async def test_evaluate_matching_partial(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Counting dots",
        activity_type=ActivityType.MATCHING,
    )
    content: MatchingContent = activity.content  # type: ignore

    # Submit only the first pair correct, rest swapped or wrong
    first_pair = content.pairs[0]
    wrong_pairs = [first_pair]
    # Intentionally reverse right IDs for other pairs
    for p in content.pairs[1:]:
        wrong_pairs.append(MatchingPair(left_id=p.left_id, right_id=content.right_items[0].id))

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.MATCHING,
        submission=MatchingSubmission(pairs=wrong_pairs),
        hints_used=1,
        activity_content=content,
    )

    result = await activity_service.evaluate_submission(request)
    assert result.is_correct is False
    assert 0.0 < result.score < 1.0
    assert "connected" in result.feedback


@pytest.mark.asyncio
async def test_evaluate_matching_invalid_item_raises(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Counting dots",
        activity_type=ActivityType.MATCHING,
    )
    content: MatchingContent = activity.content  # type: ignore

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.MATCHING,
        submission=MatchingSubmission(
            pairs=[MatchingPair(left_id="bogus_left", right_id=content.right_items[0].id)]
        ),
        hints_used=0,
        activity_content=content,
    )

    with pytest.raises(ValidationError) as exc_info:
        await activity_service.evaluate_submission(request)
    assert "does not exist in matching activity" in str(exc_info.value)


# ── Modality 3: Ordering Sequence Evaluation ─────────────────────────────────


@pytest.mark.asyncio
async def test_evaluate_ordering_correct(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Order sequence",
        activity_type=ActivityType.ORDERING,
    )
    content: OrderingContent = activity.content  # type: ignore

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.ORDERING,
        submission=OrderingSubmission(ordered_ids=content.correct_sequence),
        hints_used=0,
        activity_content=content,
    )

    result = await activity_service.evaluate_submission(request)
    assert result.is_correct is True
    assert result.score == 1.0
    assert "Spot on!" in result.feedback


@pytest.mark.asyncio
async def test_evaluate_ordering_length_mismatch_raises(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Order sequence",
        activity_type=ActivityType.ORDERING,
    )
    content: OrderingContent = activity.content  # type: ignore

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.ORDERING,
        submission=OrderingSubmission(ordered_ids=[content.correct_sequence[0]]),
        hints_used=0,
        activity_content=content,
    )

    with pytest.raises(ValidationError) as exc_info:
        await activity_service.evaluate_submission(request)
    assert "Expected" in str(exc_info.value)


# ── Modality 4: Visual Identification Evaluation ─────────────────────────────


@pytest.mark.asyncio
async def test_evaluate_visual_identification_correct(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Find red circle",
        activity_type=ActivityType.VISUAL_IDENTIFICATION,
    )
    content: VisualIdentificationContent = activity.content  # type: ignore

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.VISUAL_IDENTIFICATION,
        submission=VisualIdentificationSubmission(selected_element_id=content.target_id),
        hints_used=0,
        activity_content=content,
    )

    result = await activity_service.evaluate_submission(request)
    assert result.is_correct is True
    assert result.score == 1.0
    assert "Fantastic observation!" in result.feedback


@pytest.mark.asyncio
async def test_evaluate_visual_identification_incorrect_gentle_clue(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Find red circle",
        activity_type=ActivityType.VISUAL_IDENTIFICATION,
    )
    content: VisualIdentificationContent = activity.content  # type: ignore

    other_element = next(el for el in content.elements if el.id != content.target_id)

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.VISUAL_IDENTIFICATION,
        submission=VisualIdentificationSubmission(selected_element_id=other_element.id),
        hints_used=0,
        activity_content=content,
    )

    result = await activity_service.evaluate_submission(request)
    assert result.is_correct is False
    assert result.score == 0.0
    assert content.feedback_clue in result.feedback


# ── Modality 5: Drag and Drop Evaluation ─────────────────────────────────────


@pytest.mark.asyncio
async def test_evaluate_drag_drop_correct(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Sort shapes",
        activity_type=ActivityType.DRAG_DROP,
    )
    content: DragDropContent = activity.content  # type: ignore

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.DRAG_DROP,
        submission=DragDropSubmission(item_to_zone_mapping=content.correct_mapping),
        hints_used=0,
        activity_content=content,
    )

    result = await activity_service.evaluate_submission(request)
    assert result.is_correct is True
    assert result.score == 1.0
    assert "Excellent sorting!" in result.feedback


@pytest.mark.asyncio
async def test_evaluate_drag_drop_invalid_zone_raises(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Sort shapes",
        activity_type=ActivityType.DRAG_DROP,
    )
    content: DragDropContent = activity.content  # type: ignore

    item_id = next(iter(content.correct_mapping.keys()))
    bad_mapping = {item_id: "nonexistent_zone"}

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.DRAG_DROP,
        submission=DragDropSubmission(item_to_zone_mapping=bad_mapping),
        hints_used=0,
        activity_content=content,
    )

    with pytest.raises(ValidationError) as exc_info:
        await activity_service.evaluate_submission(request)
    assert "does not exist in activity zones" in str(exc_info.value)


# ── Rubric & Scaffolding Mastery Evaluation ──────────────────────────────────


@pytest.mark.asyncio
async def test_mastery_blocked_by_excessive_assistance(activity_service: ActivityService):
    """
    Cognitive calm / objective assessment rubric:
    Even with 100% accuracy, mastery is not attained if assistance level exceeds maximum.
    """
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Number recognition",
        activity_type=ActivityType.MULTIPLE_CHOICE,
    )
    content: MultipleChoiceContent = activity.content  # type: ignore

    # Mock learning objective with max_assistance_level = 1
    mock_obj = AsyncMock()
    mock_obj.assessment_criteria = {"minimum_accuracy": 0.8, "maximum_assistance_level": 1}

    with patch.object(activity_service, "session") as mock_session:
        with patch("app.activities.service.CurriculumService.get_learning_objective", return_value=mock_obj):
            # Learner used 3 hints (Level 3 explicit demonstration)
            request = ActivitySubmissionRequest(
                activity_id=activity.id,
                objective_id=OBJ_ID,
                activity_type=ActivityType.MULTIPLE_CHOICE,
                submission=MultipleChoiceSubmission(selected_option_id=content.correct_answer_id),
                hints_used=3,
                activity_content=content,
            )

            result = await activity_service.evaluate_submission(request)
            assert result.score == 1.0
            assert result.is_correct is True
            # Assistance level 3 exceeds maximum assistance level 1
            assert result.mastery_achieved is False


# ── API Endpoint Tests ────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def setup_api_dependencies():
    from app.activities.router import get_activity_service
    from app.database.session import get_db_session

    mock_session = AsyncMock()
    mock_result = AsyncMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result
    service = ActivityService(session=mock_session)

    app.dependency_overrides[get_db_session] = lambda: mock_session
    app.dependency_overrides[get_activity_service] = lambda: service
    yield
    app.dependency_overrides.pop(get_db_session, None)
    app.dependency_overrides.pop(get_activity_service, None)


def test_api_evaluate_submission_success():
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Numeracy",
        activity_type=ActivityType.MULTIPLE_CHOICE,
    )
    content: MultipleChoiceContent = activity.content  # type: ignore

    payload = {
        "activity_id": str(activity.id),
        "objective_id": str(OBJ_ID),
        "activity_type": "multiple_choice",
        "submission": {
            "activity_type": "multiple_choice",
            "selected_option_id": content.correct_answer_id,
        },
        "hints_used": 0,
        "time_spent_seconds": 12.5,
        "activity_content": content.model_dump(),
    }

    response = client.post("/api/v1/activities/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is True
    assert data["score"] == 1.0
    assert "feedback" in data


def test_api_evaluate_submission_modality_mismatch():
    payload = {
        "activity_id": str(uuid.uuid4()),
        "objective_id": str(OBJ_ID),
        "activity_type": "multiple_choice",
        "submission": {
            "activity_type": "ordering",
            "ordered_ids": ["item_1", "item_2"],
        },
        "hints_used": 0,
    }
    response = client.post("/api/v1/activities/evaluate", json=payload)
    assert response.status_code in (400, 422)


def test_api_get_activity_not_found():
    random_id = str(uuid.uuid4())
    response = client.get(f"/api/v1/activities/{random_id}")
    assert response.status_code == 404


def test_api_get_activity_malformed_uuid():
    response = client.get("/api/v1/activities/not-a-valid-uuid")
    assert response.status_code == 422


def test_api_get_activity_valid_cached():
    from app.activities.service import _ACTIVITIES_CACHE
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Cached numeracy",
        activity_type=ActivityType.MULTIPLE_CHOICE,
    )
    _ACTIVITIES_CACHE[activity.id] = activity

    response = client.get(f"/api/v1/activities/{activity.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(activity.id)
    assert data["activity_type"] == "multiple_choice"


def test_api_evaluate_submission_nonexistent_activity_404():
    nonexistent_id = str(uuid.uuid4())
    payload = {
        "activity_id": nonexistent_id,
        "objective_id": str(OBJ_ID),
        "activity_type": "multiple_choice",
        "submission": {
            "activity_type": "multiple_choice",
            "selected_option_id": "opt_1",
        },
        "hints_used": 0,
    }
    response = client.post("/api/v1/activities/evaluate", json=payload)
    assert response.status_code == 404


def test_api_evaluate_submission_malformed_payload_422():
    # Missing 'submission'
    payload = {
        "activity_id": str(uuid.uuid4()),
        "objective_id": str(OBJ_ID),
        "activity_type": "multiple_choice",
    }
    response = client.post("/api/v1/activities/evaluate", json=payload)
    assert response.status_code == 422


def test_api_evaluate_submission_invalid_option_id_422():
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Numeracy",
        activity_type=ActivityType.MULTIPLE_CHOICE,
    )
    content: MultipleChoiceContent = activity.content  # type: ignore

    payload = {
        "activity_id": str(activity.id),
        "objective_id": str(OBJ_ID),
        "activity_type": "multiple_choice",
        "submission": {
            "activity_type": "multiple_choice",
            "selected_option_id": "completely_invalid_option_id",
        },
        "hints_used": 0,
        "activity_content": content.model_dump(),
    }

    response = client.post("/api/v1/activities/evaluate", json=payload)
    assert response.status_code == 422
    assert "does not exist in activity options" in response.json()["detail"]


def test_protected_teacher_endpoints_require_auth():
    # Activity generation requires teacher auth
    gen_resp = client.post("/api/v1/activities/generate", json={"objective_id": str(OBJ_ID)})
    assert gen_resp.status_code == 401

    # Learner roster requires teacher auth
    learners_resp = client.get("/api/v1/learners")
    assert learners_resp.status_code == 401


# ── Additional Modality Edge Cases & Authority Verification ──────────────────


@pytest.mark.asyncio
async def test_evaluate_ordering_inverted_sequence(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Order sequence",
        activity_type=ActivityType.ORDERING,
    )
    content: OrderingContent = activity.content  # type: ignore

    inverted_seq = list(reversed(content.correct_sequence))

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.ORDERING,
        submission=OrderingSubmission(ordered_ids=inverted_seq),
        hints_used=0,
        activity_content=content,
    )

    result = await activity_service.evaluate_submission(request)
    assert result.is_correct is False
    assert result.score < 1.0


@pytest.mark.asyncio
async def test_evaluate_ordering_invalid_item_raises(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Order sequence",
        activity_type=ActivityType.ORDERING,
    )
    content: OrderingContent = activity.content  # type: ignore

    bad_seq = [content.correct_sequence[0], "bogus_item_id", content.correct_sequence[2]]

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.ORDERING,
        submission=OrderingSubmission(ordered_ids=bad_seq),
        hints_used=0,
        activity_content=content,
    )

    with pytest.raises(ValidationError) as exc_info:
        await activity_service.evaluate_submission(request)
    assert "does not exist in ordering activity items" in str(exc_info.value)


@pytest.mark.asyncio
async def test_evaluate_visual_identification_invalid_element_raises(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Find red circle",
        activity_type=ActivityType.VISUAL_IDENTIFICATION,
    )
    content: VisualIdentificationContent = activity.content  # type: ignore

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.VISUAL_IDENTIFICATION,
        submission=VisualIdentificationSubmission(selected_element_id="nonexistent_element"),
        hints_used=0,
        activity_content=content,
    )

    with pytest.raises(ValidationError) as exc_info:
        await activity_service.evaluate_submission(request)
    assert "does not exist in scene elements" in str(exc_info.value)


@pytest.mark.asyncio
async def test_evaluate_drag_drop_partial_and_incorrect(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Sort shapes",
        activity_type=ActivityType.DRAG_DROP,
    )
    content: DragDropContent = activity.content  # type: ignore

    zones = [z.id for z in content.zones]
    partial_mapping = {}
    items = list(content.correct_mapping.keys())
    for idx, item_id in enumerate(items):
        if idx % 2 == 0:
            partial_mapping[item_id] = content.correct_mapping[item_id]
        else:
            wrong_zone = [z for z in zones if z != content.correct_mapping[item_id]][0]
            partial_mapping[item_id] = wrong_zone

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.DRAG_DROP,
        submission=DragDropSubmission(item_to_zone_mapping=partial_mapping),
        hints_used=0,
        activity_content=content,
    )

    result = await activity_service.evaluate_submission(request)
    assert result.is_correct is False
    assert 0.0 < result.score < 1.0


@pytest.mark.asyncio
async def test_evaluate_drag_drop_invalid_item_raises(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Sort shapes",
        activity_type=ActivityType.DRAG_DROP,
    )
    content: DragDropContent = activity.content  # type: ignore

    bad_mapping = {"nonexistent_item": content.zones[0].id}

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.DRAG_DROP,
        submission=DragDropSubmission(item_to_zone_mapping=bad_mapping),
        hints_used=0,
        activity_content=content,
    )

    with pytest.raises(ValidationError) as exc_info:
        await activity_service.evaluate_submission(request)
    assert "does not exist in activity items" in str(exc_info.value)


@pytest.mark.asyncio
async def test_evaluate_matching_zero_correct(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Counting dots",
        activity_type=ActivityType.MATCHING,
    )
    content: MatchingContent = activity.content  # type: ignore

    # Deliberately mismatch every pair
    all_wrong_pairs = []
    right_ids = [r.id for r in content.right_items]
    for idx, p in enumerate(content.pairs):
        wrong_right = right_ids[(idx + 1) % len(right_ids)]
        all_wrong_pairs.append(MatchingPair(left_id=p.left_id, right_id=wrong_right))

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.MATCHING,
        submission=MatchingSubmission(pairs=all_wrong_pairs),
        hints_used=0,
        activity_content=content,
    )

    result = await activity_service.evaluate_submission(request)
    assert result.is_correct is False
    assert result.score == 0.0


@pytest.mark.asyncio
async def test_evaluate_matching_invalid_right_item_raises(activity_service: ActivityService):
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Counting dots",
        activity_type=ActivityType.MATCHING,
    )
    content: MatchingContent = activity.content  # type: ignore

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.MATCHING,
        submission=MatchingSubmission(
            pairs=[MatchingPair(left_id=content.left_items[0].id, right_id="bogus_right_item")]
        ),
        hints_used=0,
        activity_content=content,
    )

    with pytest.raises(ValidationError) as exc_info:
        await activity_service.evaluate_submission(request)
    assert "Right item 'bogus_right_item' does not exist in matching activity" in str(exc_info.value)


@pytest.mark.asyncio
async def test_backend_evaluation_authority_ignores_client_flags(activity_service: ActivityService):
    """
    Authoritative backend check:
    Client submitting an incorrect answer cannot obtain a passing evaluation.
    """
    activity = create_fallback_activity(
        objective_id=OBJ_ID,
        objective_title="Number recognition",
        activity_type=ActivityType.MULTIPLE_CHOICE,
    )
    content: MultipleChoiceContent = activity.content  # type: ignore

    wrong_opt = next(opt for opt in content.options if opt.id != content.correct_answer_id)

    request = ActivitySubmissionRequest(
        activity_id=activity.id,
        objective_id=OBJ_ID,
        activity_type=ActivityType.MULTIPLE_CHOICE,
        submission=MultipleChoiceSubmission(selected_option_id=wrong_opt.id),
        hints_used=0,
        activity_content=content,
    )

    result = await activity_service.evaluate_submission(request)
    assert result.is_correct is False
    assert result.score == 0.0
    assert result.mastery_achieved is False


@pytest.mark.asyncio
async def test_zero_strand_compatibility_evaluates_ai_and_fallback_activities(activity_service: ActivityService):
    """
    Zero-Strand compatibility check:
    Activities created via deterministic fallback generator or structured AI output
    are equally consumable and evaluable without modification.
    """
    # 1. Fallback activity
    fallback = create_fallback_activity(OBJ_ID, "Test", ActivityType.MULTIPLE_CHOICE)
    res_fb = await activity_service.evaluate_submission(
        ActivitySubmissionRequest(
            activity_id=fallback.id,
            objective_id=OBJ_ID,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            submission=MultipleChoiceSubmission(selected_option_id=fallback.content.correct_answer_id),
            activity_content=fallback.content,
        )
    )
    assert res_fb.is_correct is True

    # 2. Activity with custom AI-generated structure
    from app.activities.schemas import MultipleChoiceOption
    ai_content = MultipleChoiceContent(
        question="What color is a banana?",
        options=[
            MultipleChoiceOption(id="opt_yellow", text="Yellow", visual_cue="yellow", is_correct=True),
            MultipleChoiceOption(id="opt_blue", text="Blue", visual_cue="blue", is_correct=False),
        ],
        correct_answer_id="opt_yellow",
        explanation="Bananas are bright yellow when ripe.",
    )
    res_ai = await activity_service.evaluate_submission(
        ActivitySubmissionRequest(
            activity_id=uuid.uuid4(),
            objective_id=OBJ_ID,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            submission=MultipleChoiceSubmission(selected_option_id="opt_yellow"),
            activity_content=ai_content,
        )
    )
    assert res_ai.is_correct is True
    assert res_ai.score == 1.0
    assert "Bananas are bright yellow" in str(res_ai.correct_answer_summary)


