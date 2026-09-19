"""
Eduvia -- Learner & LearnerProfile SQLAlchemy ORM Models (Phase 3)

Adheres to:
- Standardized Curriculum + Personalized Delivery
- Educational terminology only (no medical or diagnostic classifications)
- Dynamic learning pattern evidence (not permanent labels)
- Strict preservation of teacher authority and override capabilities
"""
import uuid
from typing import Optional

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import EduviaBase
from app.users.models import User


class Learner(EduviaBase):
    """
    Learner domain entity representing a student.
    In MVP, learners are unauthenticated domain entities managed by Teachers/Admins.
    """
    __tablename__ = "learners"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    age_group: Mapped[str] = mapped_column(String(50), nullable=False, default="primary")
    learning_level: Mapped[str] = mapped_column(String(50), nullable=False, default="beginner")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    teacher_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Relationships
    teacher: Mapped[Optional["User"]] = relationship(lazy="selectin")
    profile: Mapped["LearnerProfile"] = relationship(
        back_populates="learner",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Learner id={self.id} name='{self.name}' level='{self.learning_level}'>"


class LearnerProfile(EduviaBase):
    """
    LearnerProfile foundation containing teacher-provided context and
    recorded learning pattern observations.
    
    Maintains the architectural boundary:
    Evidence & context (LearnerProfile) + Standardized content (Curriculum)
    = Future Personalized Delivery (Phase 4+)
    """
    __tablename__ = "learner_profiles"

    learner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("learners.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # 1. Initial Teacher-Provided Information
    communication_preferences: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "primary_mode": "verbal",  # verbal, visual_assisted, augmentative, written
            "receptive_preference": ["verbal", "visual_cues"],
            "expressive_preference": ["verbal"],
            "notes": "",
        },
    )

    current_skill_level: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "literacy_stage": "emerging",
            "numeracy_stage": "emerging",
            "attention_span_minutes": 10,
            "strengths": [],
            "focus_areas": [],
        },
    )

    support_requirements: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "sensory_accommodations": [],
            "pacing": "standard",  # relaxed, standard, accelerated
            "guidance_level": "moderate",  # minimal, moderate, intensive
            "frequent_breaks": False,
        },
    )

    # 2. Teacher Authority & Constraints
    teacher_constraints: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "max_session_duration_minutes": 20,
            "excluded_modalities": [],
            "required_modalities": [],
            "custom_guidelines": "",
        },
    )

    teacher_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    teacher_overrides: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "lock_difficulty_level": None,  # Optional teacher-locked difficulty ceiling
            "enforce_strategy": None,      # Optional teacher-mandated teaching strategy
            "manual_adjustments_active": False,
        },
    )

    # 3. Observed Learning Evidence Foundation (Populated by future learning attempts)
    modality_effectiveness: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "Visual": {"observed_count": 0, "engagement_rating": None},
            "Reading/Text": {"observed_count": 0, "engagement_rating": None},
            "Writing": {"observed_count": 0, "engagement_rating": None},
            "Audio": {"observed_count": 0, "engagement_rating": None},
            "Interactive": {"observed_count": 0, "engagement_rating": None},
        },
    )

    strategy_effectiveness: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "Step-by-Step": {"observed_count": 0, "success_rate": None},
            "Repetition": {"observed_count": 0, "success_rate": None},
            "Scaffolding": {"observed_count": 0, "success_rate": None},
            "Prompting": {"observed_count": 0, "success_rate": None},
            "Simplification": {"observed_count": 0, "success_rate": None},
            "Demonstration": {"observed_count": 0, "success_rate": None},
            "Positive Reinforcement": {"observed_count": 0, "success_rate": None},
            "Gradual Difficulty": {"observed_count": 0, "success_rate": None},
        },
    )

    activity_type_effectiveness: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "Matching": {"observed_count": 0, "accuracy_average": None},
            "MCQ": {"observed_count": 0, "accuracy_average": None},
            "Ordering": {"observed_count": 0, "accuracy_average": None},
            "Visual Identification": {"observed_count": 0, "accuracy_average": None},
            "Drag & Drop": {"observed_count": 0, "accuracy_average": None},
        },
    )

    difficulty_tolerance: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "comfortable_difficulty_level": 1,
            "highest_successful_level": 1,
            "frustration_threshold_observed": "moderate",
        },
    )

    assistance_requirements: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "prompt_dependence": "moderate",
            "most_effective_prompt_type": "visual",
        },
    )

    response_behavior: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "average_response_latency_seconds": None,
            "consistency_pattern": "stable",
        },
    )

    # Chronological log of qualitative / quantitative learning pattern observations
    observations: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    # Relationships
    learner: Mapped["Learner"] = relationship(back_populates="profile")

    def __repr__(self) -> str:
        return f"<LearnerProfile id={self.id} learner_id={self.learner_id}>"
