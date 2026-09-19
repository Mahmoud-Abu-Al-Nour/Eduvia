"""
Eduvia — Recommendation Engine Schemas (Phase 8)

Pydantic DTOs for deterministic adaptive decisions, next-activity sequencing,
and learner profile effectiveness synchronization.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.activities.schemas import Activity, ActivityType
from app.analytics.schemas import Modality, TeachingStrategy


class ConfidenceLevel(StrEnum):
    """Confidence classification for adaptive recommendations."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationDecision(BaseModel):
    """
    Deterministic adaptive recommendation decision.

    Contains the selected curriculum target, difficulty tier, sensory presentation
    modality, interaction format, pedagogical strategy, and an explainable rationale
    derived strictly from empirical interaction evidence and teacher constraints.
    """

    model_config = ConfigDict(frozen=True)

    learner_id: uuid.UUID = Field(..., description="Target learner UUID")
    objective_id: uuid.UUID = Field(..., description="Recommended learning objective UUID")
    objective_title: str = Field(..., description="Localized title of the recommended objective")
    lesson_id: uuid.UUID | None = Field(default=None, description="Parent lesson UUID")
    unit_id: uuid.UUID | None = Field(default=None, description="Parent unit UUID")
    difficulty_level: int = Field(..., ge=1, le=5, description="Calibrated difficulty tier (1-5)")
    recommended_modality: Modality = Field(
        ..., description="Selected sensory presentation modality"
    )
    recommended_activity_type: ActivityType = Field(
        ..., description="Selected activity interaction modality"
    )
    recommended_strategy: TeachingStrategy = Field(
        ..., description="Selected pedagogical teaching strategy"
    )
    scaffolding_tier: int = Field(
        default=1, ge=1, le=3, description="Recommended initial scaffolding level (1-3)"
    )
    rationale: str = Field(
        ..., min_length=1, description="Explainable educational rationale grounded in evidence"
    )
    confidence_level: ConfidenceLevel = Field(
        ..., description="Confidence tier: high, medium, or low"
    )
    confidence_score: float = Field(
        ..., ge=0.0, le=1.0, description="Normalized empirical confidence score (0.0 - 1.0)"
    )
    evidence_event_count: int = Field(
        ..., ge=0, description="Number of observed performance events supporting this decision"
    )
    applied_constraints: list[str] = Field(
        default_factory=list, description="List of authoritative constraints applied"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC timestamp of decision",
    )


class AdaptiveNextActivityResponse(BaseModel):
    """Response returned when an adaptive decision is evaluated and an activity generated."""

    decision: RecommendationDecision = Field(
        ..., description="The underlying adaptive recommendation decision"
    )
    activity: Activity = Field(
        ..., description="The generated, Pydantic-validated learning activity"
    )
    fallback_used: bool = Field(
        default=False, description="Whether deterministic fallback generator was utilized"
    )
    generation_source: str = Field(
        default="gemini",
        description="Generation origin: 'gemini', 'mock', or 'deterministic_fallback'",
    )


class ProfileSyncResult(BaseModel):
    """Result of synchronizing profile modality and strategy effectiveness from history."""

    learner_id: uuid.UUID = Field(..., description="Target learner UUID")
    updated_modalities: dict[str, Any] = Field(
        ..., description="Updated modality effectiveness dictionary"
    )
    updated_strategies: dict[str, Any] = Field(
        ..., description="Updated strategy effectiveness dictionary"
    )
    total_events_processed: int = Field(
        ..., ge=0, description="Total performance events aggregated"
    )
    synced_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC timestamp of synchronization",
    )
