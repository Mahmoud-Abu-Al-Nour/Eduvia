"""
Eduvia — Research Mode API Router

Dedicated API routes for educational research and sandbox experimentation.
Only accessible to authorized Researchers and Administrators with research permissions.
Strictly isolated from Production curriculum, RAG, and Learner profiles.
"""
from __future__ import annotations

import uuid
from typing import Any

import structlog
from fastapi import APIRouter, Body, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_active_researcher
from app.database.session import get_db_session
from app.research.catalog import SUPPORTED_RESEARCH_MODELS
from app.research.schemas import (
    ArtifactExportRequest,
    ArtifactPromotionRequest,
    ArtifactPromotionResponse,
    ExperimentComparisonResponse,
    ResearchArtifactRead,
    ResearchEvaluationCreate,
    ResearchEvaluationRead,
    ResearchExperimentCreate,
    ResearchExperimentRead,
    ResearchExperimentUpdate,
    ResearchGenerationRequest,
    ResearchMetricCreate,
    ResearchMetricRead,
    ResearchModelInfo,
    ResearchProjectCreate,
    ResearchProjectRead,
    ResearchProjectUpdate,
    ResearchRunRead,
    ResearchSnapshotCreate,
    ResearchSnapshotRead,
    ResearchVariantCreate,
    ResearchVariantRead,
    ResearchVariantUpdate,
    RunCloneRequest,
    VariantCloneRequest,
)
from app.research.service import ResearchService
from app.users.models import User

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/research", tags=["research"])


def get_research_service(session: AsyncSession = Depends(get_db_session)) -> ResearchService:
    return ResearchService(session=session)


# ---------------------------------------------------------------------------
# Supported Models Catalog
# ---------------------------------------------------------------------------

@router.get("/models", response_model=list[ResearchModelInfo])
async def list_supported_research_models(
    current_user: User = Depends(get_current_active_researcher),
) -> list[ResearchModelInfo]:
    """List canonical supported AI models for Research Sandbox."""
    return [ResearchModelInfo.model_validate(m) for m in SUPPORTED_RESEARCH_MODELS]


# ---------------------------------------------------------------------------
# Research Projects
# ---------------------------------------------------------------------------

