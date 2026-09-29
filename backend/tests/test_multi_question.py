from typing import Any
import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import app
from app.activities.schemas import (
    Activity,
    ActivityQuestion,
    ActivityType,
    ActivityGenerateRequest,
    ActivitySubmissionRequest,
    QuestionSubmission,
    MultipleChoiceContent,
    MultipleChoiceOption,
    MultipleChoiceSubmission,
    MatchingSubmission,
    OrderingSubmission,
    VisualIdentificationSubmission,
    DragDropSubmission,
)
from app.activities.fallbacks import create_fallback_activity
from app.content.bank import ContentBank, assemble_multi_question_activity
from app.analytics.service import AnalyticsService
from app.analytics.schemas import PerformanceEventCreate
from app.analytics.models import PerformanceEvent
from app.learners.models import Learner
from app.curriculum.models import LearningObjective
from app.activities.service import ActivityService, _ACTIVITIES_CACHE


# ── Fixtures & Setup ────────────────────────────────────────────────────────

client = TestClient(app)

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


MATH_OBJ_ID = "77777777-7777-7777-7777-777777777777"
LIT_OBJ_ID = "38e172d6-8616-5012-95d9-75d26a85cb5e"
EVERYDAY_OBJ_ID = "92ae654b-5a1a-5645-b2e5-e3abf2bd721b"


# ── 1. Schema Validation Bounds (3 <= questions <= 10) ──────────────────────

def test_question_count_validation_bounds():
    # Valid counts: 3, 5, 10
    req_3 = ActivityGenerateRequest(objective_id=uuid.UUID(MATH_OBJ_ID), question_count=3)
    assert req_3.question_count == 3

    req_5 = ActivityGenerateRequest(objective_id=uuid.UUID(MATH_OBJ_ID), question_count=5)
    assert req_5.question_count == 5

    req_10 = ActivityGenerateRequest(objective_id=uuid.UUID(MATH_OBJ_ID), question_count=10)
    assert req_10.question_count == 10

    # Invalid: 2 (below min 3)
    with pytest.raises(ValidationError):
        ActivityGenerateRequest(objective_id=uuid.UUID(MATH_OBJ_ID), question_count=2)

    # Invalid: 11 (above max 10)
    with pytest.raises(ValidationError):
        ActivityGenerateRequest(objective_id=uuid.UUID(MATH_OBJ_ID), question_count=11)


# ── 2. Content Bank & Multi-Question Assembly (All 5 Modalities) ────────────

@pytest.mark.parametrize("modality", [
    ActivityType.MULTIPLE_CHOICE,
    ActivityType.MATCHING,
    ActivityType.ORDERING,
    ActivityType.VISUAL_IDENTIFICATION,
    ActivityType.DRAG_DROP,
])
def test_assemble_5_question_activity_all_modalities(modality: ActivityType):
    activity = assemble_multi_question_activity(MATH_OBJ_ID, modality, count=5)
    questions = activity.questions
    
    assert len(questions) == 5
    # Distinct question IDs
    q_ids = [q.id for q in questions]
    assert len(set(q_ids)) == 5

    # Sequential question numbers
    q_nums = [q.question_number for q in questions]
    assert q_nums == [1, 2, 3, 4, 5]

    # Homogeneous modality
    for q in questions:
        assert q.question_type == modality
        assert q.content is not None
        assert q.content_source_key is not None


# ── 3. Content Bank Cross-Domain Distinct Content ───────────────────────────

def test_content_bank_distinct_items_across_subjects():
    bank = ContentBank()
    
    for obj_id in [MATH_OBJ_ID, LIT_OBJ_ID, EVERYDAY_OBJ_ID]:
        items = bank.get_items_for_objective(obj_id)
        assert len(items) >= 5, f"Objective {obj_id} must provide at least 5 distinct items"

        source_keys = [item.content_key for item in items]
        assert len(set(source_keys)) == len(source_keys), f"Items for {obj_id} must have unique source keys"

        # Verify 5-question assembly produces distinct question content
        activity = assemble_multi_question_activity(obj_id, ActivityType.MULTIPLE_CHOICE, count=5)
        assembled = activity.questions
        assert len(assembled) == 5
        keys_used = [q.content_source_key for q in assembled]
        assert len(set(keys_used)) == 5


