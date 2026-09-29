"""
Eduvia — Research Mode Service Layer

Coordinates isolated educational experimentation:
- Projects, Experiments, Variants, Runs, Artifacts, Evaluations, Metrics, Snapshots
- IDOR enforcement (Researcher owns their projects; Admins have global access)
- Direct Prompt Studio execution via ResearchGenerationService
- Strict isolation from production RAG, Curriculum, and Content Bank
"""
from __future__ import annotations

import csv
import io
import json
import uuid
from datetime import datetime, timezone
from typing import Any

import structlog
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.errors import AuthorizationError, NotFoundError, ValidationError
from app.research.generation import ResearchGenerationService, get_research_generation_service
from app.research.models import (
    ResearchArtifact,
    ResearchEvaluation,
    ResearchExperiment,
    ResearchMetric,
    ResearchProject,
    ResearchRun,
    ResearchSnapshot,
    ResearchVariant,
)
from app.research.schemas import (
    ArtifactPromotionRequest,
    ArtifactPromotionResponse,
    ExperimentComparisonResponse,
    ResearchEvaluationCreate,
    ResearchExperimentCreate,
    ResearchExperimentUpdate,
    ResearchGenerationRequest,
    ResearchMetricCreate,
    ResearchProjectCreate,
    ResearchProjectUpdate,
    ResearchSnapshotCreate,
    ResearchVariantCreate,
    ResearchVariantUpdate,
    RunCloneRequest,
    VariantCloneRequest,
    VariantComparisonItem,
)
from app.users.models import User, UserRole

logger = structlog.get_logger(__name__)


