"""
Eduvia — Analytics & Telemetry Service (Phase 6)

Handles persistence, validation, authorization, and retrieval of
learner performance events and activity attempts.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics.models import ActivityAttempt, PerformanceEvent
from app.analytics.schemas import (
    ActivityAttemptCreate,
    PerformanceEventCreate,
    PerformanceEventQueryFilter,
)
from app.core.errors import AuthorizationError, NotFoundError, ValidationError
from app.curriculum.models import LearningObjective
from app.learners.models import Learner
from app.users.models import User

logger = structlog.get_logger(__name__)


class AnalyticsService:
    """Business logic service for learner telemetry and performance persistence."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def record_performance_event(
        self,
        event_in: PerformanceEventCreate,
    ) -> PerformanceEvent:
        """
        Record a validated performance event resulting from an activity interaction or evaluation.
        Verifies learner and objective referential integrity.
        """
        # 1. Verify Learner Exists & is Active
        learner_stmt = select(Learner).where(Learner.id == event_in.learner_id)
        learner_res = await self.session.execute(learner_stmt)
        learner = learner_res.scalars().first()
        if not learner:
            raise NotFoundError(f"Learner with id '{event_in.learner_id}' not found.")
        if not learner.is_active:
            raise ValidationError(f"Cannot record performance event for inactive learner '{event_in.learner_id}'.")

        # 2. Verify Objective Exists
        obj_stmt = select(LearningObjective).where(LearningObjective.id == event_in.objective_id)
        obj_res = await self.session.execute(obj_stmt)
        objective = obj_res.scalars().first()
        if not objective:
            raise NotFoundError(f"Learning objective with id '{event_in.objective_id}' not found.")

        # 3. Verify Attempt if Provided
        if event_in.attempt_id is not None:
            attempt_stmt = select(ActivityAttempt).where(ActivityAttempt.id == event_in.attempt_id)
            attempt_res = await self.session.execute(attempt_stmt)
            if not attempt_res.scalars().first():
                raise NotFoundError(f"Activity attempt with id '{event_in.attempt_id}' not found.")

        # 4. Determine Attempt Number if not explicitly specified
        attempt_number = event_in.attempts
        if attempt_number == 1:
            count_stmt = select(func.count(PerformanceEvent.id)).where(
                PerformanceEvent.learner_id == event_in.learner_id,
                PerformanceEvent.activity_id == event_in.activity_id,
            )
            count_res = await self.session.execute(count_stmt)
            existing_count = count_res.scalar() or 0
            attempt_number = existing_count + 1

        # 5. Construct & Persist Performance Event
        now = datetime.now(timezone.utc)
        event = PerformanceEvent(
            id=uuid.uuid4(),
            learner_id=event_in.learner_id,
            activity_id=event_in.activity_id,
            attempt_id=event_in.attempt_id,
            objective_id=event_in.objective_id,
            activity_type=event_in.activity_type.value,
            modality=event_in.modality.value,
            strategy=event_in.strategy.value,
            correct=event_in.correct,
            score=event_in.score,
            attempts=attempt_number,
            response_time_ms=event_in.response_time_ms,
            hints_used=event_in.hints_used,
            assistance_level=event_in.assistance_level,
            completed=event_in.completed,
            difficulty=event_in.difficulty,
            event_metadata=event_in.metadata,
            timestamp=event_in.timestamp or now,
            created_at=now,
            updated_at=now,
        )

        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)

        logger.info(
            "performance_event_recorded",
            event_id=str(event.id),
            learner_id=str(event.learner_id),
            activity_type=event.activity_type,
            correct=event.correct,
            score=event.score,
        )

        return event

    async def record_activity_attempt(
        self,
        attempt_in: ActivityAttemptCreate,
    ) -> ActivityAttempt:
        """Record an activity attempt entry for session tracking."""
        learner_stmt = select(Learner).where(Learner.id == attempt_in.learner_id)
        learner_res = await self.session.execute(learner_stmt)
        if not learner_res.scalars().first():
            raise NotFoundError(f"Learner with id '{attempt_in.learner_id}' not found.")

        now = datetime.now(timezone.utc)
        attempt = ActivityAttempt(
            id=uuid.uuid4(),
            activity_id=attempt_in.activity_id,
            learner_id=attempt_in.learner_id,
            session_id=attempt_in.session_id,
            started_at=attempt_in.started_at or now,
            completed_at=attempt_in.completed_at,
            response_data=attempt_in.response_data,
            score=attempt_in.score,
            completed=attempt_in.completed,
            created_at=now,
            updated_at=now,
        )

        self.session.add(attempt)
        await self.session.commit()
        await self.session.refresh(attempt)

        return attempt

    async def get_learner_events(
        self,
        learner_id: uuid.UUID,
        requesting_user: User | None = None,
        filters: PerformanceEventQueryFilter | None = None,
    ) -> list[PerformanceEvent]:
        """
        Query performance telemetry events for a specific learner.
        Enforces teacher/admin access control.
        """
        learner_stmt = select(Learner).where(Learner.id == learner_id)
        learner_res = await self.session.execute(learner_stmt)
        learner = learner_res.scalars().first()
        if not learner:
            raise NotFoundError(f"Learner with id '{learner_id}' not found.")

        # Authorization check: teachers can only view their own learners
        if requesting_user is not None:
            if requesting_user.role != "admin" and learner.teacher_id != requesting_user.id:
                raise AuthorizationError("You do not have permission to view performance data for this learner.")

        query = select(PerformanceEvent).where(PerformanceEvent.learner_id == learner_id)

        if filters:
            if filters.activity_type:
                query = query.where(PerformanceEvent.activity_type == filters.activity_type.value)
            if filters.objective_id:
                query = query.where(PerformanceEvent.objective_id == filters.objective_id)
            if filters.modality:
                query = query.where(PerformanceEvent.modality == filters.modality.value)
            if filters.correct is not None:
                query = query.where(PerformanceEvent.correct == filters.correct)
            query = query.order_by(PerformanceEvent.timestamp.desc()).limit(filters.limit).offset(filters.offset)
        else:
            query = query.order_by(PerformanceEvent.timestamp.desc()).limit(50)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_event_by_id(
        self,
        event_id: uuid.UUID,
        requesting_user: User | None = None,
    ) -> PerformanceEvent:
        """Retrieve a specific performance event by its unique identifier."""
        stmt = select(PerformanceEvent).where(PerformanceEvent.id == event_id)
        res = await self.session.execute(stmt)
        event = res.scalars().first()
        if not event:
            raise NotFoundError(f"Performance event '{event_id}' not found.")

        if requesting_user is not None and requesting_user.role != "admin":
            learner_stmt = select(Learner).where(Learner.id == event.learner_id)
            learner_res = await self.session.execute(learner_stmt)
            learner = learner_res.scalars().first()
            if learner and learner.teacher_id != requesting_user.id:
                raise AuthorizationError("You do not have permission to view this performance event.")

        return event
