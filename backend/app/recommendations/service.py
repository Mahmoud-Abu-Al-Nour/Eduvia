"""
Eduvia — Recommendation Service (Phase 8)

Orchestrates adaptive recommendation generation, next-activity pipeline integration,
and empirical learner profile synchronization while strictly enforcing teacher multi-tenancy.
"""

from __future__ import annotations

import uuid
from typing import Any

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.activities.schemas import ActivityGenerateRequest
from app.activities.service import ActivityService
from app.ai.adaptation.engine import AdaptationEngine
from app.analytics.models import PerformanceEvent
from app.analytics.service import AnalyticsService
from app.core.errors import AuthorizationError, NotFoundError
from app.curriculum.models import LearningObjective
from app.learners.models import Learner, LearnerProfile
from app.recommendations.schemas import (
    AdaptiveNextActivityResponse,
    ProfileSyncResult,
    RecommendationDecision,
)
from app.users.models import User

logger = structlog.get_logger(__name__)


class RecommendationService:
    """
    Business logic for adaptive pedagogical recommendations and activity sequencing.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_authorized_learner_and_profile(
        self,
        learner_id: uuid.UUID,
        current_user: User,
    ) -> tuple[Learner, LearnerProfile | None]:
        """Verify learner existence and enforce teacher multi-tenant authorization."""
        stmt = select(Learner).where(Learner.id == learner_id)
        res = await self.session.execute(stmt)
        learner = res.scalars().first()

        if not learner:
            raise NotFoundError(f"Learner with id '{learner_id}' not found.")

        # Multi-tenant teacher ownership enforcement
        user_role = str(getattr(current_user, "role", ""))
        if user_role != "admin" and learner.teacher_id != current_user.id:
            logger.warning(
                "unauthorized_recommendation_access_attempt",
                learner_id=str(learner_id),
                user_id=str(current_user.id),
            )
            raise AuthorizationError(
                "You do not have permission to view recommendations for this learner."
            )

        profile_stmt = select(LearnerProfile).where(LearnerProfile.learner_id == learner_id)
        profile_res = await self.session.execute(profile_stmt)
        profile = profile_res.scalars().first()

        return learner, profile

    async def get_recommendation(
        self,
        learner_id: uuid.UUID,
        current_user: User,
        language: str = "en",
    ) -> RecommendationDecision:
        """
        Generate a deterministic pedagogical recommendation for the learner.

        Evaluates curriculum prerequisites, learner profile, and empirical analytics.
        """
        learner, profile = await self._get_authorized_learner_and_profile(learner_id, current_user)

        # 1. Fetch Analytics & Mastery from Phase 7 Service
        analytics_service = AnalyticsService(self.session)
        summary = await analytics_service.get_learner_summary(learner_id, current_user)
        mastery = await analytics_service.get_learner_mastery(learner_id, current_user)

        # 2. Fetch Active Curriculum Objectives with Prerequisites
        obj_stmt = (
            select(LearningObjective)
            .where(LearningObjective.is_active.is_(True))
            .order_by(LearningObjective.order_index.asc())
        )
        obj_res = await self.session.execute(obj_stmt)
        candidate_objectives = list(obj_res.scalars().all())

        if not candidate_objectives:
            raise NotFoundError("No active learning objectives found in curriculum to evaluate.")

        # 3. Discover most recent objective attempted
        recent_event_stmt = (
            select(PerformanceEvent.objective_id)
            .where(
                PerformanceEvent.learner_id == learner_id,
                PerformanceEvent.objective_id.isnot(None),
            )
            .order_by(PerformanceEvent.timestamp.desc())
            .limit(1)
        )
        recent_res = await self.session.execute(recent_event_stmt)
        recent_objective_id = recent_res.scalars().first()

        # 4. Run Deterministic Adaptation Engine
        decision = AdaptationEngine.build_recommendation(
            learner_id=learner.id,
            candidate_objectives=candidate_objectives,
            profile=profile,
            mastery_report=mastery,
            analytics_summary=summary,
            recent_objective_id=recent_objective_id,
            language=language,
        )

        logger.info(
            "adaptive_recommendation_computed",
            learner_id=str(learner_id),
            objective_id=str(decision.objective_id),
            modality=decision.recommended_modality.value,
            strategy=decision.recommended_strategy.value,
            confidence=decision.confidence_level.value,
        )
        return decision

    async def get_next_activity(
        self,
        learner_id: uuid.UUID,
        current_user: User,
        language: str = "en",
    ) -> AdaptiveNextActivityResponse:
        """
        Compute an adaptive decision and immediately invoke Phase 4 ActivityService
        to generate the next recommended activity.
        """
        decision = await self.get_recommendation(learner_id, current_user, language=language)

        # Invoke Phase 4 Activity Generation Engine
        activity_service = ActivityService(self.session)
        gen_request = ActivityGenerateRequest(
            objective_id=decision.objective_id,
            learner_id=decision.learner_id,
            activity_type=decision.recommended_activity_type,
            difficulty_level=decision.difficulty_level,
            language=language,
        )

        gen_response = await activity_service.generate_activity(gen_request, current_user)

        return AdaptiveNextActivityResponse(
            decision=decision,
            activity=gen_response.activity,
            fallback_used=gen_response.fallback_used,
            generation_source=gen_response.generation_source,
        )

    async def sync_learner_profile_effectiveness(
        self,
        learner_id: uuid.UUID,
        current_user: User,
    ) -> ProfileSyncResult:
        """
        Synchronize LearnerProfile modality and strategy effectiveness from historical events.

        Derives empirical observed counts and success ratings without corrupting telemetry.
        """
        learner, profile = await self._get_authorized_learner_and_profile(learner_id, current_user)

        if not profile:
            raise NotFoundError(f"LearnerProfile for learner '{learner_id}' not found.")

        # Query all historical performance events
        events_stmt = select(PerformanceEvent).where(PerformanceEvent.learner_id == learner_id)
        events_res = await self.session.execute(events_stmt)
        events = list(events_res.scalars().all())

        # Modality mappings
        modality_keys = {
            "visual": "Visual",
            "reading": "Reading/Text",
            "writing": "Writing",
            "audio": "Audio",
            "interactive": "Interactive",
        }
        updated_modalities: dict[str, Any] = dict(profile.modality_effectiveness or {})

        for mod_key, mod_title in modality_keys.items():
            mod_events = [e for e in events if getattr(e, "modality", None) == mod_key]
            count = len(mod_events)
            if count > 0:
                acc = sum(1 for e in mod_events if e.correct) / count
                updated_modalities[mod_title] = {
                    "observed_count": count,
                    "engagement_rating": round(acc, 2),
                }

        # Strategy mappings
        strategy_keys = {
            "step_by_step": "Step-by-Step",
            "repetition": "Repetition",
            "scaffolding": "Scaffolding",
            "prompting": "Prompting",
            "simplification": "Simplification",
            "demonstration": "Demonstration",
            "positive_reinforcement": "Positive Reinforcement",
            "gradual_difficulty": "Gradual Difficulty",
        }
        updated_strategies: dict[str, Any] = dict(profile.strategy_effectiveness or {})

        for strat_key, strat_title in strategy_keys.items():
            strat_events = [e for e in events if getattr(e, "teaching_strategy", None) == strat_key]
            count = len(strat_events)
            if count > 0:
                acc = sum(1 for e in strat_events if e.correct) / count
                updated_strategies[strat_title] = {
                    "observed_count": count,
                    "success_rate": round(acc, 2),
                }

        # Update profile
        profile.modality_effectiveness = updated_modalities
        profile.strategy_effectiveness = updated_strategies
        await self.session.commit()

        logger.info(
            "learner_profile_effectiveness_synced",
            learner_id=str(learner_id),
            events_processed=len(events),
        )

        return ProfileSyncResult(
            learner_id=learner_id,
            updated_modalities=updated_modalities,
            updated_strategies=updated_strategies,
            total_events_processed=len(events),
        )
