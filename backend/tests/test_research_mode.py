"""
Eduvia — Research Mode & Sandbox Verification Test Suite

Comprehensive tests for:
1. Researcher Role, Permissions & Access Control (Researcher vs Admin vs Teacher vs Learner).
2. Critical RAG & Production Isolation Boundary (Zero RAG, Zero Content Bank, Zero Phase 8, Zero Learner Context).
3. Project, Experiment, Variant, and Run Lineage & Cloning.
4. Prompt Studio Generation (Raw output preservation, structured normalization, failure safety).
5. Multi-Question & Mixed-Modality Experimentation.
6. Optional Production Compatibility Validation & Governance Promotion.
7. Custom Metrics, Evaluations & Side-by-Side Comparison.
8. IDOR & Multi-Tenant Researcher Isolation.
"""
from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.ai.providers.base import LLMResponse
from app.auth.dependencies import get_current_active_researcher, get_current_user
from app.auth.permissions import (
    ROLE_PERMISSIONS,
    Permission,
    has_permission,
)
from app.core.config import settings
from app.database.session import get_db_session
from app.main import app
from app.research.catalog import SUPPORTED_RESEARCH_MODELS, SUPPORTED_RESEARCH_MODEL_IDS
from app.research.generation import ResearchGenerationService, validate_production_compatibility
from app.research.models import (
    ResearchArtifact,
    ResearchEvaluation,
    ResearchExperiment,
    ResearchMetric,
    ResearchProject,
    ResearchRun,
    ResearchVariant,
)
from app.research.router import get_research_service
from app.research.schemas import (
    ArtifactPromotionRequest,
    ExperimentComparisonResponse,
    ResearchArtifactRead,
    ResearchEvaluationCreate,
    ResearchExperimentCreate,
    ResearchGenerationRequest,
    ResearchMetricCreate,
    ResearchProjectCreate,
    ResearchProjectRead,
    ResearchRunRead,
    ResearchVariantCreate,
    ResearchVariantRead,
    RunCloneRequest,
    VariantCloneRequest,
    VariantComparisonItem,
)
from app.research.service import ResearchService
from app.users.models import User, UserRole

client = TestClient(app)

# ── Fixtures ──────────────────────────────────────────────────────────────────
RESEARCHER_A_ID = uuid.uuid4()
RESEARCHER_B_ID = uuid.uuid4()
ADMIN_ID = uuid.uuid4()
TEACHER_ID = uuid.uuid4()
LEARNER_ID = uuid.uuid4()

now = datetime.now(UTC)

researcher_a = User(
    id=RESEARCHER_A_ID,
    email="researcher_a@eduvia.app",
    full_name="Dr. Alpha Researcher",
    hashed_password="hashed_pw",
    role=UserRole.researcher,
    is_active=True,
    created_at=now,
    updated_at=now,
)

researcher_b = User(
    id=RESEARCHER_B_ID,
    email="researcher_b@eduvia.app",
    full_name="Dr. Beta Researcher",
    hashed_password="hashed_pw",
    role=UserRole.researcher,
    is_active=True,
    created_at=now,
    updated_at=now,
)

admin_user = User(
    id=ADMIN_ID,
    email="admin@eduvia.app",
    full_name="Platform Admin",
    hashed_password="hashed_pw",
    role=UserRole.admin,
    is_active=True,
    created_at=now,
    updated_at=now,
)

teacher_user = User(
    id=TEACHER_ID,
    email="teacher@eduvia.app",
    full_name="Class Teacher",
    hashed_password="hashed_pw",
    role=UserRole.teacher,
    is_active=True,
    created_at=now,
    updated_at=now,
)

learner_user = User(
    id=LEARNER_ID,
    email="learner@eduvia.app",
    full_name="Student Learner",
    hashed_password="hashed_pw",
    role=UserRole.learner,
    is_active=True,
    created_at=now,
    updated_at=now,
)


@pytest.fixture(autouse=True)
def setup_dependencies():
    mock_session = AsyncMock()
    app.dependency_overrides[get_db_session] = lambda: mock_session
    yield
    app.dependency_overrides.clear()


# ==============================================================================
# 1. Researcher Role, Permissions & Access Control
# ==============================================================================