@router.get("/projects", response_model=list[ResearchProjectRead])
async def list_projects(
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> list[ResearchProjectRead]:
    """List research projects owned by the researcher (or all projects for admins)."""
    projects = await service.list_projects(current_user)
    return [ResearchProjectRead.model_validate(p) for p in projects]


@router.post("/projects", response_model=ResearchProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ResearchProjectCreate,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchProjectRead:
    """Create a new research project isolated to the authenticated researcher."""
    project = await service.create_project(current_user, data)
    return ResearchProjectRead.model_validate(project)


@router.get("/projects/{project_id}", response_model=ResearchProjectRead)
async def get_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchProjectRead:
    """Retrieve details for a specific research project."""
    project = await service.get_project(current_user, project_id)
    return ResearchProjectRead.model_validate(project)


@router.patch("/projects/{project_id}", response_model=ResearchProjectRead)
async def update_project(
    project_id: uuid.UUID,
    data: ResearchProjectUpdate,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchProjectRead:
    """Update research project metadata."""
    project = await service.update_project(current_user, project_id, data)
    return ResearchProjectRead.model_validate(project)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> None:
    """Delete a research project and its child experiments."""
    await service.delete_project(current_user, project_id)


# ---------------------------------------------------------------------------
# Research Experiments
# ---------------------------------------------------------------------------

@router.get("/projects/{project_id}/experiments", response_model=list[ResearchExperimentRead])
async def list_experiments(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> list[ResearchExperimentRead]:
    """List experiments in a project."""
    experiments = await service.list_experiments(current_user, project_id)
    return [ResearchExperimentRead.model_validate(e) for e in experiments]


@router.post(
    "/projects/{project_id}/experiments",
    response_model=ResearchExperimentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_experiment(
    project_id: uuid.UUID,
    data: ResearchExperimentCreate,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchExperimentRead:
    """Create a new experiment within a research project."""
    experiment = await service.create_experiment(current_user, project_id, data)
    return ResearchExperimentRead.model_validate(experiment)


@router.get("/experiments/{experiment_id}", response_model=ResearchExperimentRead)
async def get_experiment(
    experiment_id: uuid.UUID,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchExperimentRead:
    """Get experiment details."""
    experiment = await service.get_experiment(current_user, experiment_id)
    return ResearchExperimentRead.model_validate(experiment)


@router.patch("/experiments/{experiment_id}", response_model=ResearchExperimentRead)
async def update_experiment(
    experiment_id: uuid.UUID,
    data: ResearchExperimentUpdate,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchExperimentRead:
    """Update experiment metadata."""
    experiment = await service.update_experiment(current_user, experiment_id, data)
    return ResearchExperimentRead.model_validate(experiment)


@router.delete("/experiments/{experiment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experiment(
    experiment_id: uuid.UUID,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> None:
    """Delete an experiment."""
    await service.delete_experiment(current_user, experiment_id)


# ---------------------------------------------------------------------------
# Research Variants
# ---------------------------------------------------------------------------

@router.get("/experiments/{experiment_id}/variants", response_model=list[ResearchVariantRead])
async def list_variants(
    experiment_id: uuid.UUID,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> list[ResearchVariantRead]:
    """List variants defined for an experiment."""
    variants = await service.list_variants(current_user, experiment_id)
    return [ResearchVariantRead.model_validate(v) for v in variants]


@router.post(
    "/experiments/{experiment_id}/variants",
    response_model=ResearchVariantRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_variant(
    experiment_id: uuid.UUID,
    data: ResearchVariantCreate,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchVariantRead:
    """Create a new experimental variant."""
    variant = await service.create_variant(current_user, experiment_id, data)
    return ResearchVariantRead.model_validate(variant)


@router.get("/variants/{variant_id}", response_model=ResearchVariantRead)
async def get_variant(
    variant_id: uuid.UUID,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchVariantRead:
    """Get variant details."""
    variant = await service.get_variant(current_user, variant_id)
    return ResearchVariantRead.model_validate(variant)


@router.patch("/variants/{variant_id}", response_model=ResearchVariantRead)
async def update_variant(
    variant_id: uuid.UUID,
    data: ResearchVariantUpdate,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchVariantRead:
    """Update variant configuration."""
    variant = await service.update_variant(current_user, variant_id, data)
    return ResearchVariantRead.model_validate(variant)


@router.post(
    "/variants/{variant_id}/clone",
    response_model=ResearchVariantRead,
    status_code=status.HTTP_201_CREATED,
)
async def clone_variant(
    variant_id: uuid.UUID,
    req: VariantCloneRequest,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchVariantRead:
    """Clone an existing variant, retaining parent lineage."""
    cloned = await service.clone_variant(current_user, variant_id, req)
    return ResearchVariantRead.model_validate(cloned)


# ---------------------------------------------------------------------------
# Prompt Studio & Runs
# ---------------------------------------------------------------------------

@router.post("/prompt-studio/generate", response_model=ResearchRunRead, status_code=status.HTTP_201_CREATED)
async def generate_prompt_studio(
    req: ResearchGenerationRequest,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchRunRead:
    """
    Direct Prompt Studio generation.
    Sends raw prompt + explicit config to Gemini without production RAG or Phase 8.
    Creates and returns a ResearchRun with resulting ResearchArtifact.
    """
    run = await service.execute_run(current_user, req)
    return ResearchRunRead.model_validate(run)


@router.get("/runs/{run_id}", response_model=ResearchRunRead)
async def get_run(
    run_id: uuid.UUID,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchRunRead:
    """Retrieve full details of a research execution run."""
    run = await service.get_run(current_user, run_id)
    return ResearchRunRead.model_validate(run)


@router.post("/runs/{run_id}/clone", response_model=ResearchRunRead, status_code=status.HTTP_201_CREATED)
async def clone_run(
    run_id: uuid.UUID,
    req: RunCloneRequest,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchRunRead:
    """Clone an execution run with optional prompt or configuration overrides."""
    cloned = await service.clone_run(current_user, run_id, req)
    return ResearchRunRead.model_validate(cloned)


# ---------------------------------------------------------------------------
# Research Artifacts & Promotion
# ---------------------------------------------------------------------------

@router.get("/artifacts/{artifact_id}", response_model=ResearchArtifactRead)
async def get_artifact(
    artifact_id: uuid.UUID,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchArtifactRead:
    """Retrieve a research artifact."""
    artifact = await service.get_artifact(current_user, artifact_id)
    return ResearchArtifactRead.model_validate(artifact)


# ---------------------------------------------------------------------------
# Metrics & Evaluations
# ---------------------------------------------------------------------------

@router.post(
    "/experiments/{experiment_id}/metrics",
    response_model=ResearchMetricRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_metric(
    experiment_id: uuid.UUID,
    data: ResearchMetricCreate,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchMetricRead:
    """Define a custom research evaluation metric for an experiment."""
    metric = await service.create_metric(current_user, experiment_id, data)
    return ResearchMetricRead.model_validate(metric)


@router.get("/experiments/{experiment_id}/metrics", response_model=list[ResearchMetricRead])
async def list_metrics(
    experiment_id: uuid.UUID,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> list[ResearchMetricRead]:
    """List metrics for an experiment."""
    metrics = await service.list_metrics(current_user, experiment_id)
    return [ResearchMetricRead.model_validate(m) for m in metrics]


@router.post(
    "/artifacts/{artifact_id}/evaluations",
    response_model=ResearchEvaluationRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_evaluation(
    artifact_id: uuid.UUID,
    data: ResearchEvaluationCreate,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchEvaluationRead:
    """Record a researcher or deterministic evaluation against a generated artifact."""
    evaluation = await service.create_evaluation(current_user, artifact_id, data)
    return ResearchEvaluationRead.model_validate(evaluation)


@router.get("/artifacts/{artifact_id}/evaluations", response_model=list[ResearchEvaluationRead])
async def list_evaluations(
    artifact_id: uuid.UUID,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> list[ResearchEvaluationRead]:
    """List all evaluations scored on an artifact."""
    evaluations = await service.list_evaluations(current_user, artifact_id)
    return [ResearchEvaluationRead.model_validate(e) for e in evaluations]


# ---------------------------------------------------------------------------
# Side-by-Side Comparison
# ---------------------------------------------------------------------------

@router.get("/experiments/{experiment_id}/compare", response_model=ExperimentComparisonResponse)
async def compare_experiment_variants(
    experiment_id: uuid.UUID,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ExperimentComparisonResponse:
    """
    Side-by-side comparison across all variants of an experiment.
    Presents prompts, outputs, artifacts, metrics, and evaluations without declaring a winner.
    """
    return await service.get_experiment_comparison(current_user, experiment_id)


# ---------------------------------------------------------------------------
# Snapshots
# ---------------------------------------------------------------------------

@router.post(
    "/projects/{project_id}/snapshots",
    response_model=ResearchSnapshotRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_snapshot(
    project_id: uuid.UUID,
    data: ResearchSnapshotCreate,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ResearchSnapshotRead:
    """Create an immutable snapshot of production data for research reference."""
    snapshot = await service.create_snapshot(current_user, project_id, data)
    return ResearchSnapshotRead.model_validate(snapshot)


@router.get("/projects/{project_id}/snapshots", response_model=list[ResearchSnapshotRead])
async def list_snapshots(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> list[ResearchSnapshotRead]:
    """List snapshots in a project."""
    snapshots = await service.list_snapshots(current_user, project_id)
    return [ResearchSnapshotRead.model_validate(s) for s in snapshots]


# ---------------------------------------------------------------------------
# Artifact Export & Promotion
# ---------------------------------------------------------------------------

@router.post("/artifacts/{artifact_id}/export")
async def export_artifact(
    artifact_id: uuid.UUID,
    format: str | None = Query(None),
    req: ArtifactExportRequest | None = Body(None),
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> dict[str, Any]:
    """Export an artifact as structured JSON or Markdown document."""
    chosen_format = "json"
    if format:
        chosen_format = format
    elif req and getattr(req, "format", None):
        chosen_format = req.format
    return await service.export_artifact(current_user, artifact_id, export_format=chosen_format)


@router.post("/artifacts/{artifact_id}/promote", response_model=ArtifactPromotionResponse)
async def promote_artifact(
    artifact_id: uuid.UUID,
    req: ArtifactPromotionRequest,
    current_user: User = Depends(get_current_active_researcher),
    service: ResearchService = Depends(get_research_service),
) -> ArtifactPromotionResponse:
    """
    Promote an approved, compatible research artifact to Production Draft.
    Requires administrator role.
    """
    return await service.promote_artifact(current_user, artifact_id, req)
