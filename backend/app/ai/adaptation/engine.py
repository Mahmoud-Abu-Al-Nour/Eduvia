"""
Eduvia — Adaptive Decision Engine (Phase 8)

Deterministic pedagogical decision engine conforming strictly to:
- Eduvia Notes/03 - AI & Adaptive Learning/Adaptive Learning Intelligence Engine.md
- Eduvia Notes/03 - AI & Adaptive Learning/Strategy Engine.md
- docs/ai-architecture.md (Adaptation Logic & Explainability Format)

Gemini is NOT the decision maker. All pedagogical sequencing, difficulty tiers,
modality selection, and teaching strategies are derived deterministically from
curriculum prerequisite constraints, teacher overrides, and empirical performance data.
"""

from __future__ import annotations

import uuid
from typing import Any

from app.activities.schemas import ActivityType
from app.analytics.schemas import (
    LearnerAnalyticsSummary,
    LearnerMasteryReport,
    Modality,
    ObjectiveMasteryStatus,
    TeachingStrategy,
)
from app.curriculum.models import LearningObjective
from app.learners.models import LearnerProfile
from app.recommendations.schemas import (
    ConfidenceLevel,
    RecommendationDecision,
)


def _extract_localized_text(field_value: dict[str, Any] | str | None, lang: str = "en") -> str:
    """Safely extract localized text string from a dictionary or string."""
    if isinstance(field_value, dict):
        return str(
            field_value.get(lang) or field_value.get("en") or next(iter(field_value.values()), "")
        )
    return str(field_value or "")