class TestResearcherRoleAndPermissions:
    """Verify role extension, permission matrix, and route guards."""

    def test_researcher_role_enum_value(self) -> None:
        assert UserRole.researcher == "researcher"

    def test_researcher_permissions_matrix(self) -> None:
        perms = ROLE_PERMISSIONS[UserRole.researcher]
        assert Permission.RESEARCH_WORKSPACE_READ in perms
        assert Permission.RESEARCH_PROJECT_CREATE in perms
        assert Permission.RESEARCH_PROJECT_READ_OWN in perms
        assert Permission.RESEARCH_EXPERIMENT_CREATE in perms
        assert Permission.RESEARCH_VARIANT_CREATE in perms
        assert Permission.RESEARCH_RUN_CREATE in perms
        assert Permission.RESEARCH_COMPARE in perms
        assert Permission.RESEARCH_EXPORT in perms
        # Researcher must NOT have administrative powers
        assert Permission.USERS_MANAGE not in perms
        assert Permission.ROLES_MANAGE not in perms
        assert Permission.ADMIN_DASHBOARD not in perms
        assert Permission.RESEARCH_PROMOTE not in perms

    def test_admin_has_global_research_access(self) -> None:
        admin_perms = ROLE_PERMISSIONS[UserRole.admin]
        assert Permission.RESEARCH_WORKSPACE_READ in admin_perms
        assert Permission.RESEARCH_PROMOTE in admin_perms

    def test_teacher_and_learner_denied_research_workspace(self) -> None:
        assert not has_permission(teacher_user, Permission.RESEARCH_WORKSPACE_READ)
        assert not has_permission(learner_user, Permission.RESEARCH_WORKSPACE_READ)

    def test_route_access_guard(self) -> None:
        # Mock research service for list_projects
        mock_service = AsyncMock()
        mock_service.list_projects.return_value = []
        app.dependency_overrides[get_research_service] = lambda: mock_service

        # Researcher: 200 OK
        app.dependency_overrides[get_current_user] = lambda: researcher_a
        resp = client.get("/api/v1/research/projects")
        assert resp.status_code == 200

        # Admin: 200 OK
        app.dependency_overrides[get_current_user] = lambda: admin_user
        resp = client.get("/api/v1/research/projects")
        assert resp.status_code == 200

        # Teacher: 403 Forbidden
        app.dependency_overrides[get_current_user] = lambda: teacher_user
        resp = client.get("/api/v1/research/projects")
        assert resp.status_code == 403

        # Learner: 403 Forbidden
        app.dependency_overrides[get_current_user] = lambda: learner_user
        resp = client.get("/api/v1/research/projects")
        assert resp.status_code == 403


# ==============================================================================
# 2. Critical RAG & Production Boundary Test (MANDATORY REQUIREMENT)
# ==============================================================================

class TestCriticalRAGAndProductionBoundary:
    """
    Mandatory architectural regression test proving that Research Generation
    does NOT invoke RAG, Qdrant, Content Bank, Curriculum, Learner Profile,
    or Phase 8 Adaptive Engine.
    """

    @pytest.mark.asyncio
    async def test_research_generation_does_not_call_production_pipelines(self) -> None:
        mock_provider = AsyncMock()
        mock_provider.generate.return_value = LLMResponse(
            content=json.dumps({"experiment_result": "Pure research sandbox test"}),
            model="gemini-2.5-flash",
            provider="gemini",
            usage={"input_tokens": 20, "output_tokens": 15},
        )

        gen_service = ResearchGenerationService(provider=mock_provider)

        # Track that production components are never imported or invoked
        with patch("app.knowledge.retrieval.KnowledgeRetrievalService.retrieve_pedagogical_context", AsyncMock()) as mock_rag, \
             patch("app.content.bank.ContentBank.get_items_for_objective", MagicMock()) as mock_bank, \
             patch("app.ai.adaptation.engine.AdaptationEngine.build_recommendation", MagicMock()) as mock_phase8, \
             patch("app.learners.service.LearnerService.get_by_id", AsyncMock()) as mock_learner_prof:

            result = await gen_service.execute_generation(
                prompt="Design a custom 12-question mixed assessment on spatial reasoning.",
                system_prompt="Custom experimental system prompt.",
                output_target="assessment",
                model="gemini-2.5-flash",
                model_configuration={"temperature": 0.5, "max_output_tokens": 3000},
                explicit_context={"manual_context": "Researcher provided manual notes."},
                production_compatibility_mode=False,
            )

            # Assert complete isolation
            assert mock_rag.call_count == 0, "RAG was called during Research generation!"
            assert mock_bank.call_count == 0, "Content Bank was called during Research generation!"
            assert mock_phase8.call_count == 0, "Phase 8 was called during Research generation!"
            assert mock_learner_prof.call_count == 0, "Learner Profile was called during Research generation!"

            # Assert output preservation
            assert result["status"] == "completed"
            assert result["normalized_output"] == {"experiment_result": "Pure research sandbox test"}
            assert result["is_production_compatible"] is False

            # Assert messages sent to Gemini contain ONLY researcher prompt and explicit context
            call_args = mock_provider.generate.call_args[0]
            messages = call_args[0]
            assert len(messages) == 2
            assert messages[0].content == "Custom experimental system prompt."
            assert "[Explicit Context]\nResearcher provided manual notes." in messages[1].content
            assert "Design a custom 12-question mixed assessment on spatial reasoning." in messages[1].content
            assert "VERIFIED PEDAGOGICAL KNOWLEDGE" not in messages[1].content