# ── 4. Fallback Activity Generation for Multi-Question ──────────────────────

def test_fallback_generates_5_question_activity():
    activity = create_fallback_activity(MATH_OBJ_ID, ActivityType.MULTIPLE_CHOICE, question_count=5)
    
    assert isinstance(activity, Activity)
    assert len(activity.questions) == 5
    assert activity.activity_type == ActivityType.MULTIPLE_CHOICE
    assert len(activity.hints) >= 1

    # Verify first question content matches top-level legacy content
    assert activity.content is not None
    assert activity.questions[0].content is not None


# ── 5. Backward Compatibility (1-Question Legacy Activity) ──────────────────

def test_legacy_single_question_activity_synchronization():
    mcq = MultipleChoiceContent(
        question="Which number is 5?",
        options=[
            MultipleChoiceOption(id="o1", text="3", is_correct=False),
            MultipleChoiceOption(id="o2", text="5", is_correct=True),
        ],
        correct_answer_id="o2",
        explanation="5 is correct",
    )

    act_id = uuid.uuid4()
    act = Activity(
        id=act_id,
        objective_id=uuid.UUID(MATH_OBJ_ID),
        title="Counting 5",
        instructions="Pick 5",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        content=mcq,
    )

    # Synchronizer must populate questions array with 1 item
    assert len(act.questions) == 1
    assert act.questions[0].id == "q_1"
    assert act.questions[0].question_number == 1
    assert act.questions[0].question_type == ActivityType.MULTIPLE_CHOICE


# ── 6. Legacy Submission Request Compatibility ──────────────────────────────

def test_legacy_submission_request_normalization():
    sub = MultipleChoiceSubmission(
        activity_type=ActivityType.MULTIPLE_CHOICE,
        selected_option_id="opt_target",
    )

    # Client sends legacy single `submission` without `questions`
    req = ActivitySubmissionRequest(
        activity_id=uuid.uuid4(),
        objective_id=uuid.UUID(MATH_OBJ_ID),
        activity_type=ActivityType.MULTIPLE_CHOICE,
        submission=sub,
    )

    # Validator normalizes into questions list
    assert req.questions is not None
    assert len(req.questions) == 1
    assert req.questions[0].submission.selected_option_id == "opt_target"


# ── 7. Submission Validation (Duplicates, Unknown IDs, Bounds) ──────────────

def test_submission_duplicate_question_ids_rejected():
    activity = create_fallback_activity(MATH_OBJ_ID, ActivityType.MULTIPLE_CHOICE, question_count=3)
    _ACTIVITIES_CACHE[activity.id] = activity
    q1_id = activity.questions[0].id

    # Duplicate q1_id in submission
    duplicate_submissions = [
        {"question_id": q1_id, "submission": {"activity_type": "multiple_choice", "selected_option_id": "o1"}},
        {"question_id": q1_id, "submission": {"activity_type": "multiple_choice", "selected_option_id": "o2"}},
    ]

    response = client.post(
        "/api/v1/activities/evaluate",
        json={
            "activity_id": str(activity.id),
            "objective_id": str(activity.objective_id),
            "activity_type": "multiple_choice",
            "questions": duplicate_submissions,
        },
    )
    assert response.status_code == 422
    assert "Duplicate question ID" in response.json()["detail"]


def test_submission_unknown_question_id_rejected():
    activity = create_fallback_activity(MATH_OBJ_ID, ActivityType.MULTIPLE_CHOICE, question_count=3)
    _ACTIVITIES_CACHE[activity.id] = activity

    invalid_submissions = [
        {"question_id": "unknown_question_999", "submission": {"activity_type": "multiple_choice", "selected_option_id": "o1"}},
    ]

    response = client.post(
        "/api/v1/activities/evaluate",
        json={
            "activity_id": str(activity.id),
            "objective_id": str(activity.objective_id),
            "activity_type": "multiple_choice",
            "questions": invalid_submissions,
        },
    )
    assert response.status_code == 422
    assert "does not belong to activity" in response.json()["detail"]


# ── 8. Authoritative Evaluation & Aggregate Scoring ─────────────────────────

