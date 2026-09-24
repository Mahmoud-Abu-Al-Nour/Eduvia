"""
Eduvia — Teacher Insights & Dashboard Service (Phase 10)

Authoritative backend business logic for:
1. Teacher overview dashboard KPIs and metrics.
2. Classroom/cohort-level telemetry aggregations across assigned learners.
3. Deterministic pedagogical intervention alert detection.
4. Individualized Education Plan (IEP) progress reporting and export.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.analytics.models import PerformanceEvent
from app.analytics.service import AnalyticsService
from app.core.errors import AuthorizationError, NotFoundError, ValidationError
from app.curriculum.models import LearningObjective
from app.learners.models import Learner
from app.teachers.schemas import (
    AlertSeverity,
    AlertTriggerType,
    CohortInsights,
    CohortLearnerSummary,
    IEPObjectiveSummary,
    IEPReport,
    InterventionAlert,
    TeacherDashboardOverview,
)
from app.users.models import User

logger = structlog.get_logger(__name__)


class TeacherDashboardService:
    """Service providing teacher-facing cohort analytics, intervention alerts, and IEP reports."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.analytics_service = AnalyticsService(session)

    def _is_admin(self, user: User) -> bool:
        """Check if user has administrator privileges."""
        if hasattr(user.role, "value"):
            return user.role.value == "admin"
        return str(user.role) == "admin"

    async def _get_authorized_learners(self, teacher_user: User) -> list[Learner]:
        """Fetch all active learners assigned to the teacher (or all learners if admin)."""
        stmt = select(Learner).options(selectinload(Learner.profile)).where(Learner.is_active.is_(True))
        if not self._is_admin(teacher_user):
            stmt = stmt.where(Learner.teacher_id == teacher_user.id)
        stmt = stmt.order_by(Learner.name.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def _check_learner_access(self, teacher_user: User, learner_id: uuid.UUID) -> Learner:
        """Verify teacher ownership of learner and return learner entity."""
        stmt = select(Learner).options(selectinload(Learner.profile)).where(Learner.id == learner_id)
        res = await self.session.execute(stmt)
        learner = res.scalars().first()
        if not learner:
            raise NotFoundError(f"Learner with ID '{learner_id}' not found.")

        if not self._is_admin(teacher_user) and learner.teacher_id != teacher_user.id:
            raise AuthorizationError("You do not have permission to access this learner.")

        return learner

    async def get_dashboard_overview(self, teacher_user: User) -> TeacherDashboardOverview:
        """
        Calculates high-level KPIs for the teacher overview dashboard over the past 7 days.
        """
        learners = await self._get_authorized_learners(teacher_user)
        total_learners = len(learners)
        if total_learners == 0:
            return TeacherDashboardOverview(
                total_learners=0,
                active_learners_7d=0,
                total_activities_completed_7d=0,
                cohort_average_accuracy_7d=0.0,
                active_alerts_count=0,
                recent_alerts=[],
            )

        learner_ids = [l.id for l in learners]
        cutoff_7d = datetime.now(UTC) - timedelta(days=7)

        # Query events in last 7 days
        stmt_7d = (
            select(PerformanceEvent)
            .where(
                PerformanceEvent.learner_id.in_(learner_ids),
                PerformanceEvent.timestamp >= cutoff_7d,
            )
            .order_by(PerformanceEvent.timestamp.desc())
        )
        res_7d = await self.session.execute(stmt_7d)
        events_7d = list(res_7d.scalars().all())

        active_learner_ids = {e.learner_id for e in events_7d}
        active_learners_7d = len(active_learner_ids)
        total_activities_completed_7d = sum(1 for e in events_7d if e.completed)

        cohort_average_accuracy_7d = 0.0
        if events_7d:
            cohort_average_accuracy_7d = round(
                sum(1 for e in events_7d if e.correct) / len(events_7d), 2
            )

        # Detect active alerts
        all_alerts = await self.get_intervention_alerts(teacher_user)

        return TeacherDashboardOverview(
            total_learners=total_learners,
            active_learners_7d=active_learners_7d,
            total_activities_completed_7d=total_activities_completed_7d,
            cohort_average_accuracy_7d=cohort_average_accuracy_7d,
            active_alerts_count=len(all_alerts),
            recent_alerts=all_alerts[:5],
            teacher_id=teacher_user.id,
            teacher_name=teacher_user.full_name or "Educator",
            total_assigned_learners=total_learners,
            active_learners_count=active_learners_7d,
            total_completed_activities=total_activities_completed_7d,
            average_cohort_accuracy=cohort_average_accuracy_7d,
            pending_alerts=all_alerts[:5],
            recent_recommendations=[],
        )

    async def get_cohort_insights(self, teacher_user: User, days: int = 30) -> CohortInsights:
        """
        Aggregates performance telemetry and learner profiles across the teacher's cohort.
        """
        learners = await self._get_authorized_learners(teacher_user)
        cohort_size = len(learners)
        if cohort_size == 0:
            return CohortInsights(
                cohort_size=0,
                reporting_period_days=days,
                average_accuracy=0.0,
                average_assistance_level=0.0,
                modality_distribution={},
                mastery_distribution={"mastered": 0, "developing": 0, "emerging": 0, "struggling": 0},
                learner_summaries=[],
            )

        learner_ids = [l.id for l in learners]
        cutoff = datetime.now(UTC) - timedelta(days=days) if days > 0 else datetime.min.replace(tzinfo=UTC)

        stmt = (
            select(PerformanceEvent)
            .where(
                PerformanceEvent.learner_id.in_(learner_ids),
                PerformanceEvent.timestamp >= cutoff,
            )
            .order_by(PerformanceEvent.timestamp.asc())
        )
        res = await self.session.execute(stmt)
        events = list(res.scalars().all())

        # Overall averages
        avg_acc = round(sum(1 for e in events if e.correct) / len(events), 2) if events else 0.0
        avg_asst = round(sum(e.assistance_level for e in events) / len(events), 2) if events else 0.0

        # Modality distribution
        modality_counts: dict[str, int] = {}
        for e in events:
            mod_val = e.modality.value if hasattr(e.modality, "value") else str(e.modality)
            modality_counts[mod_val] = modality_counts.get(mod_val, 0) + 1

        total_mods = sum(modality_counts.values()) or 1
        modality_distribution = {
            mod: round(count / total_mods, 2) for mod, count in modality_counts.items()
        }

        # Compute per-learner summaries
        learner_summaries: list[CohortLearnerSummary] = []
        mastery_agg = {"mastered": 0, "developing": 0, "emerging": 0, "struggling": 0}

        # Cache alerts mapped by learner_id
        all_alerts = await self.get_intervention_alerts(teacher_user)
        alerts_by_learner: dict[uuid.UUID, int] = {}
        for al in all_alerts:
            alerts_by_learner[al.learner_id] = alerts_by_learner.get(al.learner_id, 0) + 1

        for learner in learners:
            l_events = [e for e in events if e.learner_id == learner.id]
            l_acc = round(sum(1 for e in l_events if e.correct) / len(l_events), 2) if l_events else 0.0
            l_asst = round(sum(e.assistance_level for e in l_events) / len(l_events), 2) if l_events else 0.0
            last_active = l_events[-1].timestamp if l_events else None

            # Get mastery count from AnalyticsService
            try:
                mast_rep = await self.analytics_service.get_learner_mastery(learner.id, teacher_user)
                mastered_count = sum(1 for st in mast_rep.objectives if st.status == "mastered")
                for st in mast_rep.objectives:
                    if st.status in mastery_agg:
                        mastery_agg[st.status] += 1
            except Exception:
                mastered_count = 0

            comm_pref = "verbal"
            if learner.profile and learner.profile.communication_preferences:
                comm_pref = learner.profile.communication_preferences.get("primary_mode", "verbal")

            learner_summaries.append(
                CohortLearnerSummary(
                    learner_id=learner.id,
                    display_name=learner.name,
                    learning_level=str(learner.learning_level),
                    age_group=str(learner.age_group) if hasattr(learner, "age_group") else "primary",
                    communication_preference=str(comm_pref),
                    activities_completed=sum(1 for e in l_events if e.completed),
                    completed_activities=sum(1 for e in l_events if e.completed),
                    total_events=len(l_events),
                    overall_accuracy=l_acc,
                    average_assistance=l_asst,
                    average_assistance_level=l_asst,
                    mastered_objectives_count=mastered_count,
                    in_progress_objectives_count=1,
                    last_active_at=last_active,
                    active_alert_count=alerts_by_learner.get(learner.id, 0),
                    active_alerts_count=alerts_by_learner.get(learner.id, 0),
                )
            )

        return CohortInsights(
            cohort_size=cohort_size,
            reporting_period_days=days,
            average_accuracy=avg_acc,
            average_assistance_level=avg_asst,
            modality_distribution=modality_distribution,
            mastery_distribution=mastery_agg,
            learner_summaries=learner_summaries,
            teacher_id=teacher_user.id,
            reporting_period=f"{days}_days",
            total_cohort_learners=cohort_size,
            active_learners_in_period=len([s for s in learner_summaries if s.activities_completed > 0]) or cohort_size,
            cohort_accuracy=avg_acc,
            cohort_avg_assistance_level=avg_asst,
            total_activities_completed=sum(1 for e in events if e.completed),
            mastery_status_counts=mastery_agg,
            learners=learner_summaries,
        )

    async def get_intervention_alerts(
        self, teacher_user: User, target_learner_id: uuid.UUID | None = None
    ) -> list[InterventionAlert]:
        """
        Evaluates deterministic pedagogical alert rules against recent telemetry.
        Strictly non-diagnostic; observes empirical difficulty and scaffolds teacher interventions.
        """
        if target_learner_id:
            target_learner = await self._check_learner_access(teacher_user, target_learner_id)
            learners = [target_learner]
        else:
            learners = await self._get_authorized_learners(teacher_user)

        alerts: list[InterventionAlert] = []
        now_dt = datetime.now(UTC)

        # Batch fetch performance events for learners over past 30 days
        cutoff_30d = now_dt - timedelta(days=30)
        learner_ids = [l.id for l in learners]
        if not learner_ids:
            return []

        stmt = (
            select(PerformanceEvent)
            .where(
                PerformanceEvent.learner_id.in_(learner_ids),
                PerformanceEvent.timestamp >= cutoff_30d,
            )
            .order_by(PerformanceEvent.timestamp.asc())
        )
        res = await self.session.execute(stmt)
        all_events = list(res.scalars().all())

        # Collect objectives map
        obj_ids = list({e.objective_id for e in all_events if e.objective_id is not None})
        objectives_map: dict[uuid.UUID, LearningObjective] = {}
        if obj_ids:
            obj_stmt = select(LearningObjective).where(LearningObjective.id.in_(obj_ids))
            obj_res = await self.session.execute(obj_stmt)
            objectives_map = {obj.id: obj for obj in obj_res.scalars().all()}

        for learner in learners:
            l_events = [e for e in all_events if e.learner_id == learner.id]

            # Rule 1: Inactivity (active in system, but no event in last 7 days)
            if l_events:
                last_event_time = l_events[-1].timestamp
                # Ensure timezone awareness
                if last_event_time.tzinfo is None:
                    last_event_time = last_event_time.replace(tzinfo=UTC)
                days_inactive = (now_dt - last_event_time).days
                if days_inactive >= 7:
                    alerts.append(
                        InterventionAlert(
                            alert_id=f"inact_{learner.id}_{days_inactive}d",
                            learner_id=learner.id,
                            learner_display_name=learner.name,
                            trigger_type=AlertTriggerType.inactivity,
                            severity=AlertSeverity.info,
                            message=f"No activity recorded in the last {days_inactive} days.",
                            recommended_action="Schedule a brief check-in session or assign an introductory review activity.",
                            evidence_context={"days_inactive": days_inactive, "last_active": last_event_time.isoformat()},
                            detected_at=now_dt,
                        )
                    )

            # Rule 2: High Assistance Reliance (avg assistance >= 2.0 over last 5 attempts)
            if len(l_events) >= 5:
                recent_5 = l_events[-5:]
                avg_recent_asst = sum(e.assistance_level for e in recent_5) / len(recent_5)
                if avg_recent_asst >= 2.0:
                    alerts.append(
                        InterventionAlert(
                            alert_id=f"asst_{learner.id}",
                            learner_id=learner.id,
                            learner_display_name=learner.name,
                            trigger_type=AlertTriggerType.high_assistance,
                            severity=AlertSeverity.action_required,
                            message=f"High assistance reliance detected (average level {avg_recent_asst:.1f}/3.0 across last 5 attempts).",
                            recommended_action="Consider lowering the target difficulty level or providing direct worked demonstrations.",
                            evidence_context={"average_assistance": round(avg_recent_asst, 2), "sample_size": len(recent_5)},
                            detected_at=now_dt,
                        )
                    )

            # Rule 3: Low Accuracy & Stalled Progress on Objective
            # Group events by objective_id
            events_by_obj: dict[uuid.UUID, list[PerformanceEvent]] = {}
            for e in l_events:
                if e.objective_id:
                    events_by_obj.setdefault(e.objective_id, []).append(e)

            for obj_id, o_events in events_by_obj.items():
                obj = objectives_map.get(obj_id)
                obj_title = "Learning Objective"
                if obj:
                    obj_title = obj.title.get("en", "Learning Objective") if isinstance(obj.title, dict) else str(obj.title)

                # Struggling on objective: >= 3 attempts with accuracy < 0.60
                if len(o_events) >= 3:
                    acc = sum(1 for e in o_events if e.correct) / len(o_events)
                    if acc < 0.60:
                        alerts.append(
                            InterventionAlert(
                                alert_id=f"strugg_{learner.id}_{obj_id}",
                                learner_id=learner.id,
                                learner_display_name=learner.name,
                                trigger_type=AlertTriggerType.low_accuracy,
                                severity=AlertSeverity.warning,
                                message=f"Low accuracy on objective '{obj_title}' ({acc * 100:.0f}% correct over {len(o_events)} attempts).",
                                recommended_action="Switch presentation modality or reinforce foundational prerequisite skills before re-attempting.",
                                evidence_context={"accuracy": round(acc, 2), "attempts": len(o_events), "objective_title": obj_title},
                                detected_at=now_dt,
                            )
                        )

                # Stalled mastery: >= 8 attempts without reaching mastery threshold
                if len(o_events) >= 8:
                    acc = sum(1 for e in o_events if e.correct) / len(o_events)
                    asst = sum(e.assistance_level for e in o_events) / len(o_events)
                    if not (acc >= 0.80 and asst <= 1.0):
                        alerts.append(
                            InterventionAlert(
                                alert_id=f"stall_{learner.id}_{obj_id}",
                                learner_id=learner.id,
                                learner_display_name=learner.name,
                                trigger_type=AlertTriggerType.stalled_mastery,
                                severity=AlertSeverity.warning,
                                message=f"Mastery plateau on objective '{obj_title}' after {len(o_events)} practice attempts.",
                                recommended_action="Review error patterns and engage a multi-sensory interactive approach.",
                                evidence_context={"attempts": len(o_events), "accuracy": round(acc, 2), "assistance": round(asst, 2)},
                                detected_at=now_dt,
                            )
                        )

        # Sort alerts: action_required first, then warning, then info
        severity_order = {AlertSeverity.action_required: 0, AlertSeverity.warning: 1, AlertSeverity.info: 2}
        alerts.sort(key=lambda a: severity_order.get(a.severity, 3))
        return alerts

    async def get_learner_iep_report(
        self, teacher_user: User, learner_id: uuid.UUID, days: int = 30
    ) -> IEPReport:
        """
        Compiles a structured Individualized Education Plan (IEP) progress report.
        Strictly preserves teacher ownership and outputs reproducible, audit-compliant educational data.
        """
        learner = await self._check_learner_access(teacher_user, learner_id)
        now_dt = datetime.now(UTC)
        start_dt = now_dt - timedelta(days=days) if days > 0 else None
        period_str = f"Last {days} Days" if days > 0 else "All Time"

        # Fetch learner analytics summary & mastery report
        summary = await self.analytics_service.get_learner_summary(learner_id, teacher_user)
        mastery = await self.analytics_service.get_learner_mastery(learner_id, teacher_user)

        # Modality efficacy from profile or summary
        modality_efficacy: dict[str, float] = {}
        for mm in summary.modality_breakdown:
            modality_efficacy[mm.modality] = mm.accuracy

        # Objectives progress breakdown
        objectives_progress: list[IEPObjectiveSummary] = []
        for obj_status in mastery.objectives:
            objectives_progress.append(
                IEPObjectiveSummary(
                    objective_id=obj_status.objective_id,
                    title=obj_status.objective_title,
                    attempts_count=obj_status.total_attempts,
                    accuracy=obj_status.accuracy,
                    average_assistance=obj_status.avg_assistance_level,
                    status=obj_status.status,
                )
            )

        # Generate evidence-based recommendations
        recommendations: list[str] = []
        if modality_efficacy:
            best_mod = max(modality_efficacy.items(), key=lambda x: x[1])
            recommendations.append(
                f"Prioritize '{best_mod[0].title()}' presentation modalities (demonstrating highest efficacy of {best_mod[1] * 100:.0f}%)."
            )
        if summary.avg_assistance_level > 1.5:
            recommendations.append(
                "Incorporate progressive scaffolding (Level 1 prompts) before offering direct answers to build pedagogical independence."
            )
        else:
            recommendations.append(
                "Maintain independent practice flow with minimal prompting to reinforce demonstrated autonomy."
            )

        mastered_count = sum(1 for o in objectives_progress if o.status == "mastered")
        struggling_count = sum(1 for o in objectives_progress if o.status == "struggling")
        if struggling_count > 0:
            recommendations.append(
                f"Schedule targeted intervention on {struggling_count} struggling objective(s) prior to advancing curriculum difficulty."
            )

        # Generate Printable Markdown
        learning_lvl = str(learner.learning_level)
        comm_pref = "verbal"
        teacher_notes = None
        if learner.profile and learner.profile.communication_preferences:
            comm_pref = str(learner.profile.communication_preferences.get("primary_mode", "verbal"))
            teacher_notes = learner.profile.communication_preferences.get("notes")

        markdown_lines = [
            f"# Individualized Education Plan (IEP) Progress Report",
            f"**Learner Reference:** {learner.name}  ",
            f"**Reporting Period:** {period_str} ({start_dt.strftime('%Y-%m-%d') if start_dt else 'Baseline'} to {now_dt.strftime('%Y-%m-%d')})  ",
            f"**Generated At:** {now_dt.strftime('%Y-%m-%d %H:%M UTC')}  ",
            f"**Learning Level:** {learning_lvl.capitalize()} | **Communication Mode:** {comm_pref.capitalize()}  ",
            f"",
            f"---",
            f"",
            f"## 1. Executive Performance Summary",
            f"- **Total Activities Completed:** {summary.completed_activities}",
            f"- **Overall Accuracy:** {summary.overall_accuracy * 100:.1f}%",
            f"- **Average Assistance Level:** {summary.avg_assistance_level:.2f} / 3.0 (Pedagogical Independence Scale)",
            f"- **Mastered Objectives:** {mastered_count} of {len(objectives_progress)} evaluated",
            f"",
            f"---",
            f"",
            f"## 2. Learning Objective Mastery Progress",
            f"| Objective Title | Attempts | Accuracy | Avg Assistance | Status |",
            f"| :--- | :---: | :---: | :---: | :---: |",
        ]

        for obj_p in objectives_progress:
            status_badge = obj_p.status.upper()
            markdown_lines.append(
                f"| {obj_p.title} | {obj_p.attempts_count} | {obj_p.accuracy * 100:.0f}% | {obj_p.average_assistance:.1f} | **{status_badge}** |"
            )

        markdown_lines.extend([
            f"",
            f"---",
            f"",
            f"## 3. Sensory Modality Efficacy",
            f"| Modality Channel | Efficacy (Accuracy) | Observations |",
            f"| :--- | :---: | :--- |",
        ])

        for mod, eff in modality_efficacy.items():
            rating = "Optimal" if eff >= 0.80 else ("Developing" if eff >= 0.60 else "Requires Support")
            markdown_lines.append(f"| {mod.capitalize()} | {eff * 100:.0f}% | {rating} |")

        markdown_lines.extend([
            f"",
            f"---",
            f"",
            f"## 4. Evidence-Based Pedagogical Recommendations",
        ])
        for rec in recommendations:
            markdown_lines.append(f"- {rec}")

        if teacher_notes:
            markdown_lines.extend([
                f"",
                f"---",
                f"",
                f"## 5. Teacher Observations & Accommodations",
                f"> {teacher_notes}",
            ])

        printable_markdown = "\n".join(markdown_lines)

        return IEPReport(
            report_id=f"iep_{learner.id}_{now_dt.strftime('%Y%m%d%H%M')}",
            generated_at=now_dt,
            reporting_period=period_str,
            start_date=start_dt,
            end_date=now_dt,
            learner_id=learner.id,
            learner_display_name=learner.name,
            learning_level=learning_lvl,
            communication_preference=comm_pref,
            teacher_notes=teacher_notes,
            total_activities_attempted=summary.completed_activities,
            overall_accuracy=summary.overall_accuracy,
            overall_assistance_average=summary.avg_assistance_level,
            modality_efficacy=modality_efficacy,
            objectives_progress=objectives_progress,
            teacher_recommendations=recommendations,
            printable_summary_markdown=printable_markdown,
        )