# ==============================================================================
# 3. Lineage, Variants & Cloning
# ==============================================================================

class TestProjectExperimentVariantLineage:
    """Verify relational lineage and clone operations."""

    @pytest.mark.asyncio
    async def test_variant_cloning_preserves_lineage(self) -> None:
        mock_session = AsyncMock()
        service = ResearchService(session=mock_session)

        exp_id = uuid.uuid4()
        orig_var_id = uuid.uuid4()
        project_id = uuid.uuid4()

        proj = ResearchProject(
            id=project_id,
            name="Curriculum Research",
            owner_id=RESEARCHER_A_ID,
            status="active",
        )
        exp = ResearchExperiment(
            id=exp_id,
            project_id=project_id,
            name="Pacing Test",
            status="active",
        )
        exp.project = proj

        orig_variant = ResearchVariant(
            id=orig_var_id,
            experiment_id=exp_id,
            name="Variant A: Fast Pacing",
            configuration={"pacing": "fast", "temperature": 0.3},
        )
        orig_variant.experiment = exp

        service.get_variant = AsyncMock(return_value=orig_variant)

        cloned = await service.clone_variant(
            user=researcher_a,
            variant_id=orig_var_id,
            req=VariantCloneRequest(
                new_name="Variant B: Slow Pacing",
                override_configuration={"pacing": "slow", "temperature": 0.8},
            ),
        )

        assert cloned.name == "Variant B: Slow Pacing"
        assert cloned.configuration["pacing"] == "slow"
        assert cloned.configuration["temperature"] == 0.8
        assert cloned.parent_variant_id == orig_var_id
        assert cloned.experiment_id == exp_id

    @pytest.mark.asyncio
    async def test_run_cloning_preserves_parent_run_id(self) -> None:
        mock_session = AsyncMock()
        service = ResearchService(session=mock_session)

        run_id = uuid.uuid4()
        orig_run = ResearchRun(
            id=run_id,
            variant_id=uuid.uuid4(),
            model="gemini-2.5-flash",
            model_configuration={"temperature": 0.4},
            user_prompt="Original Prompt",
            status="completed",
        )
        orig_run.variant = MagicMock()
        orig_run.variant.experiment.project.owner_id = RESEARCHER_A_ID

        service.get_run = AsyncMock(return_value=orig_run)

        cloned_run = await service.clone_run(
            user=researcher_a,
            run_id=run_id,
            req=RunCloneRequest(override_user_prompt="Overridden Prompt"),
        )

        assert cloned_run.parent_run_id == run_id
        assert cloned_run.user_prompt == "Overridden Prompt"
        assert cloned_run.model_configuration == {"temperature": 0.4}
        assert cloned_run.status == "draft"


# ==============================================================================
# 4. Multi-Question, Mixed-Modality & Raw Output Preservation
# ==============================================================================

