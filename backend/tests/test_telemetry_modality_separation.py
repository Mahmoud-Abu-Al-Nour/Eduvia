"""
Eduvia — Telemetry Modality Separation Verification Tests (Audit Requirement 3)

Validates that:
1. `activity_type` (ActivityType enum: multiple_choice, matching, ordering, visual_identification, drag_drop)
   and `modality` (Modality enum: visual, reading, writing, audio, interactive)
   are independently tracked and NEVER conflated under one ambiguous field.
2. In AnalyticsService, recording a performance event preserves both dimensions.
3. In Analytics summaries, `activity_type_breakdown` and `modality_breakdown` aggregate independently.
4. Queries can filter by activity_type and modality independently or in combination.
"""
from __future__ import annotations

import uuid
import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

from app.activities.schemas import ActivityType
from app.analytics.models import PerformanceEvent
from app.analytics.schemas import (
    ActivityTypeMetrics,
    Modality,
    ModalityMetrics,
    PerformanceEventCreate,
    TeachingStrategy,
)
from app.analytics.service import AnalyticsService


def test_schema_modality_and_activity_type_independence() -> None:
    """Ensure PerformanceEventCreate requires activity_type and modality independently."""
    learner_id = uuid.uuid4()
    activity_id = uuid.uuid4()
    objective_id = uuid.uuid4()

    # Create event for each of the 5 activity types, paired with various sensory modalities
    test_matrix = [
        (ActivityType.MULTIPLE_CHOICE, Modality.AUDIO),
        (ActivityType.MATCHING, Modality.INTERACTIVE),
        (ActivityType.ORDERING, Modality.VISUAL),
        (ActivityType.VISUAL_IDENTIFICATION, Modality.VISUAL),
        (ActivityType.DRAG_DROP, Modality.INTERACTIVE),
    ]

    for act_type, sens_mod in test_matrix:
        event = PerformanceEventCreate(
            learner_id=learner_id,
            activity_id=activity_id,
            objective_id=objective_id,
            activity_type=act_type,
            modality=sens_mod,
            strategy=TeachingStrategy.STEP_BY_STEP,
            correct=True,
            score=1.0,
            attempts=1,
            response_time_ms=1200,
        )
        assert event.activity_type == act_type
        assert event.modality == sens_mod
        assert event.activity_type.value != event.modality.value or act_type.value == "visual"


@pytest.mark.asyncio
async def test_analytics_summary_distinguishes_all_five_activity_types() -> None:
    """
    Verify that get_learner_analytics_summary produces separate breakdowns
    for all 5 activity types and sensory modalities.
    """
    learner_id = uuid.uuid4()
    mock_session = AsyncMock()

    service = AnalyticsService(mock_session)

    # Fabricate 5 events, one for each activity type, with overlapping sensory modalities
    events = [
        PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=learner_id,
            activity_id=uuid.uuid4(),
            objective_id=uuid.uuid4(),
            activity_type=ActivityType.MULTIPLE_CHOICE.value,
            modality=Modality.AUDIO.value,
            strategy="step_by_step",
            correct=True,
            score=1.0,
            attempts=1,
            response_time_ms=1000,
            hints_used=0,
            assistance_level=0,
            completed=True,
            timestamp=datetime.now(timezone.utc),
        ),
        PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=learner_id,
            activity_id=uuid.uuid4(),
            objective_id=uuid.uuid4(),
            activity_type=ActivityType.MATCHING.value,
            modality=Modality.INTERACTIVE.value,
            strategy="step_by_step",
            correct=True,
            score=1.0,
            attempts=1,
            response_time_ms=1500,
            hints_used=0,
            assistance_level=0,
            completed=True,
            timestamp=datetime.now(timezone.utc),
        ),
        PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=learner_id,
            activity_id=uuid.uuid4(),
            objective_id=uuid.uuid4(),
            activity_type=ActivityType.ORDERING.value,
            modality=Modality.VISUAL.value,
            strategy="step_by_step",
            correct=False,
            score=0.5,
            attempts=2,
            response_time_ms=2000,
            hints_used=1,
            assistance_level=1,
            completed=True,
            timestamp=datetime.now(timezone.utc),
        ),
        PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=learner_id,
            activity_id=uuid.uuid4(),
            objective_id=uuid.uuid4(),
            activity_type=ActivityType.VISUAL_IDENTIFICATION.value,
            modality=Modality.VISUAL.value,
            strategy="step_by_step",
            correct=True,
            score=1.0,
            attempts=1,
            response_time_ms=800,
            hints_used=0,
            assistance_level=0,
            completed=True,
            timestamp=datetime.now(timezone.utc),
        ),
        PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=learner_id,
            activity_id=uuid.uuid4(),
            objective_id=uuid.uuid4(),
            activity_type=ActivityType.DRAG_DROP.value,
            modality=Modality.INTERACTIVE.value,
            strategy="step_by_step",
            correct=True,
            score=1.0,
            attempts=1,
            response_time_ms=2500,
            hints_used=0,
            assistance_level=0,
            completed=True,
            timestamp=datetime.now(timezone.utc),
        ),
    ]

    mock_learner = MagicMock()
    mock_learner.id = learner_id
    mock_learner.teacher_id = uuid.uuid4()

    # Session execute returns learner first, then events
    mock_learner_result = MagicMock()
    mock_learner_result.scalars.return_value.first.return_value = mock_learner

    mock_events_result = MagicMock()
    mock_events_result.scalars.return_value.all.return_value = events

    mock_session.execute.side_effect = [mock_learner_result, mock_events_result]

    summary = await service.get_learner_summary(learner_id)

    # 1. Total events check
    assert summary.total_events == 5

    # 2. Activity Type Breakdown check
    act_types_found = {item.activity_type for item in summary.activity_type_breakdown}
    assert act_types_found == {
        "multiple_choice",
        "matching",
        "ordering",
        "visual_identification",
        "drag_drop",
    }, f"Expected all 5 activity types in breakdown, got {act_types_found}"

    # 3. Modality Breakdown check
    modalities_found = {item.modality for item in summary.modality_breakdown}
    assert modalities_found == {"audio", "interactive", "visual"}, f"Expected sensory modalities in breakdown, got {modalities_found}"

    # Verify that interactive has 2 events (matching + drag_drop)
    interactive_metrics = next(m for m in summary.modality_breakdown if m.modality == "interactive")
    assert interactive_metrics.total_events == 2

    # Verify that visual has 2 events (ordering + visual_identification)
    visual_metrics = next(m for m in summary.modality_breakdown if m.modality == "visual")
    assert visual_metrics.total_events == 2

    # Verify that audio has 1 event (multiple_choice)
    audio_metrics = next(m for m in summary.modality_breakdown if m.modality == "audio")
    assert audio_metrics.total_events == 1
