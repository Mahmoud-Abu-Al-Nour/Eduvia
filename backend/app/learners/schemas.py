"""
Eduvia -- Learner & LearnerProfile Pydantic Schemas (Phase 3)

Validates:
- Structured teacher-provided initial info
- Educational support requirements and communication preferences
- Teacher constraints and overrides
- Learning pattern observations
"""
import uuid
from datetime import UTC, datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------
# Sub-Schemas for Teacher-Provided Profile Components
# ---------------------------------------------------------

class CommunicationPreferences(BaseModel):
    primary_mode: str = Field(
        default="verbal",
        description="Primary communication mode: verbal, visual_assisted, augmentative, written",
    )
    receptive_preference: list[str] = Field(
        default_factory=lambda: ["verbal", "visual_cues"],
        description="Preferences for incoming instructions (e.g., verbal, visual_cues, demonstration)",
    )
    expressive_preference: list[str] = Field(
        default_factory=lambda: ["verbal"],
        description="Preferences for responding (e.g., verbal, selection, gestures)",
    )
    notes: str = Field(default="", description="Teacher notes regarding communication nuances")


class CurrentSkillLevel(BaseModel):
    literacy_stage: str = Field(default="emerging", description="Literacy development level")
    numeracy_stage: str = Field(default="emerging", description="Numeracy development level")
    attention_span_minutes: int = Field(default=10, ge=1, le=120, description="Observed sustained focus duration")
    strengths: list[str] = Field(default_factory=list, description="Observed learning strengths")
    focus_areas: list[str] = Field(default_factory=list, description="Targeted development areas")


class SupportRequirements(BaseModel):
    sensory_accommodations: list[str] = Field(
        default_factory=list,
        description="Environmental or sensory considerations (e.g., reduced_audio, high_contrast)",
    )
    pacing: str = Field(default="standard", description="Learning pace preference: relaxed, standard, accelerated")
    guidance_level: str = Field(
        default="moderate",
        description="Degree of instructional guidance: minimal, moderate, intensive",
    )
    frequent_breaks: bool = Field(default=False, description="Whether short pauses are beneficial")


class TeacherConstraints(BaseModel):
    max_session_duration_minutes: int = Field(default=20, ge=1, le=180, description="Maximum continuous learning time")
    excluded_modalities: list[str] = Field(default_factory=list, description="Modalities excluded by teacher decision")
    required_modalities: list[str] = Field(default_factory=list, description="Modalities prioritized by teacher")
    custom_guidelines: str = Field(default="", description="Teacher pedagogical directives")


class TeacherOverrides(BaseModel):
    lock_difficulty_level: Optional[int] = Field(
        default=None,
        ge=1,
        le=5,
        description="Teacher-imposed cap or fixed difficulty level",
    )
    enforce_strategy: Optional[str] = Field(
        default=None,
        description="Teacher-mandated teaching strategy (e.g., Step-by-Step, Scaffolding)",
    )
    manual_adjustments_active: bool = Field(
        default=False,
        description="Flag indicating active teacher overrides",
    )


class LearnerObservationCreate(BaseModel):
    category: str = Field(
        ...,
        description="Observation category: modality, strategy, activity_type, response_behavior, general",
    )
    summary: str = Field(..., min_length=3, max_length=500, description="Concise observation description")
    context: Optional[dict[str, Any]] = Field(default=None, description="Structured contextual metadata")
    teacher_note: Optional[str] = Field(default=None, description="Optional teacher reflection")


class LearnerObservationItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    category: str
    summary: str
    context: Optional[dict[str, Any]] = None
    teacher_note: Optional[str] = None


# ---------------------------------------------------------
# Learner Profile Schemas
# ---------------------------------------------------------

class LearnerProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    learner_id: uuid.UUID
    communication_preferences: dict[str, Any]
    current_skill_level: dict[str, Any]
    support_requirements: dict[str, Any]
    teacher_constraints: dict[str, Any]
    teacher_notes: Optional[str] = None
    teacher_overrides: dict[str, Any]
    modality_effectiveness: dict[str, Any]
    strategy_effectiveness: dict[str, Any]
    activity_type_effectiveness: dict[str, Any]
    difficulty_tolerance: dict[str, Any]
    assistance_requirements: dict[str, Any]
    response_behavior: dict[str, Any]
    observations: list[dict[str, Any]]
    created_at: datetime
    updated_at: datetime


class LearnerProfileUpdate(BaseModel):
    communication_preferences: Optional[dict[str, Any]] = None
    current_skill_level: Optional[dict[str, Any]] = None
    support_requirements: Optional[dict[str, Any]] = None
    teacher_constraints: Optional[dict[str, Any]] = None
    teacher_notes: Optional[str] = None
    teacher_overrides: Optional[dict[str, Any]] = None


# ---------------------------------------------------------
# Learner CRUD Schemas
# ---------------------------------------------------------

class LearnerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Learner display name")
    age_group: str = Field(
        default="primary",
        description="Age group category: early_childhood, primary, intermediate, secondary",
    )
    learning_level: str = Field(
        default="beginner",
        description="Current educational stage: emerging, beginner, intermediate, advanced",
    )
    # Optional initial profile configuration
    communication_preferences: Optional[dict[str, Any]] = None
    support_requirements: Optional[dict[str, Any]] = None
    current_skill_level: Optional[dict[str, Any]] = None
    teacher_notes: Optional[str] = None
    teacher_constraints: Optional[dict[str, Any]] = None


class LearnerUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    age_group: Optional[str] = None
    learning_level: Optional[str] = None
    is_active: Optional[bool] = None
    profile: Optional[LearnerProfileUpdate] = None


class LearnerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    age_group: str
    learning_level: str
    is_active: bool
    teacher_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime


class LearnerDetailResponse(LearnerResponse):
    profile: Optional[LearnerProfileResponse] = None