class TestMultiQuestionAndMixedModalityResearch:
    """Verify research generation supports arbitrary question counts and formats."""

    @pytest.mark.asyncio
    async def test_large_question_count_preservation(self) -> None:
        """20-question custom assessment must not be rejected by production 3-10 limits."""
        twenty_questions = [
            {"id": f"q_{i}", "prompt": f"Question {i}?", "type": "multiple_choice" if i % 2 == 0 else "matching"}
            for i in range(1, 21)
        ]
        raw_llm_json = json.dumps({"assessment_title": "Mega Assessment", "questions": twenty_questions})

        mock_provider = AsyncMock()
        mock_provider.generate.return_value = LLMResponse(
            content=raw_llm_json,
            model="gemini-2.5-flash",
            provider="gemini",
        )

        gen_service = ResearchGenerationService(provider=mock_provider)
        result = await gen_service.execute_generation(
            prompt="Generate a 20 question comprehensive assessment.",
            output_target="assessment",
        )

        assert result["status"] == "completed"
        assert len(result["normalized_output"]["questions"]) == 20
        assert result["raw_output"] == raw_llm_json

    @pytest.mark.asyncio
    async def test_raw_output_preserved_when_not_valid_json(self) -> None:
        """Non-JSON freeform responses are preserved with raw_output without crashing."""
        raw_text = "Here is an unstructured lesson outline:\n1. Introduction\n2. Hands-on exploration\n3. Conclusion"
        mock_provider = AsyncMock()
        mock_provider.generate.return_value = LLMResponse(
            content=raw_text,
            model="gemini-2.5-flash",
            provider="gemini",
        )

        gen_service = ResearchGenerationService(provider=mock_provider)
        result = await gen_service.execute_generation(
            prompt="Freeform lesson draft",
            output_target="lesson_plan",
        )

        assert result["status"] == "completed_with_parse_warning"
        assert result["raw_output"] == raw_text
        assert result["normalized_output"]["text"] == raw_text
        assert result["normalized_output"]["format"] == "freeform"


# ==============================================================================
# 5. Production Compatibility & Promotion Governance
# ==============================================================================

class TestCompatibilityAndPromotion:
    """Verify optional compatibility validation and strict promotion governance."""

    def test_production_compatibility_validator_handles_invalid_gracefully(self) -> None:
        invalid_payload = {"some_random_field": "not an activity"}
        valid, report = validate_production_compatibility(invalid_payload, target_schema="activity")
        assert valid is False
        assert "errors" in report

    @pytest.mark.asyncio
    async def test_researcher_cannot_promote_artifact(self) -> None:
        mock_session = AsyncMock()
        service = ResearchService(session=mock_session)

        art_id = uuid.uuid4()
        with pytest.raises(Exception) as exc_info:
            await service.promote_artifact(
                user=researcher_a,
                artifact_id=art_id,
                req=ArtifactPromotionRequest(target_destination="activity"),
            )
        assert "Only administrators" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_admin_can_promote_compatible_artifact(self) -> None:
        mock_session = AsyncMock()
        service = ResearchService(session=mock_session)

        art_id = uuid.uuid4()
        artifact = ResearchArtifact(
            id=art_id,
            run_id=uuid.uuid4(),
            artifact_type="activity",
            payload={"valid": "content"},
            is_production_compatible=True,
            promoted_to_production=False,
            metadata_info={},
        )
        service.get_artifact = AsyncMock(return_value=artifact)

        response = await service.promote_artifact(
            user=admin_user,
            artifact_id=art_id,
            req=ArtifactPromotionRequest(target_destination="activity", notes="Approved for draft import"),
        )

        assert response.success is True
        assert artifact.promoted_to_production is True
        assert artifact.production_entity_id is not None
        assert response.destination == "activity"


# ==============================================================================
# 6. IDOR and Multi-Tenant Researcher Isolation
# ==============================================================================

class TestIDORAndIsolation:
    """Verify complete isolation between Researcher A and Researcher B."""

    @pytest.mark.asyncio
    async def test_researcher_b_cannot_access_researcher_a_project(self) -> None:
        mock_session = AsyncMock()
        service = ResearchService(session=mock_session)

        proj_id = uuid.uuid4()
        project = ResearchProject(
            id=proj_id,
            name="Alpha Project",
            owner_id=RESEARCHER_A_ID,
            status="active",
        )

        # Mock query return
        mock_result = MagicMock()
        mock_result.scalars().first.return_value = project
        mock_session.execute.return_value = mock_result

        # Researcher A: Success
        res_a = await service.get_project(user=researcher_a, project_id=proj_id)
        assert res_a.id == proj_id

        # Researcher B: Denied (IDOR blocked)
        with pytest.raises(Exception) as exc_info:
            await service.get_project(user=researcher_b, project_id=proj_id)
        assert "Access denied" in str(exc_info.value)

        # Admin: Global Visibility Allowed
        res_admin = await service.get_project(user=admin_user, project_id=proj_id)
        assert res_admin.id == proj_id