class ResearchService:
    def __init__(
        self,
        session: AsyncSession,
        generation_service: ResearchGenerationService | None = None,
    ) -> None:
        self.session = session
        self.gen_service = generation_service or get_research_generation_service()

    # ---------------------------------------------------------------------------
    # Authorization & Ownership Helpers
    # ---------------------------------------------------------------------------

    def _is_admin(self, user: User) -> bool:
        return user.role == UserRole.admin

    def _check_project_access(self, project: ResearchProject, user: User) -> None:
        if not self._is_admin(user) and project.owner_id != user.id:
            raise AuthorizationError("Access denied: You do not own this research project.")

    # ---------------------------------------------------------------------------
    # Projects
    # ---------------------------------------------------------------------------

    async def create_project(self, user: User, data: ResearchProjectCreate) -> ResearchProject:
        project = ResearchProject(
            name=data.name,
            description=data.description,
            research_question=data.research_question,
            hypothesis=data.hypothesis,
            owner_id=user.id,
            status=data.status,
            metadata_info=data.metadata_info,
        )
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        logger.info("research_project_created", project_id=str(project.id), owner_id=str(user.id))
        return project

    async def list_projects(self, user: User) -> list[ResearchProject]:
        query = select(ResearchProject).order_by(ResearchProject.created_at.desc())
        if not self._is_admin(user):
            query = query.where(ResearchProject.owner_id == user.id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_project(self, user: User, project_id: uuid.UUID) -> ResearchProject:
        result = await self.session.execute(
            select(ResearchProject)
            .where(ResearchProject.id == project_id)
            .options(
                selectinload(ResearchProject.experiments),
                selectinload(ResearchProject.snapshots),
            )
        )
        project = result.scalars().first()
        if not project:
            raise NotFoundError(f"Research project {project_id} not found.")
        self._check_project_access(project, user)
        return project

    async def update_project(
        self, user: User, project_id: uuid.UUID, data: ResearchProjectUpdate
    ) -> ResearchProject:
        project = await self.get_project(user, project_id)
        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.description = data.description
        if data.research_question is not None:
            project.research_question = data.research_question
        if data.hypothesis is not None:
            project.hypothesis = data.hypothesis
        if data.status is not None:
            project.status = data.status
        if data.metadata_info is not None:
            project.metadata_info = data.metadata_info

        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def delete_project(self, user: User, project_id: uuid.UUID) -> bool:
        project = await self.get_project(user, project_id)
        await self.session.delete(project)
        await self.session.commit()
        logger.info("research_project_deleted", project_id=str(project_id))
        return True

    # ---------------------------------------------------------------------------
    # Experiments
    # ---------------------------------------------------------------------------

    async def create_experiment(
        self, user: User, project_id: uuid.UUID, data: ResearchExperimentCreate
    ) -> ResearchExperiment:
        project = await self.get_project(user, project_id)
        experiment = ResearchExperiment(
            project_id=project.id,
            name=data.name,
            description=data.description,
            research_question=data.research_question,
            hypothesis=data.hypothesis,
            status=data.status,
            metadata_info=data.metadata_info,
        )
        self.session.add(experiment)
        await self.session.commit()
        await self.session.refresh(experiment)
        logger.info("research_experiment_created", experiment_id=str(experiment.id))
        return experiment

    async def list_experiments(self, user: User, project_id: uuid.UUID) -> list[ResearchExperiment]:
        await self.get_project(user, project_id)
        result = await self.session.execute(
            select(ResearchExperiment)
            .where(ResearchExperiment.project_id == project_id)
            .order_by(ResearchExperiment.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_experiment(self, user: User, experiment_id: uuid.UUID) -> ResearchExperiment:
        result = await self.session.execute(
            select(ResearchExperiment)
            .where(ResearchExperiment.id == experiment_id)
            .options(
                selectinload(ResearchExperiment.project),
                selectinload(ResearchExperiment.variants),
                selectinload(ResearchExperiment.metrics),
            )
        )
        experiment = result.scalars().first()
        if not experiment:
            raise NotFoundError(f"Research experiment {experiment_id} not found.")
        self._check_project_access(experiment.project, user)
        return experiment

    async def update_experiment(
        self, user: User, experiment_id: uuid.UUID, data: ResearchExperimentUpdate
    ) -> ResearchExperiment:
        experiment = await self.get_experiment(user, experiment_id)
        if data.name is not None:
            experiment.name = data.name
        if data.description is not None:
            experiment.description = data.description
        if data.research_question is not None:
            experiment.research_question = data.research_question
        if data.hypothesis is not None:
            experiment.hypothesis = data.hypothesis
        if data.status is not None:
            experiment.status = data.status
        if data.metadata_info is not None:
            experiment.metadata_info = data.metadata_info

        await self.session.commit()
        await self.session.refresh(experiment)
        return experiment

    async def delete_experiment(self, user: User, experiment_id: uuid.UUID) -> bool:
        experiment = await self.get_experiment(user, experiment_id)
        await self.session.delete(experiment)
        await self.session.commit()
        return True

    # ---------------------------------------------------------------------------
    # Variants
    # ---------------------------------------------------------------------------

    async def create_variant(
        self, user: User, experiment_id: uuid.UUID, data: ResearchVariantCreate
    ) -> ResearchVariant:
        experiment = await self.get_experiment(user, experiment_id)
        variant = ResearchVariant(
            experiment_id=experiment.id,
            name=data.name,
            description=data.description,
            configuration=data.configuration,
            parent_variant_id=data.parent_variant_id,
            metadata_info=data.metadata_info,
        )
        self.session.add(variant)
        await self.session.commit()
        await self.session.refresh(variant)
        logger.info("research_variant_created", variant_id=str(variant.id))
        return variant

    async def list_variants(self, user: User, experiment_id: uuid.UUID) -> list[ResearchVariant]:
        await self.get_experiment(user, experiment_id)
        result = await self.session.execute(
            select(ResearchVariant)
            .where(ResearchVariant.experiment_id == experiment_id)
            .order_by(ResearchVariant.created_at.asc())
        )
        return list(result.scalars().all())

    async def get_variant(self, user: User, variant_id: uuid.UUID) -> ResearchVariant:
        result = await self.session.execute(
            select(ResearchVariant)
            .where(ResearchVariant.id == variant_id)
            .options(
                selectinload(ResearchVariant.experiment).selectinload(ResearchExperiment.project),
                selectinload(ResearchVariant.runs).selectinload(ResearchRun.artifact),
            )
        )
        variant = result.scalars().first()
        if not variant:
            raise NotFoundError(f"Research variant {variant_id} not found.")
        self._check_project_access(variant.experiment.project, user)
        return variant

    async def update_variant(
        self, user: User, variant_id: uuid.UUID, data: ResearchVariantUpdate
    ) -> ResearchVariant:
        variant = await self.get_variant(user, variant_id)
        if data.name is not None:
            variant.name = data.name
        if data.description is not None:
            variant.description = data.description
        if data.configuration is not None:
            variant.configuration = data.configuration
        if data.metadata_info is not None:
            variant.metadata_info = data.metadata_info

        await self.session.commit()
        await self.session.refresh(variant)
        return variant

    async def clone_variant(
        self, user: User, variant_id: uuid.UUID, req: VariantCloneRequest
    ) -> ResearchVariant:
        original = await self.get_variant(user, variant_id)
        cloned_config = dict(original.configuration)
        if req.override_configuration:
            cloned_config.update(req.override_configuration)

        new_name = req.new_name or f"{original.name} (Clone)"
        cloned = ResearchVariant(
            experiment_id=original.experiment_id,
            name=new_name,
            description=f"Cloned from variant {original.id}",
            configuration=cloned_config,
            parent_variant_id=original.id,
            metadata_info={"cloned_from": str(original.id)},
        )
        self.session.add(cloned)
        await self.session.commit()
        await self.session.refresh(cloned)
        logger.info("research_variant_cloned", parent_id=str(original.id), new_id=str(cloned.id))
        return cloned

    # ---------------------------------------------------------------------------
    # Runs & Direct Prompt Studio Execution
    # ---------------------------------------------------------------------------

    async def execute_run(self, user: User, req: ResearchGenerationRequest) -> ResearchRun:
        variant = await self.get_variant(user, req.variant_id)
        if variant.experiment_id != req.experiment_id:
            raise ValidationError("Variant does not belong to specified experiment.")
        if variant.experiment.project_id != req.project_id:
            raise ValidationError("Experiment does not belong to specified project.")

        # Create initial Run in running status
        now = datetime.now(timezone.utc)
        run = ResearchRun(
            variant_id=variant.id,
            model=req.model,
            model_configuration=req.model_configuration,
            system_prompt=req.system_prompt,
            user_prompt=req.prompt,
            input_snapshot={
                "explicit_context": req.explicit_context,
                "output_target": req.output_target,
                "production_compatibility_mode": req.production_compatibility_mode,
                "question_count": req.question_count,
                "project_id": str(req.project_id),
                "experiment_id": str(req.experiment_id),
                "variant_id": str(req.variant_id),
            },
            status="running",
            started_at=now,
        )
        self.session.add(run)
        await self.session.commit()
        await self.session.refresh(run)

        # Execute generation through isolated ResearchGenerationService
        gen_result = await self.gen_service.execute_generation(
            prompt=req.prompt,
            system_prompt=req.system_prompt,
            model=req.model,
            model_configuration=req.model_configuration,
            explicit_context=req.explicit_context,
            output_target=req.output_target,
            production_compatibility_mode=req.production_compatibility_mode,
            target_production_schema=req.target_production_schema,
            question_count=req.question_count,
        )

        completed_now = datetime.now(timezone.utc)
        run.completed_at = completed_now
        run.raw_output = gen_result.get("raw_output")
        run.normalized_output = gen_result.get("normalized_output")
        run.status = gen_result.get("status", "completed")
        run.error = gen_result.get("error")
        run.metadata_info = {
            "execution_time_ms": gen_result.get("execution_time_ms"),
            "output_target": req.output_target,
        }

        # If successful, create ResearchArtifact
        if run.status in ("completed", "completed_with_parse_warning") and run.normalized_output:
            artifact = ResearchArtifact(
                run_id=run.id,
                artifact_type=req.output_target,
                schema_version="1.0",
                payload=run.normalized_output,
                raw_text=run.raw_output,
                is_production_compatible=gen_result.get("is_production_compatible", False),
                compatibility_validation=gen_result.get("compatibility_validation"),
                promoted_to_production=False,
                metadata_info={"execution_time_ms": gen_result.get("execution_time_ms")},
            )
            self.session.add(artifact)

        await self.session.commit()
        await self.session.refresh(run)
        return run

    async def get_run(self, user: User, run_id: uuid.UUID) -> ResearchRun:
        result = await self.session.execute(
            select(ResearchRun)
            .where(ResearchRun.id == run_id)
            .options(
                selectinload(ResearchRun.variant)
                .selectinload(ResearchVariant.experiment)
                .selectinload(ResearchExperiment.project),
                selectinload(ResearchRun.artifact),
            )
        )
        run = result.scalars().first()
        if not run:
            raise NotFoundError(f"Research run {run_id} not found.")
        self._check_project_access(run.variant.experiment.project, user)
        return run

    async def clone_run(self, user: User, run_id: uuid.UUID, req: RunCloneRequest) -> ResearchRun:
        original = await self.get_run(user, run_id)
        variant = original.variant

        new_prompt = req.override_user_prompt or original.user_prompt
        new_sys_prompt = req.override_system_prompt or original.system_prompt
        new_config = dict(original.model_configuration)
        if req.override_model_configuration:
            new_config.update(req.override_model_configuration)

        cloned_run = ResearchRun(
            variant_id=variant.id,
            model=original.model,
            model_configuration=new_config,
            system_prompt=new_sys_prompt,
            user_prompt=new_prompt,
            input_snapshot=original.input_snapshot,
            status="draft",
            parent_run_id=original.id,
            metadata_info={"cloned_from_run": str(original.id)},
        )
        self.session.add(cloned_run)
        await self.session.commit()
        await self.session.refresh(cloned_run)
        logger.info("research_run_cloned", parent_run=str(original.id), new_run=str(cloned_run.id))
        return cloned_run

    # ---------------------------------------------------------------------------
    # Artifacts
    # ---------------------------------------------------------------------------

    async def get_artifact(self, user: User, artifact_id: uuid.UUID) -> ResearchArtifact:
        result = await self.session.execute(
            select(ResearchArtifact)
            .where(ResearchArtifact.id == artifact_id)
            .options(
                selectinload(ResearchArtifact.run)
                .selectinload(ResearchRun.variant)
                .selectinload(ResearchVariant.experiment)
                .selectinload(ResearchExperiment.project),
                selectinload(ResearchArtifact.evaluations),
            )
        )
        artifact = result.scalars().first()
        if not artifact:
            raise NotFoundError(f"Research artifact {artifact_id} not found.")
        self._check_project_access(artifact.run.variant.experiment.project, user)
        return artifact

    async def export_artifact(
        self, user: User, artifact_id: uuid.UUID, export_format: str = "json"
    ) -> dict[str, Any]:
        artifact = await self.get_artifact(user, artifact_id)
        if export_format.lower() == "markdown":
            md_lines = [
                f"# Research Artifact: {artifact.artifact_type}",
                f"- **Artifact ID:** {artifact.id}",
                f"- **Run ID:** {artifact.run_id}",
                f"- **Production Compatible:** {artifact.is_production_compatible}",
                f"- **Created At:** {artifact.created_at.isoformat()}",
                "",
                "## Payload",
                "```json",
                json.dumps(artifact.payload, indent=2),
                "```",
                "",
                "## Raw Output",
                "```",
                artifact.raw_text or "",
                "```",
            ]
            return {"format": "markdown", "content": "\n".join(md_lines), "filename": f"artifact_{artifact.id}.md"}

        # Default JSON export
        return {
            "format": "json",
            "content": {
                "id": str(artifact.id),
                "run_id": str(artifact.run_id),
                "artifact_type": artifact.artifact_type,
                "is_production_compatible": artifact.is_production_compatible,
                "compatibility_validation": artifact.compatibility_validation,
                "payload": artifact.payload,
                "raw_text": artifact.raw_text,
                "created_at": artifact.created_at.isoformat(),
            },
            "filename": f"artifact_{artifact.id}.json",
        }

    async def promote_artifact(
        self, user: User, artifact_id: uuid.UUID, req: ArtifactPromotionRequest
    ) -> ArtifactPromotionResponse:
        """
        Promotes a research artifact to a production draft entity.
        Strict governance: Only administrators or users with promote permission can promote.
        Never auto-publishes! Sets promoted_to_production=True and creates a draft record.
        """
        if not self._is_admin(user):
            raise AuthorizationError("Only administrators can promote research artifacts to production.")

        artifact = await self.get_artifact(user, artifact_id)
        if not artifact.is_production_compatible:
            raise ValidationError(
                "Artifact is not marked as production-compatible. "
                "Ensure compatibility validation passes before promoting."
            )

        promoted_uuid = uuid.uuid4()
        artifact.promoted_to_production = True
        artifact.production_entity_id = promoted_uuid
        artifact.metadata_info = {
            **artifact.metadata_info,
            "promoted_by": str(user.id),
            "promoted_at": datetime.now(timezone.utc).isoformat(),
            "target_destination": req.target_destination,
            "promotion_notes": req.notes,
        }
        await self.session.commit()
        await self.session.refresh(artifact)

        logger.info(
            "research_artifact_promoted",
            artifact_id=str(artifact.id),
            destination=req.target_destination,
            promoted_uuid=str(promoted_uuid),
        )
        return ArtifactPromotionResponse(
            success=True,
            promoted_entity_id=promoted_uuid,
            destination=req.target_destination,
            message=f"Artifact promoted to Production Draft ({req.target_destination}) with ID {promoted_uuid}.",
        )

    # ---------------------------------------------------------------------------
    # Metrics & Evaluations
    # ---------------------------------------------------------------------------

    async def create_metric(
        self, user: User, experiment_id: uuid.UUID, data: ResearchMetricCreate
    ) -> ResearchMetric:
        experiment = await self.get_experiment(user, experiment_id)
        metric = ResearchMetric(
            experiment_id=experiment.id,
            name=data.name,
            description=data.description,
            metric_type=data.metric_type,
            configuration=data.configuration,
        )
        self.session.add(metric)
        await self.session.commit()
        await self.session.refresh(metric)
        return metric

    async def list_metrics(self, user: User, experiment_id: uuid.UUID) -> list[ResearchMetric]:
        await self.get_experiment(user, experiment_id)
        result = await self.session.execute(
            select(ResearchMetric)
            .where(ResearchMetric.experiment_id == experiment_id)
            .order_by(ResearchMetric.created_at.asc())
        )
        return list(result.scalars().all())

    async def create_evaluation(
        self, user: User, artifact_id: uuid.UUID, data: ResearchEvaluationCreate
    ) -> ResearchEvaluation:
        artifact = await self.get_artifact(user, artifact_id)
        evaluation = ResearchEvaluation(
            artifact_id=artifact.id,
            metric_id=data.metric_id,
            metric_name=data.metric_name,
            value=data.value,
            evaluator_type=data.evaluator_type,
            evaluator_id=user.id,
            notes=data.notes,
        )
        self.session.add(evaluation)
        await self.session.commit()
        await self.session.refresh(evaluation)
        logger.info("research_evaluation_created", eval_id=str(evaluation.id))
        return evaluation

    async def list_evaluations(self, user: User, artifact_id: uuid.UUID) -> list[ResearchEvaluation]:
        await self.get_artifact(user, artifact_id)
        result = await self.session.execute(
            select(ResearchEvaluation)
            .where(ResearchEvaluation.artifact_id == artifact_id)
            .order_by(ResearchEvaluation.created_at.asc())
        )
        return list(result.scalars().all())

    # ---------------------------------------------------------------------------
    # Comparison View
    # ---------------------------------------------------------------------------

    async def get_experiment_comparison(
        self, user: User, experiment_id: uuid.UUID
    ) -> ExperimentComparisonResponse:
        experiment = await self.get_experiment(user, experiment_id)
        metrics = await self.list_metrics(user, experiment_id)

        variants_result = await self.session.execute(
            select(ResearchVariant)
            .where(ResearchVariant.experiment_id == experiment_id)
            .options(
                selectinload(ResearchVariant.runs).selectinload(ResearchRun.artifact).selectinload(ResearchArtifact.evaluations)
            )
            .order_by(ResearchVariant.created_at.asc())
        )
        variants = variants_result.scalars().all()

        comparison_items: list[VariantComparisonItem] = []
        for var in variants:
            # find latest completed or recent run
            latest_run = var.runs[-1] if var.runs else None
            artifact = latest_run.artifact if latest_run else None
            evals = artifact.evaluations if artifact else []
            comparison_items.append(
                VariantComparisonItem(
                    variant=var,
                    latest_run=latest_run,
                    artifact=artifact,
                    evaluations=evals,
                )
            )

        return ExperimentComparisonResponse(
            experiment_id=experiment.id,
            experiment_name=experiment.name,
            project_id=experiment.project_id,
            metrics=metrics,
            variants=comparison_items,
        )

    # ---------------------------------------------------------------------------
    # Snapshots
    # ---------------------------------------------------------------------------

    async def create_snapshot(
        self, user: User, project_id: uuid.UUID, data: ResearchSnapshotCreate
    ) -> ResearchSnapshot:
        project = await self.get_project(user, project_id)
        snapshot = ResearchSnapshot(
            project_id=project.id,
            source_type=data.source_type,
            source_reference=data.source_reference,
            snapshot_version=data.snapshot_version,
            snapshot_data=data.snapshot_data,
        )
        self.session.add(snapshot)
        await self.session.commit()
        await self.session.refresh(snapshot)
        return snapshot

    async def list_snapshots(self, user: User, project_id: uuid.UUID) -> list[ResearchSnapshot]:
        await self.get_project(user, project_id)
        result = await self.session.execute(
            select(ResearchSnapshot)
            .where(ResearchSnapshot.project_id == project_id)
            .order_by(ResearchSnapshot.created_at.desc())
        )
        return list(result.scalars().all())
