"""
Eduvia — Instructional Content Domain Tests
Covers:
- Unit tests: Schema validation across all 4 explanation methods and block types
- Unit tests: Deterministic fallback generation for all 4 methods (Zero-Strand Guarantee)
- Service tests: Status transitions (review_required -> approved -> published) and teacher edits
- Router / API tests: Learner visibility rules, teacher approval workflow, non-evaluative contract
"""
import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.auth.security import create_access_token, get_password_hash
from app.curriculum.models import LearningObjective
from app.database.session import get_db_session
from app.instructional.models import InstructionalContent
from app.instructional.router import get_instructional_service
from app.instructional.schemas import (
    ContentBlockType,
    ExplanationMethod,
    InstructionalBlock,
    InstructionalContentRead,
    InstructionalContentUpdate,
    InstructionalGenerateRequest,
    InstructionalStatus,
)
from app.instructional.service import InstructionalService, create_fallback_instructional_content
from app.main import app
from app.users.models import User, UserRole

client = TestClient(app)

MATH_OBJ_ID = uuid.uuid4()
now = datetime.now(UTC)

mock_teacher = User(
    id=uuid.uuid4(),
    email="teacher_inst@eduvia.app",
    full_name="Teacher Instructional",
    hashed_password=get_password_hash("password123"),
    role=UserRole.teacher,
    is_active=True,
    created_at=now,
    updated_at=now,
)

teacher_token = create_access_token(str(mock_teacher.id))
teacher_headers = {"Authorization": f"Bearer {teacher_token}"}


@pytest.fixture(autouse=True)
def override_db():
    mock_session = AsyncMock()
    mock_res = MagicMock()
    mock_res.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_res
    app.dependency_overrides[get_db_session] = lambda: mock_session
    yield
    app.dependency_overrides.pop(get_db_session, None)


# ── 1. Schema Validation Tests ───────────────────────────────────────────────

class TestInstructionalSchemas:
    """Validate Pydantic models for instructional content and blocks."""

    def test_valid_blocks_and_methods(self):
        blocks = [
            InstructionalBlock(
                id="b_1",
                block_type=ContentBlockType.HEADING,
                title="Counting Basics",
                order_index=1,
            ),
            InstructionalBlock(
                id="b_2",
                block_type=ContentBlockType.TEXT,
                body="Let's look at how we count items one by one.",
                order_index=2,
            ),
            InstructionalBlock(
                id="b_3",
                block_type=ContentBlockType.VISUAL_CUE,
                visual_cue="🍎 🍎 🍎",
                order_index=3,
            ),
            InstructionalBlock(
                id="b_4",
                block_type=ContentBlockType.STEP,
                title="Step 1",
                body="Point to the first apple and say 1.",
                order_index=4,
            ),
            InstructionalBlock(
                id="b_5",
                block_type=ContentBlockType.WORKED_EXAMPLE,
                title="Example",
                body="We have 3 apples in front of us.",
                order_index=5,
            ),
            InstructionalBlock(
                id="b_6",
                block_type=ContentBlockType.CALLOUT,
                body="Remember: each object gets exactly one number.",
                order_index=6,
            ),
            InstructionalBlock(
                id="b_7",
                block_type=ContentBlockType.AUDIO_SCRIPT,
                body="Listen carefully as we count together: one, two, three.",
                order_index=7,
            ),
        ]

        content = InstructionalContentRead(
            id=uuid.uuid4(),
            objective_id=MATH_OBJ_ID,
            title="Counting 1 to 5",
            explanation_method=ExplanationMethod.VISUAL_EXPLANATION,
            difficulty_level=1,
            language="en",
            blocks=blocks,
            summary="Understanding counting with concrete visuals.",
            status=InstructionalStatus.REVIEW_REQUIRED,
            created_at=now,
            updated_at=now,
        )

        assert len(content.blocks) == 7
        assert content.explanation_method == ExplanationMethod.VISUAL_EXPLANATION
        assert content.status == InstructionalStatus.REVIEW_REQUIRED

    def test_schema_rejects_unsupported_method(self):
        with pytest.raises(ValidationError):
            InstructionalGenerateRequest(
                objective_id=MATH_OBJ_ID,
                explanation_method="invalid_method_xyz",  # type: ignore
            )

    def test_non_evaluative_contract(self):
        """Verify instructional content schema contains no score or correctness fields."""
        content = InstructionalContentRead(
            id=uuid.uuid4(),
            objective_id=MATH_OBJ_ID,
            title="Non-Evaluative Concept",
            explanation_method=ExplanationMethod.TEXT_EXPLANATION,
            difficulty_level=1,
            language="en",
            blocks=[InstructionalBlock(id="b_1", block_type=ContentBlockType.TEXT, body="Pure learning")],
            summary="Just an explanation",
            status=InstructionalStatus.APPROVED,
            created_at=now,
            updated_at=now,
        )
        data = content.model_dump()
        assert "score" not in data
        assert "is_correct" not in data
        assert "pass_fail" not in data
        assert "mastery_achieved" not in data