# ==============================================================================
# 7. Custom Metrics, Evaluations & Side-by-Side Comparison
# ==============================================================================

class TestEvaluationsAndComparison:
    """Verify metrics, evaluations, and side-by-side comparison without auto-ranking."""

    @pytest.mark.asyncio
    async def test_comparison_view_assembles_variants_and_evaluations(self) -> None:
        mock_session = AsyncMock()
        service = ResearchService(session=mock_session)

        exp_id = uuid.uuid4()
        exp = ResearchExperiment(
            id=exp_id,
            project_id=uuid.uuid4(),
            name="Visual vs Textual Scaffolding",
        )
        service.get_experiment = AsyncMock(return_value=exp)
        service.list_metrics = AsyncMock(return_value=[
            ResearchMetric(
                id=uuid.uuid4(),
                experiment_id=exp_id,
                name="Clarity",
                metric_type="rating",
                configuration={},
                created_at=now,
                updated_at=now,
            )
        ])

        # Mock variants query
        var_a = ResearchVariant(
            id=uuid.uuid4(),
            experiment_id=exp_id,
            name="Variant A",
            configuration={},
            metadata_info={},
            created_at=now,
            updated_at=now,
        )
        var_a.runs = []
        var_b = ResearchVariant(
            id=uuid.uuid4(),
            experiment_id=exp_id,
            name="Variant B",
            configuration={},
            metadata_info={},
            created_at=now,
            updated_at=now,
        )
        var_b.runs = []

        mock_var_result = MagicMock()
        mock_var_result.scalars().all.return_value = [var_a, var_b]
        mock_session.execute.return_value = mock_var_result

        comparison = await service.get_experiment_comparison(user=researcher_a, experiment_id=exp_id)

        assert comparison.experiment_id == exp_id
        assert len(comparison.variants) == 2
        assert len(comparison.metrics) == 1
        assert comparison.metrics[0].name == "Clarity"
        # Notice: No winner or auto-rank is returned! It is an evidence comparison workspace.


# ==============================================================================
# 8. Model Catalog, Resource Limits & Question Count Verification
# ==============================================================================

