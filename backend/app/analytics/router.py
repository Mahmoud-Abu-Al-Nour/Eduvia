"""
Eduvia — Analytics & Telemetry API Router (Phase 6)

Endpoints for ingesting performance telemetry events, activity attempt sessions,
and querying learner event logs with teacher/admin access control.
"""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.analytics.schemas import (
    ActivityAttemptCreate,
    ActivityAttemptRead,
    LearnerAnalyticsSummary,
    LearnerMasteryReport,
    LearnerProgressReport,
    Modality,
    PerformanceEventCreate,
    PerformanceEventQueryFilter,
    PerformanceEventRead,
)
from app.analytics.service import AnalyticsService
from app.auth.dependencies import SessionDep, get_current_user
from app.activities.schemas import ActivityType
from app.core.errors import AuthorizationError, NotFoundError, ValidationError
from app.users.models import User

router = APIRouter(prefix="/analytics", tags=["analytics"])


def get_analytics_service(session: SessionDep) -> AnalyticsService:
    return AnalyticsService(session)


@router.post(
    "/events",
    response_model=PerformanceEventRead,
    status_code=status.HTTP_201_CREATED,
    summary="Record performance telemetry event",
    description="Persists an authoritative performance telemetry event from an activity interaction or evaluation.",
)
async def record_performance_event(
    event_in: PerformanceEventCreate,
    service: Annotated[AnalyticsService, Depends(get_analytics_service)],
) -> PerformanceEventRead:
    try:
        event = await service.record_performance_event(event_in)
        return PerformanceEventRead.model_validate(event)
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
        )
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=exc.message,
        )


@router.post(
    "/attempts",
    response_model=ActivityAttemptRead,
    status_code=status.HTTP_201_CREATED,
    summary="Record activity attempt",
    description="Records a learner's discrete attempt session on an activity.",
)
async def record_activity_attempt(
    attempt_in: ActivityAttemptCreate,
    service: Annotated[AnalyticsService, Depends(get_analytics_service)],
) -> ActivityAttemptRead:
    try:
        attempt = await service.record_activity_attempt(attempt_in)
        return ActivityAttemptRead.model_validate(attempt)
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
        )


@router.get(
    "/learners/{learner_id}/events",
    response_model=list[PerformanceEventRead],
    status_code=status.HTTP_200_OK,
    summary="List learner performance events",
    description="Retrieves performance event history for a learner. Accessible by the assigned teacher or admin.",
)
async def get_learner_events(
    learner_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[AnalyticsService, Depends(get_analytics_service)],
    activity_type: ActivityType | None = Query(default=None),
    objective_id: uuid.UUID | None = Query(default=None),
    modality: Modality | None = Query(default=None),
    correct: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[PerformanceEventRead]:
    filters = PerformanceEventQueryFilter(
        activity_type=activity_type,
        objective_id=objective_id,
        modality=modality,
        correct=correct,
        limit=limit,
        offset=offset,
    )
    try:
        events = await service.get_learner_events(
            learner_id=learner_id,
            requesting_user=current_user,
            filters=filters,
        )
        return [PerformanceEventRead.model_validate(e) for e in events]
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
        )
    except AuthorizationError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.message,
        )


@router.get(
    "/events/{event_id}",
    response_model=PerformanceEventRead,
    status_code=status.HTTP_200_OK,
    summary="Get performance event by ID",
    description="Retrieves a specific performance event. Requires teacher or admin access.",
)
async def get_event_by_id(
    event_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[AnalyticsService, Depends(get_analytics_service)],
) -> PerformanceEventRead:
    try:
        event = await service.get_event_by_id(
            event_id=event_id,
            requesting_user=current_user,
        )
        return PerformanceEventRead.model_validate(event)
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
        )
    except AuthorizationError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.message,
        )


# ── Phase 7: Learner Analytics & Mastery Endpoints ───────────────────────────


@router.get(
    "/learners/{learner_id}/summary",
    response_model=LearnerAnalyticsSummary,
    status_code=status.HTTP_200_OK,
    summary="Get learner performance analytics summary",
    description="Calculates aggregate accuracy, response latency, assistance levels, and modality breakdown for a learner.",
)
async def get_learner_analytics_summary(
    learner_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[AnalyticsService, Depends(get_analytics_service)],
) -> LearnerAnalyticsSummary:
    try:
        return await service.get_learner_summary(
            learner_id=learner_id,
            requesting_user=current_user,
        )
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
        )
    except AuthorizationError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.message,
        )


@router.get(
    "/learners/{learner_id}/mastery",
    response_model=LearnerMasteryReport,
    status_code=status.HTTP_200_OK,
    summary="Get learner learning objective mastery report",
    description="Evaluates mastery across curriculum objectives using the deterministic objective rubric.",
)
async def get_learner_mastery_report(
    learner_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[AnalyticsService, Depends(get_analytics_service)],
) -> LearnerMasteryReport:
    try:
        return await service.get_learner_mastery(
            learner_id=learner_id,
            requesting_user=current_user,
        )
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
        )
    except AuthorizationError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.message,
        )


@router.get(
    "/learners/{learner_id}/progress",
    response_model=LearnerProgressReport,
    status_code=status.HTTP_200_OK,
    summary="Get learner longitudinal progress timeline",
    description="Returns daily chronological performance points for longitudinal trend analysis.",
)
async def get_learner_progress_timeline(
    learner_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[AnalyticsService, Depends(get_analytics_service)],
    days: int = Query(default=30, ge=1, le=365, description="Number of historical days to inspect"),
) -> LearnerProgressReport:
    try:
        return await service.get_learner_progress(
            learner_id=learner_id,
            requesting_user=current_user,
            days=days,
        )
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
        )
    except AuthorizationError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.message,
        )