# ── 2. Fallback Generation Tests (All 4 Methods) ────────────────────────────

class TestInstructionalFallbacks:
    """Verify deterministic fallback generation for all 4 MVP methods."""

    def test_fallback_visual_explanation(self):
        content = create_fallback_instructional_content(
            objective_id=MATH_OBJ_ID,
            objective_title="Counting Objects 1 to 5",
            method=ExplanationMethod.VISUAL_EXPLANATION,
            language="en",
        )
        assert content["explanation_method"] == ExplanationMethod.VISUAL_EXPLANATION
        block_types = [b["block_type"] for b in content["blocks"]]
        assert ContentBlockType.VISUAL_CUE.value in block_types
        assert ContentBlockType.TEXT.value in block_types
        assert content["summary"] is not None

    def test_fallback_step_by_step(self):
        content = create_fallback_instructional_content(
            objective_id=MATH_OBJ_ID,
            objective_title="Counting Step by Step",
            method=ExplanationMethod.STEP_BY_STEP,
            language="en",
        )
        assert content["explanation_method"] == ExplanationMethod.STEP_BY_STEP
        step_blocks = [b for b in content["blocks"] if b["block_type"] == ContentBlockType.STEP.value]
        assert len(step_blocks) >= 3

    def test_fallback_worked_example(self):
        content = create_fallback_instructional_content(
            objective_id=MATH_OBJ_ID,
            objective_title="Worked Example Counting",
            method=ExplanationMethod.WORKED_EXAMPLE,
            language="en",
        )
        assert content["explanation_method"] == ExplanationMethod.WORKED_EXAMPLE
        example_blocks = [b for b in content["blocks"] if b["block_type"] == ContentBlockType.WORKED_EXAMPLE.value]
        assert len(example_blocks) >= 1

    def test_fallback_text_explanation(self):
        content = create_fallback_instructional_content(
            objective_id=MATH_OBJ_ID,
            objective_title="Simple Text Counting",
            method=ExplanationMethod.TEXT_EXPLANATION,
            language="en",
        )
        assert content["explanation_method"] == ExplanationMethod.TEXT_EXPLANATION
        text_blocks = [b for b in content["blocks"] if b["block_type"] == ContentBlockType.TEXT.value]
        assert len(text_blocks) >= 2


# ── 3. Service Workflow & Status Transitions ────────────────────────────────

@pytest.mark.asyncio
class TestInstructionalServiceWorkflow:
    """Test generation, editing, approval, and publishing state machine."""

    async def test_generation_sets_review_required(self):
        session = AsyncMock()
        service = InstructionalService(session=session)

        # Mock objective lookup
        obj = LearningObjective(
            id=MATH_OBJ_ID,
            lesson_id=uuid.uuid4(),
            title={"en": "Counting 1 to 5"},
            difficulty_level=1,
            order_index=1,
        )
        mock_res = MagicMock()
        mock_res.scalars.return_value.first.return_value = obj
        session.execute.return_value = mock_res

        req = InstructionalGenerateRequest(
            objective_id=MATH_OBJ_ID,
            explanation_method=ExplanationMethod.VISUAL_EXPLANATION,
            language="en",
        )
        res = await service.generate(req, current_user=mock_teacher)

        assert res.content.status == InstructionalStatus.REVIEW_REQUIRED
        assert str(res.content.objective_id) == str(MATH_OBJ_ID)
        assert len(res.content.blocks) >= 2

    async def test_teacher_approval_and_publishing_transitions(self):
        session = AsyncMock()
        service = InstructionalService(session=session)
        content_id = uuid.uuid4()

        # Existing record in review_required
        record = InstructionalContent(
            id=content_id,
            objective_id=MATH_OBJ_ID,
            title="Initial Title",
            explanation_method=ExplanationMethod.STEP_BY_STEP.value,
            difficulty_level=1,
            language="en",
            blocks=[{"id": "b1", "block_type": "text", "body": "Initial step"}],
            summary="Initial summary",
            status=InstructionalStatus.REVIEW_REQUIRED.value,
            created_at=now,
            updated_at=now,
        )

        mock_res = MagicMock()
        mock_res.scalars.return_value.first.return_value = record
        session.execute.return_value = mock_res

        # 1. Teacher edits content
        update_data = InstructionalContentUpdate(
            title="Teacher Edited Title",
            summary="Teacher Edited Summary",
        )
        updated = await service.update(content_id, update_data, current_user=mock_teacher)
        assert updated.title == "Teacher Edited Title"
        assert updated.status == InstructionalStatus.REVIEW_REQUIRED

        # 2. Teacher approves content
        approved = await service.approve(content_id, current_user=mock_teacher)
        assert approved.status == InstructionalStatus.APPROVED

        # 3. Teacher publishes content
        published = await service.publish(content_id, current_user=mock_teacher)
        assert published.status == InstructionalStatus.PUBLISHED