class TestModelCatalogAndLimits:
    """Verify supported model catalog, server-side resource limits, and question counts."""

    def test_selectable_models_exist_in_catalog(self) -> None:
        """Every selectable research model must exist in the supported model catalog."""
        assert len(SUPPORTED_RESEARCH_MODELS) >= 2
        for model in SUPPORTED_RESEARCH_MODELS:
            assert model["id"] in SUPPORTED_RESEARCH_MODEL_IDS
            assert "name" in model
            assert "description" in model

    def test_shut_down_and_obsolete_models_explicitly_rejected(self) -> None:
        """Explicit verification that gemini-2.0-flash-exp, gemini-1.5-pro, and arbitrary strings are rejected."""
        rejected_models = ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-2.0-flash", "arbitrary-custom-model"]
        for bad_model in rejected_models:
            with pytest.raises(Exception) as exc_info:
                ResearchGenerationRequest(
                    project_id=uuid.uuid4(),
                    experiment_id=uuid.uuid4(),
                    variant_id=uuid.uuid4(),
                    prompt="Valid prompt",
                    model=bad_model,
                )
            assert "not supported in Research Mode" in str(exc_info.value)

    def test_every_catalog_model_passes_validation(self) -> None:
        """Every model exposed by the catalog and GET /models passes validation."""
        assert len(SUPPORTED_RESEARCH_MODELS) == 4
        # Verify preferred models are present
        model_ids = {m["id"] for m in SUPPORTED_RESEARCH_MODELS}
        assert "gemini-3.8-flash" in model_ids
        assert "gemini-3.5-flash-lite" in model_ids
        assert "gemini-2.5-flash" in model_ids
        assert "gemini-2.5-pro" in model_ids

        # Verify each model can be instantiated in a generation request without error
        for model in SUPPORTED_RESEARCH_MODELS:
            req = ResearchGenerationRequest(
                project_id=uuid.uuid4(),
                experiment_id=uuid.uuid4(),
                variant_id=uuid.uuid4(),
                prompt="Valid research prompt",
                model=model["id"],
            )
            assert req.model == model["id"]

    def test_get_models_api_endpoint(self) -> None:
        """GET /api/v1/research/models returns the canonical catalog to authorized researchers."""
        app.dependency_overrides[get_current_active_researcher] = lambda: researcher_a
        try:
            res = client.get("/api/v1/research/models")
            assert res.status_code == 200
            data = res.json()
            assert len(data) == len(SUPPORTED_RESEARCH_MODELS)
            returned_ids = {item["id"] for item in data}
            assert returned_ids == SUPPORTED_RESEARCH_MODEL_IDS
            for item in data:
                # Every model from the endpoint passes server validation
                req = ResearchGenerationRequest(
                    project_id=uuid.uuid4(),
                    experiment_id=uuid.uuid4(),
                    variant_id=uuid.uuid4(),
                    prompt="Valid prompt",
                    model=item["id"],
                )
                assert req.model == item["id"]
        finally:
            app.dependency_overrides.pop(get_current_active_researcher, None)

    def test_prompt_length_limit_enforced(self) -> None:
        """Prompts exceeding MAX_RESEARCH_PROMPT_LENGTH must be rejected."""
        oversized_prompt = "A" * (settings.MAX_RESEARCH_PROMPT_LENGTH + 1)
        with pytest.raises(Exception):
            ResearchGenerationRequest(
                project_id=uuid.uuid4(),
                experiment_id=uuid.uuid4(),
                variant_id=uuid.uuid4(),
                prompt=oversized_prompt,
                model="gemini-2.5-flash",
            )

    def test_max_output_tokens_limit_enforced(self) -> None:
        """Tokens exceeding MAX_RESEARCH_OUTPUT_TOKENS must be rejected."""
        with pytest.raises(Exception) as exc_info:
            ResearchGenerationRequest(
                project_id=uuid.uuid4(),
                experiment_id=uuid.uuid4(),
                variant_id=uuid.uuid4(),
                prompt="Test prompt",
                model="gemini-2.5-flash",
                model_configuration={"max_output_tokens": settings.MAX_RESEARCH_OUTPUT_TOKENS + 1000},
            )
        assert "exceeds maximum allowed" in str(exc_info.value)

    def test_question_count_validation(self) -> None:
        """Research mode accepts 1, 5, 10, 20, 50 questions, rejecting > 50 or < 1."""
        for count in [1, 5, 10, 20, 50]:
            req = ResearchGenerationRequest(
                project_id=uuid.uuid4(),
                experiment_id=uuid.uuid4(),
                variant_id=uuid.uuid4(),
                prompt="Test prompt",
                model="gemini-2.5-flash",
                question_count=count,
            )
            assert req.question_count == count

        with pytest.raises(Exception):
            ResearchGenerationRequest(
                project_id=uuid.uuid4(),
                experiment_id=uuid.uuid4(),
                variant_id=uuid.uuid4(),
                prompt="Test prompt",
                model="gemini-2.5-flash",
                question_count=51,
            )

        with pytest.raises(Exception):
            ResearchGenerationRequest(
                project_id=uuid.uuid4(),
                experiment_id=uuid.uuid4(),
                variant_id=uuid.uuid4(),
                prompt="Test prompt",
                model="gemini-2.5-flash",
                question_count=0,
            )


# ==============================================================================
# 9. Actual Gemini Execution Path, Prompt Preservation & Provenance Audit
# ==============================================================================

