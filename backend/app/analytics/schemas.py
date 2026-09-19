"""
Eduvia — Analytics & Telemetry Pydantic Schemas (Phase 6)

Strict validation contracts for performance event ingestion, attempt tracking,
and query filtering.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.activities.schemas import ActivityType


class Modality(StrEnum):
    """Supported delivery modalities for learning activities."""
    VISUAL = "visual"
    READING = "reading"
    WRITING = "writing"
    AUDIO = "audio"
    INTERACTIVE = "interactive"


class TeachingStrategy(StrEnum):
    """Cognitive pedagogical teaching strategies."""
    STEP_BY_STEP = "step_by_step"
    REPETITION = "repetition"
    SCAFFOLDING = "scaffolding"
    PROMPTING = "prompting"
    SIMPLIFICATION = "simplification"
    DEMONSTRATION = "demonstration"
    POSITIVE_REINFORCEMENT = "positive_reinforcement"
    GRADUAL_DIFFICULTY = "gradual_difficulty"


# ── Performance Event Schemas ───────────────────────────────────────────────


class PerformanceEventCreate(BaseModel):
    """Input payload for recording a performance telemetry event."""
    model_config = ConfigDict(extra="forbid")

    learner_id: uuid.UUID = Field(..., description="Target learner identifier")
    activity_id: uuid.UUID = Field(..., description="Activity instance identifier")
    attempt_id: uuid.UUID | None = Field(default=None, description="Optional attempt session identifier")
    objective_id: uuid.UUID = Field(..., description="Curriculum learning objective identifier")
    activity_type: ActivityType = Field(..., description="Modality of the activity")
    modality: Modality = Field(default=Modality.VISUAL, description="Sensory delivery modality")
    strategy: TeachingStrategy = Field(default=TeachingStrategy.STEP_BY_STEP, description="Teaching strategy used")
    correct: bool = Field(..., description="Whether submission was authoritatively correct")
    score: float = Field(default=0.0, ge=0.0, le=1.0, description="Accuracy score (0.0 to 1.0)")
    attempts: int = Field(default=1, ge=1, description="Attempt number (>= 1)")
    response_time_ms: int = Field(default=0, ge=0, description="Latency / time spent in milliseconds")
    hints_used: int = Field(default=0, ge=0, le=10, description="Number of hints revealed")
    assistance_level: int = Field(default=0, ge=0, le=3, description="Assistance tier (0=None, 1=Subtle, 2=Guided, 3=Explicit)")
    completed: bool = Field(default=True, description="Whether activity session was completed")
    difficulty: int = Field(default=1, ge=1, le=5, description="Difficulty rating 1-5")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Detailed interaction telemetry metadata")
    timestamp: datetime | None = Field(default=None, description="Client or event occurrence timestamp")


class PerformanceEventRead(BaseModel):
    """Read schema representing a stored performance event."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    learner_id: uuid.UUID
    activity_id: uuid.UUID
    attempt_id: uuid.UUID | None = None
    objective_id: uuid.UUID
    activity_type: ActivityType
    modality: Modality
    strategy: TeachingStrategy
    correct: bool
    score: float
    attempts: int
    response_time_ms: int
    hints_used: int
    assistance_level: int
    completed: bool
    difficulty: int
    metadata: dict[str, Any] = Field(default_factory=dict, validation_alias="event_metadata")
    timestamp: datetime
    created_at: datetime


# ── Activity Attempt Schemas ────────────────────────────────────────────────


class ActivityAttemptCreate(BaseModel):
    """Input payload for recording a discrete activity attempt."""
    model_config = ConfigDict(extra="forbid")

    activity_id: uuid.UUID = Field(..., description="Activity identifier")
    learner_id: uuid.UUID = Field(..., description="Learner identifier")
    session_id: uuid.UUID | None = Field(default=None, description="Client interaction session ID")
    started_at: datetime | None = Field(default=None, description="Timestamp when attempt began")
    completed_at: datetime | None = Field(default=None, description="Timestamp when attempt completed")
    response_data: dict[str, Any] | None = Field(default=None, description="Raw learner response payload")
    score: float | None = Field(default=None, ge=0.0, le=1.0, description="Final score if completed")
    completed: bool = Field(default=False, description="Whether attempt was finished")


class ActivityAttemptRead(BaseModel):
    """Read schema for an activity attempt record."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    activity_id: uuid.UUID
    learner_id: uuid.UUID
    session_id: uuid.UUID | None
    started_at: datetime
    completed_at: datetime | None
    response_data: dict[str, Any] | None
    score: float | None
    completed: bool
    created_at: datetime
    updated_at: datetime


# ── Query & Filter Schemas ──────────────────────────────────────────────────


class PerformanceEventQueryFilter(BaseModel):
    """Query filters for retrieving learner performance telemetry."""
    activity_type: ActivityType | None = None
    objective_id: uuid.UUID | None = None
    modality: Modality | None = None
    correct: bool | None = None
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)