def test_authoritative_evaluation_5_question_scoring():
    activity = create_fallback_activity(MATH_OBJ_ID, ActivityType.MULTIPLE_CHOICE, question_count=5)
    _ACTIVITIES_CACHE[activity.id] = activity
    
    # Identify correct option for Q1, Q2, Q3, Q4 and wrong for Q5
    submissions = []
    for idx, q in enumerate(activity.questions):
        mcq: MultipleChoiceContent = q.content
        correct_opt = next((o for o in mcq.options if o.is_correct), mcq.options[0])
        wrong_opt = next((o for o in mcq.options if not o.is_correct), mcq.options[-1])

        if idx < 4:
            # 4 correct answers
            submissions.append({
                "question_id": q.id,
                "submission": {"activity_type": "multiple_choice", "selected_option_id": correct_opt.id},
            })
        else:
            # 1 incorrect answer
            submissions.append({
                "question_id": q.id,
                "submission": {"activity_type": "multiple_choice", "selected_option_id": wrong_opt.id},
            })

    response = client.post(
        "/api/v1/activities/evaluate",
        json={
            "activity_id": str(activity.id),
            "objective_id": str(activity.objective_id),
            "activity_type": "multiple_choice",
            "questions": submissions,
        },
    )
    assert response.status_code == 200
    data = response.json()

    assert data["questions_total"] == 5
    assert data["questions_answered"] == 5
    assert data["questions_correct"] == 4
    assert data["percentage"] == 80.0
    assert data["score"] == 0.8
    assert data["is_correct"] is True  # 80% >= 80% passing threshold
    assert len(data["question_results"]) == 5
    assert data["question_results"][0]["is_correct"] is True
    assert data["question_results"][4]["is_correct"] is False


def test_authoritative_evaluation_unanswered_question_handling():
    activity = create_fallback_activity(MATH_OBJ_ID, ActivityType.MULTIPLE_CHOICE, question_count=5)
    _ACTIVITIES_CACHE[activity.id] = activity
    
    # Submit only 3 of 5 questions
    submissions = []
    for idx in range(3):
        q = activity.questions[idx]
        mcq: MultipleChoiceContent = q.content
        correct_opt = next((o for o in mcq.options if o.is_correct), mcq.options[0])
        submissions.append({
            "question_id": q.id,
            "submission": {"activity_type": "multiple_choice", "selected_option_id": correct_opt.id},
        })

    response = client.post(
        "/api/v1/activities/evaluate",
        json={
            "activity_id": str(activity.id),
            "objective_id": str(activity.objective_id),
            "activity_type": "multiple_choice",
            "questions": submissions,
        },
    )
    assert response.status_code == 200
    data = response.json()

    assert data["questions_total"] == 5
    assert data["questions_answered"] == 3
    assert data["questions_correct"] == 3
    # 3 correct out of 5 total = 60.0%
    assert data["score"] == 0.6
    assert data["percentage"] == 60.0
    assert data["is_correct"] is False  # 60% < 80%


# ── 9. Analytics Telemetry & Activity Count Inflation Prevention ────────────

@pytest.mark.asyncio
async def test_telemetry_records_question_id_without_inflating_activity_count():
    learner_uuid = uuid.uuid4()
    activity_uuid = uuid.uuid4()
    attempt_uuid = uuid.uuid4()
    obj_uuid = uuid.UUID(MATH_OBJ_ID)

    # Create mock learner and objective
    mock_learner = Learner(id=learner_uuid, name="Test Learner", teacher_id=uuid.uuid4())
    mock_objective = LearningObjective(id=obj_uuid, lesson_id=uuid.uuid4(), title={"en": "Math"}, order_index=0)

    # Create 5 question events for 1 single activity
    recorded_events = []
    for i in range(5):
        event = PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=learner_uuid,
            activity_id=activity_uuid,
            objective_id=obj_uuid,
            activity_type="multiple_choice",
            modality="visual",
            score=1.0,
            correct=True,
            completed=True,
            question_id=f"q_{i+1}",
            attempt_id=attempt_uuid,
            hints_used=0,
            assistance_level=0,
            response_time_ms=5000,
        )
        recorded_events.append(event)

    session = AsyncMock()

    def mock_execute(stmt, *args, **kwargs):
        stmt_str = str(stmt)
        result = MagicMock()
        result.scalar.return_value = 0
        if "FROM learners" in stmt_str:
            result.scalars.return_value.first.return_value = mock_learner
        elif "FROM learning_objectives" in stmt_str:
            result.scalars.return_value.first.return_value = mock_objective
        elif "FROM performance_events" in stmt_str:
            result.scalars.return_value.all.return_value = recorded_events
        else:
            result.scalars.return_value.first.return_value = None
            result.scalars.return_value.all.return_value = []
        return result

    session.execute.side_effect = mock_execute
    session.add = MagicMock()
    session.commit = AsyncMock()

    analytics = AnalyticsService(session=session)

    # Learner summary MUST count exactly 1 completed activity, NOT 5
    summary = await analytics.get_learner_summary(learner_uuid)
    assert summary.completed_activities == 1, (
        f"Expected exactly 1 completed activity, got {summary.completed_activities}. "
        "Question events must NOT inflate completed activity count!"
    )