class TestGeminiExecutionPathAndProvenance:
    """Verify Gemini execution path, prompt preservation, and provenance completeness."""

    @pytest.mark.asyncio
    async def test_gemini_execution_path_and_preservation(self) -> None:
        """Mock Gemini provider and verify model, exact prompt, context, and system instructions."""
        mock_provider = AsyncMock()
        mock_provider.generate.return_value = LLMResponse(
            content='{"result": "success", "data": "sandbox output"}',
            model="gemini-2.5-pro",
            provider="gemini",
        )

        gen_service = ResearchGenerationService(provider=mock_provider)
        exact_prompt = "Generate a formative diagnostic assessment on photosynthesis."
        custom_sys = "You are a specialized biology education researcher."
        manual_context = "Photosynthesis occurs in chloroplasts via light-dependent and light-independent reactions."

        result = await gen_service.execute_generation(
            prompt=exact_prompt,
            system_prompt=custom_sys,
            model="gemini-2.5-pro",
            model_configuration={"temperature": 0.3, "max_output_tokens": 4096},
            explicit_context={"manual_context": manual_context},
            output_target="assessment",
            question_count=10,
        )

        # 1. Provider is called exactly once
        assert mock_provider.generate.call_count == 1
        call_args = mock_provider.generate.call_args
        messages, config = call_args[0]

        # 2. Correct model passed in GenerationConfig
        assert config.model == "gemini-2.5-pro"
        assert config.temperature == 0.3
        assert config.max_tokens == 4096

        # 3. Exact researcher prompt is preserved in user message
        user_msg = [m for m in messages if m.role == "user"][0]
        assert exact_prompt in user_msg.content
        assert manual_context in user_msg.content
        assert "Target count: 10 questions" in user_msg.content

        # 4. Research-specific system instructions passed
        sys_msg = [m for m in messages if m.role == "system"][0]
        assert sys_msg.content == custom_sys

        # 5. Result preserves raw and normalized output
        assert result["status"] == "completed"
        assert result["raw_output"] == '{"result": "success", "data": "sandbox output"}'
        assert result["normalized_output"]["result"] == "success"

    @pytest.mark.asyncio
    async def test_provenance_completeness(self) -> None:
        """Verify full lineage and execution parameters can be reconstructed from a run."""
        mock_session = AsyncMock()
        mock_provider = AsyncMock()
        mock_provider.generate.return_value = LLMResponse(
            content='{"assessment": "complete"}',
            model="gemini-2.5-flash",
            provider="gemini",
        )

        gen_service = ResearchGenerationService(provider=mock_provider)
        service = ResearchService(session=mock_session, generation_service=gen_service)

        project_id = uuid.uuid4()
        experiment_id = uuid.uuid4()
        variant_id = uuid.uuid4()

        variant = ResearchVariant(
            id=variant_id,
            experiment_id=experiment_id,
            name="Variant Lineage Test",
            configuration={"temperature": 0.5},
            metadata_info={},
        )
        variant.experiment = MagicMock()
        variant.experiment.project_id = project_id
        variant.experiment.project.owner_id = RESEARCHER_A_ID
        service.get_variant = AsyncMock(return_value=variant)

        req = ResearchGenerationRequest(
            project_id=project_id,
            experiment_id=experiment_id,
            variant_id=variant_id,
            prompt="Analyze cognitive load of multi-step word problems.",
            system_prompt="Custom sandbox instructions.",
            model="gemini-2.5-flash",
            model_configuration={"temperature": 0.5, "max_output_tokens": 2048},
            explicit_context={"manual_context": "Sample word problem text."},
            question_count=5,
            output_target="assessment",
        )

        run = await service.execute_run(user=researcher_a, req=req)

        # Provenance verification
        assert run.user_prompt == req.prompt
        assert run.system_prompt == req.system_prompt
        assert run.model == "gemini-2.5-flash"
        assert run.model_configuration == {"temperature": 0.5, "max_output_tokens": 2048}
        assert run.input_snapshot["explicit_context"] == {"manual_context": "Sample word problem text."}
        assert run.input_snapshot["question_count"] == 5
        assert run.input_snapshot["project_id"] == str(project_id)
        assert run.input_snapshot["experiment_id"] == str(experiment_id)
        assert run.input_snapshot["variant_id"] == str(variant_id)
        assert run.raw_output == '{"assessment": "complete"}'
        assert run.status == "completed"
        assert run.started_at is not None
        assert run.completed_at is not None

        # Verify no sensitive data leaked into run or input_snapshot
        snapshot_str = json.dumps(run.input_snapshot)
        assert "password" not in snapshot_str
        assert "secret" not in snapshot_str
        assert "token" not in snapshot_str
        assert "api_key" not in snapshot_str

    @pytest.mark.asyncio
    async def test_mixed_modality_assessment_safe_preservation(self) -> None:
        """5-question mixed modality assessment preserves experimental structure safely."""
        mixed_payload = {
            "title": "Mixed Modality Diagnostic",
            "questions": [
                {"number": 1, "type": "multiple_choice", "prompt": "Identify the noun."},
                {"number": 2, "type": "matching", "prompt": "Match words to synonyms."},
                {"number": 3, "type": "ordering", "prompt": "Order steps chronologically."},
                {"number": 4, "type": "visual_identification", "prompt": "Identify the shaded region."},
                {"number": 5, "type": "drag_drop", "prompt": "Categorize items into bins."},
            ],
        }
        raw_text = json.dumps(mixed_payload)
        mock_provider = AsyncMock()
        mock_provider.generate.return_value = LLMResponse(
            content=raw_text,
            model="gemini-2.5-flash",
            provider="gemini",
        )

        gen_service = ResearchGenerationService(provider=mock_provider)
        result = await gen_service.execute_generation(
            prompt="Generate a 5-question mixed modality assessment.",
            output_target="assessment",
        )

        assert result["status"] == "completed"
        questions = result["normalized_output"]["questions"]
        assert len(questions) == 5
        types = [q["type"] for q in questions]
        assert types == ["multiple_choice", "matching", "ordering", "visual_identification", "drag_drop"]
        assert result["raw_output"] == raw_text


