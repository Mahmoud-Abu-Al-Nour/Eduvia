"""
Eduvia — Teacher Insights & Dashboard Schemas (Phase 10)

Pydantic models for classroom/cohort aggregations, deterministic intervention alerts,
and Individualized Education Plan (IEP) progress reports.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AlertSeverity(str, Enum):
    """Severity levels for observable educational intervention alerts."""

    info = "info"
    warning = "warning"
    action_required = "action_required"


class AlertTriggerType(str, Enum):
    """Observable interaction signal types that trigger educational alerts."""

    low_accuracy = "low_accuracy"
    high_assistance = "high_assistance"
    stalled_mastery = "stalled_mastery"
    inactivity = "inactivity"


class InterventionAlert(BaseModel):
    """
    Deterministic educational alert representing an observable interaction signal.
    Strictly non-diagnostic; describes pedagogical observations and recommended adjustments.
    """

    model_config = ConfigDict(from_attributes=True)

    alert_id: str = Field(..., description="Unique deterministic identifier for the alert")
    learner_id: uuid.UUID = Field(..., description="Target learner identifier")
    learner_display_name: str = Field(..., description="Non-PII display name of the learner")
    trigger_type: AlertTriggerType = Field(..., description="Type of educational trigger")
    severity: AlertSeverity = Field(..., description="Urgency of recommended intervention")
    message: str = Field(..., description="Human-readable pedagogical explanation of the signal")
    summary: str = Field(default="", description="Frontend alert summary")
    recommended_action: str = Field(
        ..., description="Suggested teacher adjustment (e.g. adjust modality, lower difficulty)"
    )
    recommended_pedagogical_action: str = Field(
        default="", description="Frontend recommended pedagogical action"
    )
    evidence_context: dict[str, Any] = Field(
        default_factory=dict, description="Supporting telemetry metrics"
    )
    evidence_metrics: dict[str, Any] = Field(
        default_factory=dict, description="Frontend evidence metrics"
    )
    detected_at: datetime = Field(..., description="UTC timestamp of signal detection")
    created_at: datetime | None = Field(default=None, description="Created timestamp")
    is_resolved: bool = Field(default=False, description="Whether alert is resolved")


class TeacherDashboardOverview(BaseModel):
    """High-level KPIs for authenticated teacher overview dashboard."""

    model_config = ConfigDict(from_attributes=True)

    # Backend core fields
    total_learners: int = Field(default=0, description="Total learners assigned to this teacher")
    active_learners_7d: int = Field(default=0, description="Learners with interaction events in last 7 days")
    total_activities_completed_7d: int = Field(
        default=0, description="Total completed activities by assigned learners in last 7 days"
    )
    cohort_average_accuracy_7d: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Mean accuracy across assigned cohort over last 7 days"
    )
    active_alerts_count: int = Field(default=0, description="Count of active intervention alerts")
    recent_alerts: list[InterventionAlert] = Field(
        default_factory=list, description="Top active intervention alerts needing attention"
    )

    # Frontend compatibility fields
    teacher_id: uuid.UUID | None = Field(default=None, description="Teacher ID")
    teacher_name: str = Field(default="Educator", description="Teacher display name")
    total_assigned_learners: int = Field(default=0, description="Total assigned learners count")
    active_learners_count: int = Field(default=0, description="Active learners count")
    total_completed_activities: int = Field(default=0, description="Total completed activities")
    average_cohort_accuracy: float = Field(default=0.0, description="Cohort average accuracy")
    pending_alerts: list[InterventionAlert] = Field(
        default_factory=list, description="Active intervention alerts"
    )
    recent_recommendations: list[Any] = Field(
        default_factory=list, description="Recent adaptive recommendations"
    )


class CohortLearnerSummary(BaseModel):
    """Individual learner summary within cohort roster view."""

    model_config = ConfigDict(from_attributes=True)

    learner_id: uuid.UUID
    display_name: str
    learning_level: str
    age_group: str = Field(default="primary")
    communication_preference: str
    is_active: bool = Field(default=True)
    total_events: int = Field(default=0)
    activities_completed: int = Field(default=0)
    completed_activities: int = Field(default=0)
    overall_accuracy: float = Field(..., ge=0.0, le=1.0)
    average_assistance: float = Field(default=0.0, ge=0.0, le=3.0)
    average_assistance_level: float = Field(default=0.0, ge=0.0, le=3.0)
    mastered_objectives_count: int = Field(default=0)
    in_progress_objectives_count: int = Field(default=0)
    last_active_at: datetime | None = None
    active_alert_count: int = 0
    active_alerts_count: int = 0


class CohortInsights(BaseModel):
    """Classroom-level aggregated insights across all assigned learners."""

    model_config = ConfigDict(from_attributes=True)

    # Backend core fields
    cohort_size: int = Field(default=0)
    reporting_period_days: int = Field(default=30)
    average_accuracy: float = Field(default=0.0, ge=0.0, le=1.0)
    average_assistance_level: float = Field(default=0.0, ge=0.0, le=3.0)
    modality_distribution: dict[str, float] = Field(
        default_factory=dict, description="Percentage of activities completed per sensory modality"
    )
    mastery_distribution: dict[str, int] = Field(
        default_factory=dict,
        description="Count of objectives across cohort: mastered, developing, emerging, struggling",
    )
    learner_summaries: list[CohortLearnerSummary] = Field(
        default_factory=list, description="Roster-level individual student summaries"
    )

    # Frontend compatibility fields
    teacher_id: uuid.UUID | None = Field(default=None)
    reporting_period: str = Field(default="30_days")
    total_cohort_learners: int = Field(default=0)
    active_learners_in_period: int = Field(default=0)
    cohort_accuracy: float = Field(default=0.0)
    cohort_avg_assistance_level: float = Field(default=0.0)
    total_activities_completed: int = Field(default=0)
    mastery_status_counts: dict[str, int] = Field(default_factory=dict)
    learners: list[CohortLearnerSummary] = Field(default_factory=list)


class IEPReportingPeriod(str, Enum):
    """Pre-configured reporting periods for IEP reports."""

    seven_days = "7_days"
    thirty_days = "30_days"
    ninety_days = "90_days"
    all_time = "all_time"
    custom = "custom"


class IEPObjectiveSummary(BaseModel):
    """Summary of progress on a specific learning objective for IEP reporting."""

    model_config = ConfigDict(from_attributes=True)

    objective_id: uuid.UUID
    title: str
    attempts_count: int
    accuracy: float = Field(..., ge=0.0, le=1.0)
    average_assistance: float = Field(..., ge=0.0, le=3.0)
    status: str = Field(..., description="mastered, developing, emerging, struggling, not_started")


class IEPReport(BaseModel):
    """
    Comprehensive Individualized Education Plan (IEP) progress report.
    Presents objective progress, sensory modality effectiveness, and teacher recommendations.
    """

    model_config = ConfigDict(from_attributes=True)

    report_id: str
    generated_at: datetime
    reporting_period: str
    start_date: datetime | None = None
    end_date: datetime | None = None
    learner_id: uuid.UUID
    learner_display_name: str
    learning_level: str
    communication_preference: str
    teacher_notes: str | None = None
    total_activities_attempted: int
    overall_accuracy: float = Field(..., ge=0.0, le=1.0)
    overall_assistance_average: float = Field(..., ge=0.0, le=3.0)
    modality_efficacy: dict[str, float] = Field(
        default_factory=dict, description="Empirical success rate per presentation modality"
    )
    objectives_progress: list[IEPObjectiveSummary] = Field(
        default_factory=list, description="Progress on individual learning objectives"
    )
    teacher_recommendations: list[str] = Field(
        default_factory=list, description="Actionable pedagogical adjustments based on evidence"
    )
    printable_summary_markdown: str = Field(
        ..., description="Clean markdown document ready for printing or exporting"
    )