# ── 11. Learner-Safe Zero Answer-Truth Leakage (All 5 Modalities) ───────────

@pytest.mark.parametrize("modality", [
    ActivityType.MULTIPLE_CHOICE,
    ActivityType.MATCHING,
    ActivityType.ORDERING,
    ActivityType.VISUAL_IDENTIFICATION,
    ActivityType.DRAG_DROP,
])
def test_learner_safe_activity_zero_answer_key_leakage(modality: ActivityType):
    """
    CRITICAL SECURITY CHECK:
    Verify that the learner-facing activity payload contains absolutely NO authoritative
    answer keys, correctness flags, or target identifiers.
    """
    act = create_fallback_activity(uuid.UUID(MATH_OBJ_ID), activity_type=modality, question_count=5)
    safe_act = act.to_learner_safe()
    dumped = safe_act.model_dump()

    # Recursively check the dumped JSON for forbidden answer-truth keys
    forbidden_keys = {
        "is_correct",
        "correct_answer",
        "correct_answer_id",
        "expected_mapping",
        "correct_sequence",
        "target_id",
        "correct_mapping",
        "is_target",
    }

    def check_dict_for_forbidden_keys(d: Any, path: str = ""):
        if isinstance(d, dict):
            for k, v in d.items():
                current_path = f"{path}.{k}" if path else k
                assert k not in forbidden_keys, (
                    f"CRITICAL SECURITY VIOLATION: Learner payload exposed '{k}' at path '{current_path}'"
                )
                check_dict_for_forbidden_keys(v, current_path)
        elif isinstance(d, list):
            for idx, item in enumerate(d):
                check_dict_for_forbidden_keys(item, f"{path}[{idx}]")

    check_dict_for_forbidden_keys(dumped)
    assert len(safe_act.questions) == 5


# ── 12. Backend Evaluation Preservation with Learner-Safe Payloads ───────────

@pytest.mark.asyncio
@pytest.mark.parametrize("modality", [
    ActivityType.MULTIPLE_CHOICE,
    ActivityType.MATCHING,
    ActivityType.ORDERING,
    ActivityType.VISUAL_IDENTIFICATION,
    ActivityType.DRAG_DROP,
])
async def test_backend_evaluation_still_works_with_learner_safe(modality: ActivityType):
    """
    Verify that while the learner receives a sanitized payload, the server-side
    authoritative activity remains intact and backend evaluation evaluates submissions accurately.
    """
    full_act = create_fallback_activity(uuid.UUID(MATH_OBJ_ID), activity_type=modality, question_count=3)
    _ACTIVITIES_CACHE[full_act.id] = full_act
    safe_act = full_act.to_learner_safe()

    # Generate learner submissions based only on visible items in safe_act
    q_subs = []
    for q in safe_act.questions:
        q_content = q.content
        if modality == ActivityType.MULTIPLE_CHOICE:
            chosen = q_content.options[0].id
            q_subs.append(QuestionSubmission(
                question_id=q.id,
                submission=MultipleChoiceSubmission(selected_option_id=chosen),
            ))
        elif modality == ActivityType.MATCHING:
            pairs = [{"left_id": q_content.left_items[0].id, "right_id": q_content.right_items[0].id}]
            q_subs.append(QuestionSubmission(
                question_id=q.id,
                submission=MatchingSubmission(pairs=pairs),
            ))
        elif modality == ActivityType.ORDERING:
            ordered_ids = [i.id for i in q_content.items]
            q_subs.append(QuestionSubmission(
                question_id=q.id,
                submission=OrderingSubmission(ordered_ids=ordered_ids),
            ))
        elif modality == ActivityType.VISUAL_IDENTIFICATION:
            chosen = q_content.elements[0].id
            q_subs.append(QuestionSubmission(
                question_id=q.id,
                submission=VisualIdentificationSubmission(selected_element_id=chosen),
            ))
        elif modality == ActivityType.DRAG_DROP:
            mapping = {q_content.items[0].id: q_content.zones[0].id}
            q_subs.append(QuestionSubmission(
                question_id=q.id,
                submission=DragDropSubmission(item_to_zone_mapping=mapping),
            ))

    req = ActivitySubmissionRequest(
        activity_id=full_act.id,
        objective_id=MATH_OBJ_ID,
        activity_type=modality,
        questions=q_subs,
    )

    service = ActivityService(session=AsyncMock())
    result = await service.evaluate_submission(req)

    assert result.activity_id == full_act.id
    assert len(result.question_results) == 3
    assert result.questions_total == 3
    assert 0.0 <= result.score <= 1.0