# ==============================================================================
# 10. Artifact Cardinality & Failure Handling Invariants
# ==============================================================================

class TestArtifactCardinalityAndFailureHandling:
    """
    Verify ResearchRun -> ResearchArtifact = 1:1 maximum.
    - Successful run creates at most one artifact.
    - Failed run creates zero artifacts.
    - Duplicate artifact creation for the same run is prevented by schema constraint.
    """

    @pytest.mark.asyncio
    async def test_successful_run_creates_at_most_one_artifact(self) -> None:
        mock_session = AsyncMock()
        mock_provider = AsyncMock()
        mock_provider.generate.return_value = LLMResponse(
            content='{"activity": "test content"}',
            model="gemini-3.8-flash",
            provider="gemini",
        )

        gen_service = ResearchGenerationService(provider=mock_provider)
        service = ResearchService(session=mock_session, generation_service=gen_service)

        project_id = uuid.uuid4()
        experiment_id = uuid.uuid4()
        variant_id = uuid.uuid4()

        variant = ResearchVariant(
            id=variant_id,
            experiment_id=experiment_id,
            name="Variant Cardinality Test",
            configuration={},
            metadata_info={},
        )
        variant.experiment = MagicMock()
        variant.experiment.project_id = project_id
        variant.experiment.project.owner_id = RESEARCHER_A_ID
        service.get_variant = AsyncMock(return_value=variant)

        req = ResearchGenerationRequest(
            project_id=project_id,
            experiment_id=experiment_id,
            variant_id=variant_id,
            prompt="Generate a test activity",
            model="gemini-3.8-flash",
        )

        run = await service.execute_run(user=researcher_a, req=req)

        assert run.status == "completed"
        added_artifacts = [
            call.args[0] for call in mock_session.add.call_args_list
            if isinstance(call.args[0], ResearchArtifact)
        ]
        assert len(added_artifacts) == 1
        assert added_artifacts[0].run_id == run.id

    @pytest.mark.asyncio
    async def test_failed_run_creates_zero_artifacts(self) -> None:
        mock_session = AsyncMock()
        mock_provider = AsyncMock()
        mock_provider.generate.side_effect = Exception("API key invalid or network error")

        gen_service = ResearchGenerationService(provider=mock_provider)
        service = ResearchService(session=mock_session, generation_service=gen_service)

        project_id = uuid.uuid4()
        experiment_id = uuid.uuid4()
        variant_id = uuid.uuid4()

        variant = ResearchVariant(
            id=variant_id,
            experiment_id=experiment_id,
            name="Variant Failure Test",
            configuration={},
            metadata_info={},
        )
        variant.experiment = MagicMock()
        variant.experiment.project_id = project_id
        variant.experiment.project.owner_id = RESEARCHER_A_ID
        service.get_variant = AsyncMock(return_value=variant)

        req = ResearchGenerationRequest(
            project_id=project_id,
            experiment_id=experiment_id,
            variant_id=variant_id,
            prompt="Prompt to test failure handling",
            model="gemini-3.8-flash",
        )

        run = await service.execute_run(user=researcher_a, req=req)

        assert run.status == "failed"
        assert run.error is not None
        assert "API key invalid or network error" in run.error
        assert run.user_prompt == req.prompt

        added_artifacts = [
            call.args[0] for call in mock_session.add.call_args_list
            if isinstance(call.args[0], ResearchArtifact)
        ]
        assert len(added_artifacts) == 0

    def test_duplicate_artifact_prevented_by_schema_constraints(self) -> None:
        """Database schema strictly prevents more than one artifact per run."""
        from app.research.models import ResearchArtifact, ResearchRun
        run_id_col = ResearchArtifact.__table__.columns["run_id"]
        assert run_id_col.unique is True
        assert ResearchRun.artifact.property.uselist is False

