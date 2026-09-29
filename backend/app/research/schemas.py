"""
Eduvia — Research Mode Schemas

Defines Pydantic DTOs for research projects, experiments, variants, runs,
artifacts, evaluations, metrics, snapshots, and Prompt Studio generation.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.config import settings
from app.research.catalog import (
    DEFAULT_RESEARCH_MODEL_ID,
    SUPPORTED_RESEARCH_MODEL_IDS,
    SUPPORTED_RESEARCH_MODELS,
)

# Supported output targets for Research Sandbox
ResearchOutputTarget = Literal[
    "freeform",
    "instructional_content",
    "question_set",
    "activity",
    "assessment",
    "curriculum",
    "lesson_plan",
]

ResearchStatus = Literal["draft", "active", "completed", "archived", "running", "failed"]


# ---------------------------------------------------------------------------
# Project Schemas
# ---------------------------------------------------------------------------

class ResearchProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    research_question: str | None = None
    hypothesis: str | None = None
    status: str = "active"
    metadata_info: dict[str, Any] = Field(default_factory=dict)


class ResearchProjectCreate(ResearchProjectBase):
    pass


class ResearchProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    research_question: str | None = None
    hypothesis: str | None = None
    status: str | None = None
    metadata_info: dict[str, Any] | None = None


class ResearchProjectRead(ResearchProjectBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Experiment Schemas
# ---------------------------------------------------------------------------

class ResearchExperimentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    research_question: str | None = None
    hypothesis: str | None = None
    status: str = "active"
    metadata_info: dict[str, Any] = Field(default_factory=dict)


class ResearchExperimentCreate(ResearchExperimentBase):
    pass


class ResearchExperimentUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    research_question: str | None = None
    hypothesis: str | None = None
    status: str | None = None
    metadata_info: dict[str, Any] | None = None


class ResearchExperimentRead(ResearchExperimentBase):
    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Variant Schemas
# ---------------------------------------------------------------------------

class ResearchVariantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    configuration: dict[str, Any] = Field(default_factory=dict)
    parent_variant_id: uuid.UUID | None = None
    metadata_info: dict[str, Any] = Field(default_factory=dict)


class ResearchVariantCreate(ResearchVariantBase):
    pass


class ResearchVariantUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    configuration: dict[str, Any] | None = None
    metadata_info: dict[str, Any] | None = None


class VariantCloneRequest(BaseModel):
    new_name: str | None = None
    override_configuration: dict[str, Any] | None = None


class ResearchVariantRead(ResearchVariantBase):
    id: uuid.UUID
    experiment_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Metric & Evaluation Schemas
# ---------------------------------------------------------------------------

class ResearchMetricCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    metric_type: str = "rating"
    configuration: dict[str, Any] = Field(default_factory=dict)


class ResearchMetricRead(BaseModel):
    id: uuid.UUID
    experiment_id: uuid.UUID
    name: str
    description: str | None = None
    metric_type: str
    configuration: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ResearchEvaluationCreate(BaseModel):
    metric_id: uuid.UUID | None = None
    metric_name: str = Field(..., min_length=1, max_length=100)
    value: dict[str, Any] = Field(..., description="e.g. {'score': 4, 'max': 5} or {'verdict': 'pass'}")
    evaluator_type: str = "manual"
    notes: str | None = None


class ResearchEvaluationRead(BaseModel):
    id: uuid.UUID
    artifact_id: uuid.UUID
    metric_id: uuid.UUID | None = None
    metric_name: str
    value: dict[str, Any]
    evaluator_type: str
    evaluator_id: uuid.UUID
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Run & Artifact Schemas
# ---------------------------------------------------------------------------

class RunCloneRequest(BaseModel):
    override_model_configuration: dict[str, Any] | None = None
    override_user_prompt: str | None = None
    override_system_prompt: str | None = None


class ResearchArtifactRead(BaseModel):
    id: uuid.UUID
    run_id: uuid.UUID
    artifact_type: str
    schema_version: str
    payload: dict[str, Any]
    raw_text: str | None = None
    is_production_compatible: bool = False
    compatibility_validation: dict[str, Any] | None = None
    promoted_to_production: bool = False
    production_entity_id: uuid.UUID | None = None
    metadata_info: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

    @field_validator("promoted_to_production", "is_production_compatible", mode="before")
    @classmethod
    def default_bool(cls, v: Any) -> bool:
        if v is None:
            return False
        return bool(v)


class ResearchRunRead(BaseModel):
    id: uuid.UUID
    variant_id: uuid.UUID
    model: str
    model_configuration: dict[str, Any]
    system_prompt: str | None = None
    user_prompt: str
    input_snapshot: dict[str, Any] | None = None
    raw_output: str | None = None
    normalized_output: dict[str, Any] | None = None
    status: str
    error: str | None = None
    parent_run_id: uuid.UUID | None = None
    metadata_info: dict[str, Any]
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    artifact: ResearchArtifactRead | None = None
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Snapshot Schemas
# ---------------------------------------------------------------------------

class ResearchSnapshotCreate(BaseModel):
    source_type: str = Field(..., description="curriculum | content_item | activity")
    source_reference: str
    snapshot_version: str = "1.0"
    snapshot_data: dict[str, Any]


class ResearchSnapshotRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    source_type: str
    source_reference: str
    snapshot_version: str
    snapshot_data: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Prompt Studio & Generation DTOs
# ---------------------------------------------------------------------------

class ResearchModelInfo(BaseModel):
    id: str
    name: str
    description: str
    is_default: bool


class ResearchGenerationRequest(BaseModel):
    """
    Direct prompt studio generation contract.
    Does NOT require production curriculum, RAG, or learner profiles.
    Enforces server-side resource limits.
    """
    project_id: uuid.UUID
    experiment_id: uuid.UUID
    variant_id: uuid.UUID
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=settings.MAX_RESEARCH_PROMPT_LENGTH,
        description=f"Researcher prompt (max {settings.MAX_RESEARCH_PROMPT_LENGTH} characters)",
    )
    system_prompt: str | None = Field(
        None,
        max_length=settings.MAX_RESEARCH_PROMPT_LENGTH,
        description="Optional custom system prompt",
    )
    output_target: ResearchOutputTarget = Field("freeform", description="Type of educational asset")
    model: str = Field(DEFAULT_RESEARCH_MODEL_ID, description="Gemini model identifier")
    model_configuration: dict[str, Any] = Field(
        default_factory=lambda: {"temperature": 0.7, "max_output_tokens": 2048},
        description="Temperature, top_p, max_output_tokens, etc.",
    )
    explicit_context: dict[str, Any] | None = Field(
        default=None,
        description="Explicit researcher-supplied context (e.g. {'manual_context': '...'})",
    )
    question_count: int | None = Field(
        default=None,
        description=f"Optional explicit question count target (1-{settings.MAX_RESEARCH_QUESTIONS})",
    )
    production_compatibility_mode: bool = Field(
        default=False,
        description="If True, validates against production schemas without altering artifact",
    )
    target_production_schema: str | None = Field(
        default=None,
        description="'activity' | 'instructional_content'",
    )

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        if v not in SUPPORTED_RESEARCH_MODEL_IDS:
            raise ValueError(
                f"Model '{v}' is not supported in Research Mode. Supported models: {sorted(SUPPORTED_RESEARCH_MODEL_IDS)}"
            )
        return v

    @field_validator("model_configuration")
    @classmethod
    def validate_model_configuration(cls, v: dict[str, Any]) -> dict[str, Any]:
        if "max_output_tokens" in v:
            try:
                tokens = int(v["max_output_tokens"])
                if tokens > settings.MAX_RESEARCH_OUTPUT_TOKENS:
                    raise ValueError(
                        f"max_output_tokens ({tokens}) exceeds maximum allowed ({settings.MAX_RESEARCH_OUTPUT_TOKENS})"
                    )
                if tokens < 1:
                    raise ValueError("max_output_tokens must be >= 1")
            except (TypeError, ValueError) as e:
                raise ValueError(str(e))
        return v

    @field_validator("question_count")
    @classmethod
    def validate_question_count(cls, v: int | None) -> int | None:
        if v is not None:
            if v < 1 or v > settings.MAX_RESEARCH_QUESTIONS:
                raise ValueError(
                    f"question_count ({v}) must be between 1 and {settings.MAX_RESEARCH_QUESTIONS}"
                )
        return v


class ResearchGenerationResponse(BaseModel):
    run_id: uuid.UUID
    artifact_id: uuid.UUID | None = None
    status: str
    raw_output: str
    normalized_output: dict[str, Any] | None = None
    is_production_compatible: bool = False
    compatibility_validation: dict[str, Any] | None = None
    execution_time_ms: float | None = None
    error: str | None = None


# ---------------------------------------------------------------------------
# Promotion & Comparison DTOs
# ---------------------------------------------------------------------------

class ArtifactExportRequest(BaseModel):
    format: Literal["json", "markdown"] = "json"


class ArtifactPromotionRequest(BaseModel):
    target_destination: Literal["activity", "instructional_content"] = "activity"
    notes: str | None = None


class ArtifactPromotionResponse(BaseModel):
    success: bool
    promoted_entity_id: uuid.UUID | None = None
    destination: str
    message: str


class VariantComparisonItem(BaseModel):
    variant: ResearchVariantRead
    latest_run: ResearchRunRead | None = None
    artifact: ResearchArtifactRead | None = None
    evaluations: list[ResearchEvaluationRead] = Field(default_factory=list)


class ExperimentComparisonResponse(BaseModel):
    experiment_id: uuid.UUID
    experiment_name: str
    project_id: uuid.UUID
    metrics: list[ResearchMetricRead] = Field(default_factory=list)
    variants: list[VariantComparisonItem] = Field(default_factory=list)