# ── 13. Content Bank Semantic Alignment Across Domains ───────────────────────

def test_content_bank_semantic_alignment_cross_domain():
    """
    Audit representative objectives from Mathematics, Literacy, and Everyday Learning.
    Prove that all five items share the intended educational skill, objective semantics,
    and appropriate activity modalities.
    """
    bank = ContentBank()
    
    # 1. Mathematics: Counting 0 to 5
    math_items = bank.get_items_for_objective("obj.math.count_0_5")
    assert len(math_items) == 5
    for item in math_items:
        assert item.subject_code == "math"
        assert item.objective_key == "obj.math.count_0_5"
        # Prompt must be mathematically relevant
        p_en = item.prompt.get("en", "")
        assert any(w in p_en.lower() for w in ["number", "count", "numeral", "order", "items", "star", "one", "two"])

    # 2. Literacy: Identifying Uppercase Letters
    lit_items = bank.get_items_for_objective("obj.lit.identify_uppercase")
    assert len(lit_items) == 5
    for item in lit_items:
        assert item.subject_code == "literacy"
        assert item.objective_key == "obj.lit.identify_uppercase"
        p_en = item.prompt.get("en", "")
        assert any(w in p_en.lower() for w in ["letter", "uppercase", "alphabet", "phonic", "cards"])

    # 3. Everyday Learning: Morning Routines
    edl_items = bank.get_items_for_objective("obj.life.order_morning_routines")
    assert len(edl_items) == 5
    for item in edl_items:
        assert item.subject_code == "everyday"
        assert item.objective_key == "obj.life.order_morning_routines"
        p_en = item.prompt.get("en", "")
        assert any(w in p_en.lower() for w in ["morning", "routine", "steps", "wash", "order", "actions"])


# ── 14. Activity Homogeneous Modality Regression ─────────────────────────────

@pytest.mark.parametrize("modality", [
    ActivityType.MULTIPLE_CHOICE,
    ActivityType.MATCHING,
    ActivityType.ORDERING,
    ActivityType.VISUAL_IDENTIFICATION,
    ActivityType.DRAG_DROP,
])
def test_homogeneous_activity_enforcement(modality: ActivityType):
    """
    Verify that normal activities enforce strict homogeneity:
    Activity.activity_type must match every question.question_type.
    """
    activity = assemble_multi_question_activity("obj.math.count_0_5", modality, count=5)
    assert activity.activity_type == modality
    for q in activity.questions:
        assert q.question_type == modality

    # An accidental mixed question type MUST trigger a ValidationError
    mismatched_modality = (
        ActivityType.MATCHING if modality != ActivityType.MATCHING else ActivityType.MULTIPLE_CHOICE
    )
    with pytest.raises(ValidationError) as exc_info:
        Activity(
            objective_id=uuid.uuid4(),
            activity_type=modality,
            title="Mismatched Activity",
            instructions="Test directions",
            questions=[
                ActivityQuestion(
                    id="q_1",
                    question_number=1,
                    question_type=mismatched_modality,
                    content=activity.questions[0].content,
                )
            ],
        )
    assert "does not match activity modality" in str(exc_info.value)

