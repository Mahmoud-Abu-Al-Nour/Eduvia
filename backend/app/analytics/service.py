"""
Eduvia — Analytics & Telemetry Service (Phase 6)

Handles persistence, validation, authorization, and retrieval of
learner performance events and activity attempts.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics.models import ActivityAttempt, PerformanceEvent
from app.analytics.schemas import (
    ActivityAttemptCreate,
    ActivityTypeMetrics,
    LearnerAnalyticsSummary,
    LearnerMasteryReport,
    LearnerProgressReport,
    ModalityMetrics,
    ObjectiveMasteryStatus,
    PerformanceEventCreate,
    PerformanceEventQueryFilter,
    ProgressDataPoint,
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

    async def get_learner_summary(
        self,
        learner_id: uuid.UUID,
        requesting_user: User | None = None,
    ) -> LearnerAnalyticsSummary:
        """
        Compute aggregate performance summary for a learner across all modalities and activity types.
        Enforces teacher/admin authorization.
        """
        learner_stmt = select(Learner).where(Learner.id == learner_id)
        learner_res = await self.session.execute(learner_stmt)
        learner = learner_res.scalars().first()
        if not learner:
            raise NotFoundError(f"Learner with id '{learner_id}' not found.")

        if requesting_user is not None and requesting_user.role != "admin":
            if learner.teacher_id != requesting_user.id:
                raise AuthorizationError("You do not have permission to view analytics for this learner.")

        query = (
            select(PerformanceEvent)
            .where(PerformanceEvent.learner_id == learner_id)
            .order_by(PerformanceEvent.timestamp.asc())
        )
        result = await self.session.execute(query)
        events = list(result.scalars().all())

        if not events:
            return LearnerAnalyticsSummary(
                learner_id=learner_id,
                total_events=0,
                completed_activities=0,
                overall_accuracy=0.0,
                avg_score=0.0,
                avg_response_time_ms=0.0,
                avg_hints_per_activity=0.0,
                avg_assistance_level=0.0,
                modality_breakdown=[],
                activity_type_breakdown=[],
                first_activity_at=None,
                last_activity_at=None,
            )

        total_events = len(events)
        completed_activities = sum(1 for e in events if e.completed)
        correct_count = sum(1 for e in events if e.correct)
        overall_accuracy = round(correct_count / total_events, 4)
        avg_score = round(sum(e.score for e in events) / total_events, 4)
        avg_response_time_ms = round(sum(e.response_time_ms for e in events) / total_events, 2)
        avg_hints_per_activity = round(sum(e.hints_used for e in events) / total_events, 2)
        avg_assistance_level = round(sum(e.assistance_level for e in events) / total_events, 2)

        # Modality breakdown
        modalities = sorted(list({e.modality for e in events}))
        modality_breakdown: list[ModalityMetrics] = []
        for mod in modalities:
            mod_events = [e for e in events if e.modality == mod]
            mod_total = len(mod_events)
            mod_correct = sum(1 for e in mod_events if e.correct)
            modality_breakdown.append(
                ModalityMetrics(
                    modality=mod,
                    total_events=mod_total,
                    accuracy=round(mod_correct / mod_total, 4) if mod_total else 0.0,
                    avg_score=round(sum(e.score for e in mod_events) / mod_total, 4) if mod_total else 0.0,
                    avg_response_time_ms=round(sum(e.response_time_ms for e in mod_events) / mod_total, 2) if mod_total else 0.0,
                    avg_assistance_level=round(sum(e.assistance_level for e in mod_events) / mod_total, 2) if mod_total else 0.0,
                )
            )

        # Activity type breakdown
        act_types = sorted(list({e.activity_type for e in events}))
        activity_type_breakdown: list[ActivityTypeMetrics] = []
        for at in act_types:
            at_events = [e for e in events if e.activity_type == at]
            at_total = len(at_events)
            at_correct = sum(1 for e in at_events if e.correct)
            activity_type_breakdown.append(
                ActivityTypeMetrics(
                    activity_type=at,
                    total_events=at_total,
                    accuracy=round(at_correct / at_total, 4) if at_total else 0.0,
                    avg_score=round(sum(e.score for e in at_events) / at_total, 4) if at_total else 0.0,
                )
            )

        return LearnerAnalyticsSummary(
            learner_id=learner_id,
            total_events=total_events,
            completed_activities=completed_activities,
            overall_accuracy=overall_accuracy,
            avg_score=avg_score,
            avg_response_time_ms=avg_response_time_ms,
            avg_hints_per_activity=avg_hints_per_activity,
            avg_assistance_level=avg_assistance_level,
            modality_breakdown=modality_breakdown,
            activity_type_breakdown=activity_type_breakdown,
            first_activity_at=events[0].timestamp,
            last_activity_at=events[-1].timestamp,
        )

    async def get_learner_mastery(
        self,
        learner_id: uuid.UUID,
        requesting_user: User | None = None,
    ) -> LearnerMasteryReport:
        """
        Evaluate learning objective mastery for a learner using the deterministic rubric.
        Threshold: Accuracy >= minimum_accuracy (default 0.80) and assistance <= maximum_assistance (default 1).
        """
        learner_stmt = select(Learner).where(Learner.id == learner_id)
        learner_res = await self.session.execute(learner_stmt)
        learner = learner_res.scalars().first()
        if not learner:
            raise NotFoundError(f"Learner with id '{learner_id}' not found.")

        if requesting_user is not None and requesting_user.role != "admin":
            if learner.teacher_id != requesting_user.id:
                raise AuthorizationError("You do not have permission to view mastery for this learner.")

        query = (
            select(PerformanceEvent)
            .where(
                PerformanceEvent.learner_id == learner_id,
                PerformanceEvent.objective_id.isnot(None),
            )
            .order_by(PerformanceEvent.timestamp.asc())
        )
        result = await self.session.execute(query)
        events = list(result.scalars().all())

        # Collect unique objective IDs
        obj_ids = list({e.objective_id for e in events if e.objective_id is not None})
        objectives_map: dict[uuid.UUID, LearningObjective] = {}
        if obj_ids:
            obj_stmt = select(LearningObjective).where(LearningObjective.id.in_(obj_ids))
            obj_res = await self.session.execute(obj_stmt)
            objectives_map = {obj.id: obj for obj in obj_res.scalars().all()}

        objective_statuses: list[ObjectiveMasteryStatus] = []
        for obj_id in obj_ids:
            obj = objectives_map.get(obj_id)
            if obj:
                if isinstance(obj.title, dict):
                    obj_title = str(obj.title.get("en") or next(iter(obj.title.values()), str(obj.id)))
                else:
                    obj_title = str(obj.title)
            else:
                obj_title = f"Objective {obj_id}"
            diff_level = obj.difficulty_level if obj else 1
            criteria = (getattr(obj, "assessment_criteria", None) or {}) if obj else {}
            min_acc = float(criteria.get("minimum_accuracy", 0.80))
            max_assist = int(criteria.get("maximum_assistance_level", 1))

            obj_events = [e for e in events if e.objective_id == obj_id]
            total_attempts = len(obj_events)
            correct_count = sum(1 for e in obj_events if e.correct)
            accuracy = round(correct_count / total_attempts, 4) if total_attempts > 0 else 0.0
            avg_assistance = round(sum(e.assistance_level for e in obj_events) / total_attempts, 2) if total_attempts > 0 else 0.0
            last_attempt_at = max((e.timestamp for e in obj_events), default=None)

            mastery_achieved = bool(total_attempts >= 1 and accuracy >= min_acc and avg_assistance <= max_assist)
            status = "mastered" if mastery_achieved else ("in_progress" if total_attempts > 0 else "not_started")

            objective_statuses.append(
                ObjectiveMasteryStatus(
                    objective_id=obj_id,
                    objective_title=obj_title,
                    difficulty_level=diff_level,
                    total_attempts=total_attempts,
                    accuracy=accuracy,
                    avg_assistance_level=avg_assistance,
                    mastery_achieved=mastery_achieved,
                    status=status,
                    last_attempt_at=last_attempt_at,
                )
            )

        total_objectives_evaluated = len(objective_statuses)
        mastered_count = sum(1 for o in objective_statuses if o.status == "mastered")
        in_progress_count = sum(1 for o in objective_statuses if o.status == "in_progress")
        not_started_count = sum(1 for o in objective_statuses if o.status == "not_started")
        mastery_pct = round((mastered_count / total_objectives_evaluated) * 100.0, 2) if total_objectives_evaluated > 0 else 0.0

        return LearnerMasteryReport(
            learner_id=learner_id,
            total_objectives_evaluated=total_objectives_evaluated,
            mastered_count=mastered_count,
            in_progress_count=in_progress_count,
            not_started_count=not_started_count,
            mastery_percentage=mastery_pct,
            objectives=objective_statuses,
        )

    async def get_learner_progress(
        self,
        learner_id: uuid.UUID,
        requesting_user: User | None = None,
        days: int = 30,
    ) -> LearnerProgressReport:
        """
        Compute longitudinal performance timeline grouped by calendar day (UTC).
        """
        learner_stmt = select(Learner).where(Learner.id == learner_id)
        learner_res = await self.session.execute(learner_stmt)
        learner = learner_res.scalars().first()
        if not learner:
            raise NotFoundError(f"Learner with id '{learner_id}' not found.")

        if requesting_user is not None and requesting_user.role != "admin":
            if learner.teacher_id != requesting_user.id:
                raise AuthorizationError("You do not have permission to view progress for this learner.")

        query = select(PerformanceEvent).where(PerformanceEvent.learner_id == learner_id)
        if days > 0:
            cutoff = datetime.now(timezone.utc) - timedelta(days=days)
            query = query.where(PerformanceEvent.timestamp >= cutoff)

        query = query.order_by(PerformanceEvent.timestamp.asc())
        result = await self.session.execute(query)
        events = list(result.scalars().all())

        # Group events by date string (YYYY-MM-DD)
        daily_groups: dict[str, list[PerformanceEvent]] = {}
        for e in events:
            date_key = e.timestamp.strftime("%Y-%m-%d")
            if date_key not in daily_groups:
                daily_groups[date_key] = []
            daily_groups[date_key].append(e)

        data_points: list[ProgressDataPoint] = []
        for date_str in sorted(daily_groups.keys()):
            day_events = daily_groups[date_str]
            day_total = len(day_events)
            day_correct = sum(1 for e in day_events if e.correct)
            acc = round(day_correct / day_total, 4) if day_total else 0.0
            avg_sc = round(sum(e.score for e in day_events) / day_total, 4) if day_total else 0.0
            data_points.append(
                ProgressDataPoint(
                    date=date_str,
                    events_count=day_total,
                    accuracy=acc,
                    avg_score=avg_sc,
                )
            )

        return LearnerProgressReport(
            learner_id=learner_id,
            total_days_active=len(data_points),
            data_points=data_points,
        )