class AdaptationEngine:
    """
    Core deterministic adaptation decision engine.

    Evaluates curriculum prerequisites, learner profile constraints, teacher overrides,
    and empirical telemetry metrics to select the optimal learning step.
    """

    @classmethod
    def evaluate_next_objective(
        cls,
        candidate_objectives: list[LearningObjective],
        mastery_report: LearnerMasteryReport | None,
        recent_objective_id: uuid.UUID | None = None,
    ) -> tuple[LearningObjective, list[str]]:
        """
        Traverse curriculum prerequisite graph to select the next optimal learning objective.

        Rules:
        1. An objective is locked and ineligible if ANY of its prerequisites is not mastered.
        2. Mastered objectives are excluded unless all candidates are mastered (reinforcement).
        3. Priority: In-progress objectives with satisfied prerequisites > Next unstarted objective
           in sequence > Safe baseline fallback.
        """
        applied_constraints: list[str] = []

        if not candidate_objectives:
            raise ValueError("Candidate objectives list cannot be empty.")

        # Build mastery lookup: objective_id -> ObjectiveMasteryStatus
        mastery_map: dict[uuid.UUID, ObjectiveMasteryStatus] = {}
        if mastery_report:
            mastery_map = {obj.objective_id: obj for obj in mastery_report.objectives}

        # Determine mastered objective IDs
        mastered_ids = {
            obj_id for obj_id, status in mastery_map.items() if status.status == "mastered"
        }

        # Step 1: Filter to candidates whose prerequisites are 100% mastered
        eligible_candidates: list[LearningObjective] = []
        for candidate in candidate_objectives:
            if not candidate.is_active:
                continue

            # Check all prerequisites
            prereq_ids = [p.id if hasattr(p, "id") else p for p in (candidate.prerequisites or [])]
            if all(p_id in mastered_ids for p_id in prereq_ids):
                eligible_candidates.append(candidate)
            else:
                applied_constraints.append(f"prereq_locked:{candidate.id}")

        if not eligible_candidates:
            # Fallback: if all prerequisites locked or circular, select earliest active
            applied_constraints.append("fallback_unlocked_candidate")
            eligible_candidates = [
                c for c in candidate_objectives if c.is_active
            ] or candidate_objectives

        # Step 2: Check struggle on recent objective (reinforcement check)
        if recent_objective_id and recent_objective_id in mastery_map:
            recent_status = mastery_map[recent_objective_id]
            # If learner struggled repeatedly (accuracy < 0.50, attempts >= 3), reinforce prereq
            if recent_status.total_attempts >= 3 and recent_status.accuracy < 0.50:
                recent_obj = next(
                    (c for c in candidate_objectives if c.id == recent_objective_id), None
                )
                if recent_obj and recent_obj.prerequisites:
                    reinforcement_target = recent_obj.prerequisites[0]
                    applied_constraints.append("reinforce_struggling_prerequisite")
                    return reinforcement_target, applied_constraints

        # Step 3: Candidate selection by learning state
        # 3a. In-progress objectives that are eligible
        in_progress_candidates = [
            c
            for c in eligible_candidates
            if c.id in mastery_map and mastery_map[c.id].status == "in_progress"
        ]
        if in_progress_candidates:
            # Prioritize the one with the most attempts or lowest index
            in_progress_candidates.sort(key=lambda c: (c.order_index, c.difficulty_level))
            applied_constraints.append("continue_in_progress_objective")
            return in_progress_candidates[0], applied_constraints

        # 3b. Unstarted objectives (not yet mastered)
        unstarted_candidates = [
            c
            for c in eligible_candidates
            if c.id not in mastered_ids
            and (c.id not in mastery_map or mastery_map[c.id].status == "not_started")
        ]
        if unstarted_candidates:
            unstarted_candidates.sort(key=lambda c: (c.order_index, c.difficulty_level))
            applied_constraints.append("advance_unstarted_objective")
            return unstarted_candidates[0], applied_constraints

        # 3c. All eligible objectives mastered -> choose highest difficulty for reinforcement
        eligible_candidates.sort(key=lambda c: c.difficulty_level, reverse=True)
        applied_constraints.append("reinforce_mastered_curriculum")
        return eligible_candidates[0], applied_constraints

    @classmethod
    def calibrate_difficulty(
        cls,
        base_difficulty: int,
        recent_status: ObjectiveMasteryStatus | None,
        profile: LearnerProfile | None,
    ) -> tuple[int, list[str]]:
        """
        Calibrate difficulty tier (1–5) based on teacher overrides and recent performance.

        Teacher lock strictly overrides empirical calculation.
        """
        applied_constraints: list[str] = []
        tier = max(1, min(5, base_difficulty))

        # Teacher Override Precedence
        if profile and profile.teacher_overrides:
            lock_diff = profile.teacher_overrides.get("lock_difficulty_level")
            if lock_diff is not None and isinstance(lock_diff, int):
                applied_constraints.append("teacher_locked_difficulty")
                return max(1, min(5, lock_diff)), applied_constraints

        if not recent_status or recent_status.total_attempts == 0:
            return tier, applied_constraints

        # Empirical calibration
        if recent_status.accuracy >= 0.80 and recent_status.avg_assistance_level <= 1.0:
            if tier < 5:
                tier += 1
                applied_constraints.append("empirical_difficulty_promoted")
        elif recent_status.accuracy < 0.50 or recent_status.avg_assistance_level >= 2.0:
            if tier > 1:
                tier -= 1
                applied_constraints.append("empirical_difficulty_scaffolded")

        return tier, applied_constraints

    @classmethod
    def select_modality_and_activity_type(
        cls,
        profile: LearnerProfile | None,
        analytics_summary: LearnerAnalyticsSummary | None,
    ) -> tuple[Modality, ActivityType, list[str]]:
        """
        Select sensory presentation modality and interaction format.

        Enforces the Adaptation Hierarchy:
        - Filters out excluded modalities from teacher constraints.
        - Requires >= 5 evidence events to switch away from profile default.
        - Selects modality with highest empirical accuracy and lowest assistance.
        """
        applied_constraints: list[str] = []

        # Available modalities
        allowed_modalities = [
            Modality.VISUAL,
            Modality.INTERACTIVE,
            Modality.READING,
            Modality.AUDIO,
            Modality.WRITING,
        ]

        # 1. Teacher Constraints Exclusions
        if profile and profile.teacher_constraints:
            excluded = [
                m.lower() for m in profile.teacher_constraints.get("excluded_modalities", [])
            ]
            if excluded:
                allowed_modalities = [
                    m for m in allowed_modalities if m.value.lower() not in excluded
                ]
                applied_constraints.append("teacher_excluded_modalities_applied")

            required = [
                m.lower() for m in profile.teacher_constraints.get("required_modalities", [])
            ]
            if required:
                req_filtered = [m for m in allowed_modalities if m.value.lower() in required]
                if req_filtered:
                    allowed_modalities = req_filtered
                    applied_constraints.append("teacher_required_modalities_applied")

        if not allowed_modalities:
            allowed_modalities = [Modality.VISUAL]

        # 2. Check Evidence Threshold (5+ events required to change modality)
        total_events = analytics_summary.total_events if analytics_summary else 0
        primary_modality = Modality.VISUAL

        # Inspect profile primary mode
        if profile and profile.communication_preferences:
            mode = profile.communication_preferences.get("primary_mode", "verbal")
            if mode in ("visual_assisted", "visual"):
                primary_modality = Modality.VISUAL
            elif mode == "written":
                primary_modality = Modality.READING
            elif mode == "augmentative":
                primary_modality = Modality.INTERACTIVE

        selected_modality = (
            primary_modality if primary_modality in allowed_modalities else allowed_modalities[0]
        )

        # 3. Empirical Selection if Evidence >= 5
        if analytics_summary and total_events >= 5 and analytics_summary.modality_breakdown:
            best_modality = selected_modality
            highest_score = -1.0

            for m_metrics in analytics_summary.modality_breakdown:
                try:
                    mod_enum = Modality(m_metrics.modality)
                except ValueError:
                    continue

                if mod_enum not in allowed_modalities:
                    continue

                # Efficacy score: 70% accuracy + 30% independence
                independence_score = max(0.0, 1.0 - (m_metrics.avg_assistance_level / 3.0))
                efficacy = (m_metrics.accuracy * 0.7) + (independence_score * 0.3)

                if efficacy > highest_score and m_metrics.total_events >= 2:
                    highest_score = efficacy
                    best_modality = mod_enum

            if best_modality != selected_modality:
                selected_modality = best_modality
                applied_constraints.append("empirical_modality_selected")
            else:
                applied_constraints.append("profile_modality_retained")
        else:
            applied_constraints.append("insufficient_evidence_default_modality")

        # 4. Map Modality to Compatible Activity Type
        activity_type = ActivityType.MATCHING
        if selected_modality == Modality.VISUAL:
            activity_type = ActivityType.VISUAL_IDENTIFICATION
        elif selected_modality == Modality.INTERACTIVE:
            activity_type = ActivityType.DRAG_DROP
        elif selected_modality == Modality.READING:
            activity_type = ActivityType.MULTIPLE_CHOICE
        elif selected_modality == Modality.AUDIO:
            activity_type = ActivityType.MULTIPLE_CHOICE
        elif selected_modality == Modality.WRITING:
            activity_type = ActivityType.ORDERING

        return selected_modality, activity_type, applied_constraints

    @classmethod
    def select_strategy(
        cls,
        profile: LearnerProfile | None,
        recent_status: ObjectiveMasteryStatus | None,
    ) -> tuple[TeachingStrategy, int, list[str]]:
        """
        Select teaching strategy and initial scaffolding tier.

        Teacher enforcement strictly takes precedence.
        """
        applied_constraints: list[str] = []

        # Teacher Override Precedence
        if profile and profile.teacher_overrides:
            enforced = profile.teacher_overrides.get("enforce_strategy")
            if enforced:
                try:
                    strategy_enum = TeachingStrategy(
                        enforced.lower().replace(" ", "_").replace("-", "_")
                    )
                    applied_constraints.append("teacher_enforced_strategy")
                    return strategy_enum, 1, applied_constraints
                except ValueError:
                    pass

        # Performance-based selection
        if not recent_status or recent_status.total_attempts == 0:
            return TeachingStrategy.STEP_BY_STEP, 1, applied_constraints

        if recent_status.avg_assistance_level >= 2.0:
            applied_constraints.append("high_assistance_demonstration_strategy")
            return TeachingStrategy.DEMONSTRATION, 2, applied_constraints

        if recent_status.accuracy < 0.50:
            applied_constraints.append("low_accuracy_simplification_strategy")
            return TeachingStrategy.SIMPLIFICATION, 2, applied_constraints

        if recent_status.accuracy >= 0.85:
            applied_constraints.append("high_accuracy_gradual_difficulty")
            return TeachingStrategy.GRADUAL_DIFFICULTY, 1, applied_constraints

        applied_constraints.append("standard_scaffolding_strategy")
        return TeachingStrategy.SCAFFOLDING, 1, applied_constraints

    @classmethod
    def build_recommendation(
        cls,
        learner_id: uuid.UUID,
        candidate_objectives: list[LearningObjective],
        profile: LearnerProfile | None,
        mastery_report: LearnerMasteryReport | None,
        analytics_summary: LearnerAnalyticsSummary | None,
        recent_objective_id: uuid.UUID | None = None,
        language: str = "en",
    ) -> RecommendationDecision:
        """
        Compute a complete deterministic recommendation decision with explainable rationale.
        """
        all_constraints: list[str] = []

        # 1. Objective Selection
        selected_obj, obj_constraints = cls.evaluate_next_objective(
            candidate_objectives=candidate_objectives,
            mastery_report=mastery_report,
            recent_objective_id=recent_objective_id,
        )
        all_constraints.extend(obj_constraints)

        # 2. Difficulty Calibration
        obj_status = None
        if mastery_report:
            obj_status = next(
                (o for o in mastery_report.objectives if o.objective_id == selected_obj.id), None
            )

        difficulty, diff_constraints = cls.calibrate_difficulty(
            base_difficulty=selected_obj.difficulty_level,
            recent_status=obj_status,
            profile=profile,
        )
        all_constraints.extend(diff_constraints)

        # 3. Modality & Activity Type
        modality, activity_type, mod_constraints = cls.select_modality_and_activity_type(
            profile=profile,
            analytics_summary=analytics_summary,
        )
        all_constraints.extend(mod_constraints)

        # 4. Teaching Strategy & Scaffolding
        strategy, scaffolding_tier, strat_constraints = cls.select_strategy(
            profile=profile,
            recent_status=obj_status,
        )
        all_constraints.extend(strat_constraints)

        # 5. Explainable Rationale & Confidence Rating
        total_events = analytics_summary.total_events if analytics_summary else 0
        overall_accuracy = analytics_summary.overall_accuracy if analytics_summary else 0.0
        avg_hints = analytics_summary.avg_hints_per_activity if analytics_summary else 0.0

        if total_events >= 10:
            confidence_level = ConfidenceLevel.HIGH
            confidence_score = min(1.0, 0.70 + (total_events * 0.01))
        elif total_events >= 3:
            confidence_level = ConfidenceLevel.MEDIUM
            confidence_score = 0.50 + (total_events * 0.03)
        else:
            confidence_level = ConfidenceLevel.LOW
            confidence_score = 0.30

        obj_title_str = _extract_localized_text(selected_obj.title, language)

        if total_events > 0:
            strat_name = strategy.value.replace("_", " ")
            rationale = (
                f"Selected '{obj_title_str}' using {modality.value} presentation "
                f"with {strat_name} strategy. Observed performance indicates an "
                f"overall accuracy of {overall_accuracy:.0%} with an average of "
                f"{avg_hints:.1f} hints required across {total_events} events."
            )
        else:
            rationale = (
                f"Selected foundational objective '{obj_title_str}' using "
                f"{modality.value} presentation. Baseline recommendation initiated "
                f"according to learner profile preferences with gentle scaffolding."
            )

        lesson_id = getattr(selected_obj, "lesson_id", None)
        unit_id = (
            getattr(selected_obj.lesson, "unit_id", None)
            if getattr(selected_obj, "lesson", None)
            else None
        )

        return RecommendationDecision(
            learner_id=learner_id,
            objective_id=selected_obj.id,
            objective_title=obj_title_str,
            lesson_id=lesson_id,
            unit_id=unit_id,
            difficulty_level=difficulty,
            recommended_modality=modality,
            recommended_activity_type=activity_type,
            recommended_strategy=strategy,
            scaffolding_tier=scaffolding_tier,
            rationale=rationale,
            confidence_level=confidence_level,
            confidence_score=round(confidence_score, 2),
            evidence_event_count=total_events,
            applied_constraints=list(dict.fromkeys(all_constraints)),
        )