# ── 4. API & Learner Visibility Rules ───────────────────────────────────────

class TestInstructionalApiVisibility:
    """Ensure learners cannot see unpublished (review_required / draft) content."""

    def test_learner_cannot_see_review_required_content_by_id(self):
        content_id = uuid.uuid4()
        record = InstructionalContent(
            id=content_id,
            objective_id=MATH_OBJ_ID,
            title="Unpublished Draft",
            explanation_method="visual_explanation",
            difficulty_level=1,
            language="en",
            blocks=[{"id": "b1", "block_type": "text", "body": "Draft"}],
            summary="Draft summary",
            status=InstructionalStatus.REVIEW_REQUIRED.value,
            created_at=now,
            updated_at=now,
        )

        mock_session = AsyncMock()
        mock_res = MagicMock()
        mock_res.scalars.return_value.first.return_value = record
        mock_session.execute.return_value = mock_res

        app.dependency_overrides[get_db_session] = lambda: mock_session

        # Learner attempts to get unpublished content by ID -> 404
        response = client.get(f"/api/v1/instructional-content/{content_id}")
        assert response.status_code == 404

    def test_teacher_can_see_review_required_content_by_id(self):
        content_id = uuid.uuid4()
        record = InstructionalContent(
            id=content_id,
            objective_id=MATH_OBJ_ID,
            title="Draft in Review",
            explanation_method="visual_explanation",
            difficulty_level=1,
            language="en",
            blocks=[{"id": "b1", "block_type": "text", "body": "Draft in Review"}],
            summary="Draft summary",
            status=InstructionalStatus.REVIEW_REQUIRED.value,
            created_at=now,
            updated_at=now,
        )

        mock_session = AsyncMock()
        async def mock_exec(stmt, *args, **kwargs):
            res = MagicMock()
            if "FROM users" in str(stmt):
                res.scalars.return_value.first.return_value = mock_teacher
            else:
                res.scalars.return_value.first.return_value = record
                res.scalars.return_value.all.return_value = [record]
            return res

        mock_session.execute.side_effect = mock_exec
        app.dependency_overrides[get_db_session] = lambda: mock_session

        response = client.get(
            f"/api/v1/instructional-content/{content_id}",
            headers=teacher_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Draft in Review"
        assert data["status"] == "review_required"

    def test_learner_can_see_published_content(self):
        content_id = uuid.uuid4()
        record = InstructionalContent(
            id=content_id,
            objective_id=MATH_OBJ_ID,
            title="Published Lesson",
            explanation_method="visual_explanation",
            difficulty_level=1,
            language="en",
            blocks=[{"id": "b1", "block_type": "text", "body": "Published explanation"}],
            summary="Ready for learners",
            status=InstructionalStatus.PUBLISHED.value,
            created_at=now,
            updated_at=now,
        )

        mock_session = AsyncMock()
        mock_res = MagicMock()
        mock_res.scalars.return_value.first.return_value = record
        mock_res.scalars.return_value.all.return_value = [record]
        mock_session.execute.return_value = mock_res

        app.dependency_overrides[get_db_session] = lambda: mock_session

        response = client.get(f"/api/v1/instructional-content/objective/{MATH_OBJ_ID}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Published Lesson"
        assert data[0]["status"] == "published"
