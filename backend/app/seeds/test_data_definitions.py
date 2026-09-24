"""
Eduvia — Deterministic Test Data Definitions for Development & QA

Provides 20+ realistic educational student scenarios, 2 distinct cohorts,
curriculum objectives, and comprehensive performance telemetry spanning 60 days.

Deterministic IDs ensure idempotent seeding, safe removal, and zero impact on
production or core demo entities (admin@eduvia.app, teacher@eduvia.app, Tariq Al-Mansoor).
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

# Fixed namespace UUID for Eduvia development test data
TEST_NAMESPACE = uuid.UUID("e0d00000-0000-0000-0000-000000000001")


def get_test_uuid(identifier: str) -> uuid.UUID:
    """Generate a deterministic UUID from a scenario identifier."""
    return uuid.uuid5(TEST_NAMESPACE, identifier)


# Teacher / Cohort Identifiers
COHORT_A_TEACHER_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")
COHORT_A_TEACHER_EMAIL = "teacher@eduvia.app"
COHORT_A_TEACHER_NAME = "Alice Teacher"
COHORT_A_NAME = "Cohort A - Early Numeracy Alpha"

COHORT_B_TEACHER_ID = get_test_uuid("user.teacher.cohort_b")
COHORT_B_TEACHER_EMAIL = "teacher.cohortb@eduvia.local"
COHORT_B_TEACHER_NAME = "Marcus Cohort-B Teacher"
COHORT_B_NAME = "Cohort B - Foundational Development Beta"

# Curriculum Identifiers
CURRICULUM_ID = uuid.UUID("33333333-3333-3333-3333-333333333333")
SUBJECT_ID = uuid.UUID("44444444-4444-4444-4444-444444444444")
UNIT_ID = uuid.UUID("55555555-5555-5555-5555-555555555555")
LESSON_ID = uuid.UUID("66666666-6666-6666-6666-666666666666")

OBJ_1_5_ID = uuid.UUID("77777777-7777-7777-7777-777777777777")
OBJ_6_10_ID = uuid.UUID("88888888-8888-8888-8888-888888888888")
OBJ_PATTERNS_ID = get_test_uuid("curriculum.obj.patterns")


@dataclass
class TelemetryTemplate:
    """Blueprint for generating realistic telemetry events over time."""
    days_ago: int
    objective_id: uuid.UUID
    activity_type: str  # matching, ordering, drag_drop, visual_identification, multiple_choice
    modality: str       # visual, interactive, audio, kinesthetic
    strategy: str       # step_by_step, chunking, visual_cueing, scaffolded
    correct: bool
    score: float
    assistance_level: int  # 0=independent, 1=hint, 2=moderate, 3=high
    hints_used: int
    response_time_ms: int
    difficulty: int = 1
    completed: bool = True


@dataclass
class LearnerScenarioDefinition:
    """Complete specification of a test learner scenario."""
    key: str
    name: str
    email: str
    cohort_key: str  # "cohort_a" or "cohort_b"
    teacher_id: uuid.UUID
    age_group: str   # primary, secondary, early_childhood
    learning_level: str  # beginner, intermediate, advanced
    summary_description: str
    expected_mastery: str
    expected_engagement: str
    expected_adaptive_behavior: str
    
    # Profile details
    communication_primary_mode: str
    receptive_preferences: list[str]
    expressive_preferences: list[str]
    numeracy_stage: str
    literacy_stage: str
    attention_span_minutes: int
    strengths: list[str]
    focus_areas: list[str]
    sensory_accommodations: list[str]
    pacing: str
    teacher_notes: str
    modality_effectiveness: dict[str, float]
    
    # Telemetry events generator plan
    telemetry_events: list[TelemetryTemplate] = field(default_factory=list)

    @property
    def learner_id(self) -> uuid.UUID:
        return get_test_uuid(f"learner.{self.key}")

    @property
    def profile_id(self) -> uuid.UUID:
        return get_test_uuid(f"profile.{self.key}")


def generate_learner_definitions(now: datetime | None = None) -> list[LearnerScenarioDefinition]:
    """
    Constructs the 20 test student definitions with calibrated pedagogical scenarios.
    """
    if now is None:
        now = datetime.now(UTC)

    students: list[LearnerScenarioDefinition] = []

    # ──────────────────────────────────────────────────────────────────────────
    # 1. EXCELLENT (Cohort A)
    # Mastery: 95%+, High scores, minimal assistance, very recent activity.
    # Adaptive: Advance to higher difficulty tier (Tier 3) with independent pacing.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="excellent",
            name="Test Student - Excellent",
            email="test.excellent@eduvia.local",
            cohort_key="cohort_a",
            teacher_id=COHORT_A_TEACHER_ID,
            age_group="primary",
            learning_level="advanced",
            summary_description="Consistently demonstrates outstanding numerical reasoning and fast autonomous problem solving.",
            expected_mastery="90-100% across all evaluated objectives",
            expected_engagement="High and sustained across the past 14 days",
            expected_adaptive_behavior="Advancement to higher difficulty tier 3 with low scaffolding",
            communication_primary_mode="verbal",
            receptive_preferences=["verbal", "visual_cues"],
            expressive_preferences=["verbal", "tactile"],
            numeracy_stage="advanced",
            literacy_stage="fluent",
            attention_span_minutes=25,
            strengths=["rapid number pattern recognition", "high confidence", "autonomous completion"],
            focus_areas=["multi-digit challenge puzzles"],
            sensory_accommodations=["minimal_distractions"],
            pacing="accelerated",
            teacher_notes="Exceptional grasp of foundational math. Ready for enriched and independent practice.",
            modality_effectiveness={"visual": 0.95, "interactive": 0.92, "audio": 0.85, "kinesthetic": 0.90},
            telemetry_events=[
                TelemetryTemplate(days_ago=14, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=1.0, assistance_level=0, hints_used=0, response_time_ms=1800),
                TelemetryTemplate(days_ago=12, objective_id=OBJ_1_5_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=True, score=1.0, assistance_level=0, hints_used=0, response_time_ms=1950),
                TelemetryTemplate(days_ago=10, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="interactive", strategy="visual_cueing", correct=True, score=0.95, assistance_level=0, hints_used=0, response_time_ms=2100),
                TelemetryTemplate(days_ago=8, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=1.0, assistance_level=0, hints_used=0, response_time_ms=1750),
                TelemetryTemplate(days_ago=5, objective_id=OBJ_6_10_ID, activity_type="visual_identification", modality="visual", strategy="step_by_step", correct=True, score=1.0, assistance_level=0, hints_used=0, response_time_ms=1600),
                TelemetryTemplate(days_ago=3, objective_id=OBJ_PATTERNS_ID, activity_type="ordering", modality="interactive", strategy="chunking", correct=True, score=0.92, assistance_level=0, hints_used=0, response_time_ms=2200),
                TelemetryTemplate(days_ago=1, objective_id=OBJ_PATTERNS_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=1.0, assistance_level=0, hints_used=0, response_time_ms=1800),
                TelemetryTemplate(days_ago=0, objective_id=OBJ_PATTERNS_ID, activity_type="drag_drop", modality="interactive", strategy="chunking", correct=True, score=1.0, assistance_level=0, hints_used=0, response_time_ms=1700),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 2. HIGH PERFORMER (Cohort A)
    # Mastery: 85-90%, consistent performance, minor mistakes on complex items.
    # Adaptive: Recommend advanced sequencing with brief hints on multi-step tasks.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="highperformer",
            name="Test Student - High Performer",
            email="test.highperformer@eduvia.local",
            cohort_key="cohort_a",
            teacher_id=COHORT_A_TEACHER_ID,
            age_group="primary",
            learning_level="intermediate",
            summary_description="Strong, steady student who masters topics promptly with occasional self-corrected errors.",
            expected_mastery="85-90% accuracy across standard objectives",
            expected_engagement="High active frequency (7+ sessions in past 2 weeks)",
            expected_adaptive_behavior="Advance through curriculum with standard progression",
            communication_primary_mode="verbal",
            receptive_preferences=["verbal", "visual_cues"],
            expressive_preferences=["verbal"],
            numeracy_stage="intermediate",
            literacy_stage="developing",
            attention_span_minutes=20,
            strengths=["consistent work ethic", "good retention"],
            focus_areas=["multi-step instructions"],
            sensory_accommodations=["structured_checklists"],
            pacing="standard",
            teacher_notes="Reliable learner. Thrives when allowed to work at their own steady pace.",
            modality_effectiveness={"visual": 0.88, "interactive": 0.85, "audio": 0.78, "kinesthetic": 0.80},
            telemetry_events=[
                TelemetryTemplate(days_ago=13, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.90, assistance_level=0, hints_used=0, response_time_ms=2400),
                TelemetryTemplate(days_ago=11, objective_id=OBJ_1_5_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=True, score=0.88, assistance_level=1, hints_used=1, response_time_ms=2800),
                TelemetryTemplate(days_ago=9, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="interactive", strategy="visual_cueing", correct=True, score=0.90, assistance_level=0, hints_used=0, response_time_ms=2500),
                TelemetryTemplate(days_ago=6, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.95, assistance_level=0, hints_used=0, response_time_ms=2100),
                TelemetryTemplate(days_ago=4, objective_id=OBJ_PATTERNS_ID, activity_type="visual_identification", modality="visual", strategy="step_by_step", correct=True, score=0.85, assistance_level=1, hints_used=1, response_time_ms=2600),
                TelemetryTemplate(days_ago=1, objective_id=OBJ_PATTERNS_ID, activity_type="ordering", modality="interactive", strategy="chunking", correct=True, score=0.90, assistance_level=0, hints_used=0, response_time_ms=2300),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 3. IMPROVING (Cohort A)
    # Started at 0.50 accuracy 3 weeks ago; recent 7 days average >0.85.
    # Adaptive: Positive reinforcement, maintain momentum with scaffolded difficulty 2.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="improving",
            name="Test Student - Improving",
            email="test.improving@eduvia.local",
            cohort_key="cohort_a",
            teacher_id=COHORT_A_TEACHER_ID,
            age_group="primary",
            learning_level="beginner",
            summary_description="Demonstrates remarkable recent growth following introduction of visual scaffolding.",
            expected_mastery="Recent accuracy >85%, lifetime average ~72%",
            expected_engagement="Steadily increasing over past 10 days",
            expected_adaptive_behavior="Reinforce recent breakthrough without overwhelming",
            communication_primary_mode="visual_cues",
            receptive_preferences=["visual_cues", "tactile"],
            expressive_preferences=["verbal", "tactile"],
            numeracy_stage="emerging",
            literacy_stage="emerging",
            attention_span_minutes=15,
            strengths=["tactile engagement", "perseverance"],
            focus_areas=["transitioning to higher numbers"],
            sensory_accommodations=["high_contrast_visuals", "calm_pacing"],
            pacing="moderate",
            teacher_notes="Major progress after adapting presentation to visual matching with low distractor counts.",
            modality_effectiveness={"visual": 0.85, "interactive": 0.80, "audio": 0.50, "kinesthetic": 0.75},
            telemetry_events=[
                # Historical lower performance
                TelemetryTemplate(days_ago=22, objective_id=OBJ_1_5_ID, activity_type="matching", modality="audio", strategy="direct_instruction", correct=False, score=0.40, assistance_level=3, hints_used=3, response_time_ms=7500),
                TelemetryTemplate(days_ago=20, objective_id=OBJ_1_5_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=False, score=0.50, assistance_level=2, hints_used=2, response_time_ms=6800),
                TelemetryTemplate(days_ago=16, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="visual_cueing", correct=True, score=0.65, assistance_level=2, hints_used=2, response_time_ms=5200),
                # Recent improvement phase
                TelemetryTemplate(days_ago=6, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="visual_cueing", correct=True, score=0.85, assistance_level=1, hints_used=1, response_time_ms=3400),
                TelemetryTemplate(days_ago=4, objective_id=OBJ_1_5_ID, activity_type="drag_drop", modality="visual", strategy="step_by_step", correct=True, score=0.90, assistance_level=0, hints_used=0, response_time_ms=2900),
                TelemetryTemplate(days_ago=2, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="visual_cueing", correct=True, score=0.85, assistance_level=1, hints_used=1, response_time_ms=3200),
                TelemetryTemplate(days_ago=0, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="visual", strategy="step_by_step", correct=True, score=0.90, assistance_level=0, hints_used=0, response_time_ms=2700),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 4. STRUGGLING (Cohort B)
    # Low accuracy (45%), high assistance reliance (Level 2-3), incomplete attempts.
    # Adaptive: Recommend foundational prerequisite review with high visual scaffolding.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="struggling",
            name="Test Student - Struggling",
            email="test.struggling@eduvia.local",
            cohort_key="cohort_b",
            teacher_id=COHORT_B_TEACHER_ID,
            age_group="primary",
            learning_level="beginner",
            summary_description="Requires significant pedagogical assistance and frequently relies on full scaffolding.",
            expected_mastery="Low mastery (40-50%), elevated error rate",
            expected_engagement="Active practice but high frustration/assistance reliance",
            expected_adaptive_behavior="Recommend remediation on prerequisite Objective 1-5 with Level 2 assistance",
            communication_primary_mode="tactile",
            receptive_preferences=["tactile", "visual_cues"],
            expressive_preferences=["tactile"],
            numeracy_stage="emerging",
            literacy_stage="pre-emergent",
            attention_span_minutes=10,
            strengths=["willingness to try", "responds well to encouraging sounds"],
            focus_areas=["symbol-to-quantity mapping", "assistance reduction"],
            sensory_accommodations=["large_touch_targets", "reduced_distractor_count"],
            pacing="deliberate",
            teacher_notes="Needs patient, error-free learning steps. Struggles with symbolic digits 6 to 10.",
            modality_effectiveness={"visual": 0.55, "interactive": 0.60, "audio": 0.35, "kinesthetic": 0.65},
            telemetry_events=[
                TelemetryTemplate(days_ago=14, objective_id=OBJ_1_5_ID, activity_type="matching", modality="interactive", strategy="scaffolded", correct=False, score=0.45, assistance_level=3, hints_used=3, response_time_ms=8900),
                TelemetryTemplate(days_ago=12, objective_id=OBJ_1_5_ID, activity_type="drag_drop", modality="interactive", strategy="scaffolded", correct=True, score=0.55, assistance_level=2, hints_used=2, response_time_ms=7800),
                TelemetryTemplate(days_ago=9, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=False, score=0.35, assistance_level=3, hints_used=4, response_time_ms=9500),
                TelemetryTemplate(days_ago=6, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="interactive", strategy="scaffolded", correct=False, score=0.40, assistance_level=3, hints_used=3, response_time_ms=8400),
                TelemetryTemplate(days_ago=3, objective_id=OBJ_6_10_ID, activity_type="ordering", modality="interactive", strategy="scaffolded", correct=False, score=0.45, assistance_level=2, hints_used=2, response_time_ms=7900),
                TelemetryTemplate(days_ago=1, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="visual_cueing", correct=True, score=0.50, assistance_level=2, hints_used=2, response_time_ms=6800),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 5. AT RISK (Cohort B)
    # Long inactivity (22 days), low historic accuracy, stalled mastery.
    # Triggers: Inactivity threshold + high assistance alerts.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="atrisk",
            name="Test Student - At Risk",
            email="test.atrisk@eduvia.local",
            cohort_key="cohort_b",
            teacher_id=COHORT_B_TEACHER_ID,
            age_group="primary",
            learning_level="beginner",
            summary_description="Shows persistent difficulty coupled with multi-week inactivity, triggering pedagogical intervention alerts.",
            expected_mastery="Below 40% mastery, stalled progress",
            expected_engagement="Zero engagement in last 21+ days",
            expected_adaptive_behavior="Flag for teacher intervention, recommend low-stakes re-engagement activity",
            communication_primary_mode="visual_cues",
            receptive_preferences=["visual_cues"],
            expressive_preferences=["tactile"],
            numeracy_stage="emerging",
            literacy_stage="pre-emergent",
            attention_span_minutes=8,
            strengths=["visual interest in colorful cards"],
            focus_areas=["attendance consistency", "concept retention"],
            sensory_accommodations=["high_contrast", "short_sessions"],
            pacing="deliberate",
            teacher_notes="At risk of disengagement. Last active over 3 weeks ago after struggling on counting 6-10.",
            modality_effectiveness={"visual": 0.45, "interactive": 0.40, "audio": 0.30, "kinesthetic": 0.45},
            telemetry_events=[
                TelemetryTemplate(days_ago=26, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=False, score=0.40, assistance_level=3, hints_used=3, response_time_ms=9800),
                TelemetryTemplate(days_ago=24, objective_id=OBJ_1_5_ID, activity_type="drag_drop", modality="interactive", strategy="scaffolded", correct=False, score=0.35, assistance_level=3, hints_used=4, response_time_ms=10500),
                TelemetryTemplate(days_ago=22, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=False, score=0.30, assistance_level=3, hints_used=3, response_time_ms=11200),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 6. INACTIVE (Cohort B)
    # Performed decently (70% accuracy) 45 days ago, then zero recent sessions.
    # Tests historical retention metrics vs active cohort distinction.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="inactive",
            name="Test Student - Inactive",
            email="test.inactive@eduvia.local",
            cohort_key="cohort_b",
            teacher_id=COHORT_B_TEACHER_ID,
            age_group="secondary",
            learning_level="intermediate",
            summary_description="Previously active student with good baseline performance who has not accessed the platform in over 40 days.",
            expected_mastery="Solid historical mastery (70-75%), but decaying recency",
            expected_engagement="Zero sessions in last 30 days",
            expected_adaptive_behavior="Propose light warm-up activity to reassess retention baseline",
            communication_primary_mode="verbal",
            receptive_preferences=["verbal", "visual_cues"],
            expressive_preferences=["verbal"],
            numeracy_stage="intermediate",
            literacy_stage="fluent",
            attention_span_minutes=20,
            strengths=["prior foundational knowledge"],
            focus_areas=["re-establishing platform engagement habit"],
            sensory_accommodations=["standard"],
            pacing="standard",
            teacher_notes="Student completed initial modules last month but has had extended absence.",
            modality_effectiveness={"visual": 0.75, "interactive": 0.70, "audio": 0.65, "kinesthetic": 0.60},
            telemetry_events=[
                TelemetryTemplate(days_ago=52, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.80, assistance_level=1, hints_used=1, response_time_ms=3100),
                TelemetryTemplate(days_ago=48, objective_id=OBJ_1_5_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=True, score=0.75, assistance_level=1, hints_used=1, response_time_ms=3400),
                TelemetryTemplate(days_ago=44, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="interactive", strategy="visual_cueing", correct=True, score=0.70, assistance_level=1, hints_used=2, response_time_ms=3900),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 7. NEW (Cohort A)
    # Enrolled 2 days ago; only 2 completed onboarding activities.
    # Tests newly enrolled profile state, low total event count.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="new",
            name="Test Student - New",
            email="test.new@eduvia.local",
            cohort_key="cohort_a",
            teacher_id=COHORT_A_TEACHER_ID,
            age_group="early_childhood",
            learning_level="beginner",
            summary_description="Recently registered student currently undergoing initial pedagogical intake and orientation.",
            expected_mastery="Emerging baseline across initial 2 exercises",
            expected_engagement="Recent onboarding activity only",
            expected_adaptive_behavior="Deliver diagnostic foundational activities",
            communication_primary_mode="visual_cues",
            receptive_preferences=["visual_cues", "verbal"],
            expressive_preferences=["tactile"],
            numeracy_stage="emerging",
            literacy_stage="emerging",
            attention_span_minutes=12,
            strengths=["eager to engage with interactive touch interface"],
            focus_areas=["baseline numeracy assessment"],
            sensory_accommodations=["gentle_audio_reinforcement"],
            pacing="moderate",
            teacher_notes="Enrolled this week. Completed initial orientation without hesitation.",
            modality_effectiveness={"visual": 0.85, "interactive": 0.80, "audio": 0.70, "kinesthetic": 0.75},
            telemetry_events=[
                TelemetryTemplate(days_ago=1, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.85, assistance_level=1, hints_used=1, response_time_ms=3600),
                TelemetryTemplate(days_ago=0, objective_id=OBJ_1_5_ID, activity_type="visual_identification", modality="visual", strategy="step_by_step", correct=True, score=0.90, assistance_level=0, hints_used=0, response_time_ms=2900),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 8. NO ACTIVITY (Cohort B)
    # Completely empty activity record (0 attempts, 0 telemetry events).
    # Critical edge case testing zero-division, empty states, and clean cards.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="noactivity",
            name="Test Student - No Activity",
            email="test.noactivity@eduvia.local",
            cohort_key="cohort_b",
            teacher_id=COHORT_B_TEACHER_ID,
            age_group="primary",
            learning_level="beginner",
            summary_description="Student enrolled in cohort with zero recorded practice attempts or telemetry events.",
            expected_mastery="0% (Empty state gracefully handled)",
            expected_engagement="Zero sessions recorded",
            expected_adaptive_behavior="Recommend initial onboarding practice session",
            communication_primary_mode="verbal",
            receptive_preferences=["verbal"],
            expressive_preferences=["verbal"],
            numeracy_stage="emerging",
            literacy_stage="emerging",
            attention_span_minutes=15,
            strengths=["pending initial evaluation"],
            focus_areas=["pending initial evaluation"],
            sensory_accommodations=["standard"],
            pacing="standard",
            teacher_notes="Awaiting initial session in classroom learning lab.",
            modality_effectiveness={},
            telemetry_events=[],  # Explicitly ZERO telemetry
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 9. LOW ENGAGEMENT (Cohort A)
    # Sound mastery (82% accuracy) when they show up, but only 3 sessions in a month.
    # Tests engagement alerts on capable students.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="lowengagement",
            name="Test Student - Low Engagement",
            email="test.lowengagement@eduvia.local",
            cohort_key="cohort_a",
            teacher_id=COHORT_A_TEACHER_ID,
            age_group="primary",
            learning_level="intermediate",
            summary_description="Displays good comprehension during practice but accesses the system infrequently.",
            expected_mastery="80-85% accuracy on completed activities",
            expected_engagement="Low frequency (sparse events over 30 days)",
            expected_adaptive_behavior="Recommend concise, high-interest challenge to increase visit frequency",
            communication_primary_mode="verbal",
            receptive_preferences=["verbal", "visual_cues"],
            expressive_preferences=["verbal"],
            numeracy_stage="intermediate",
            literacy_stage="developing",
            attention_span_minutes=18,
            strengths=["sound conceptual foundation", "quick execution when logged in"],
            focus_areas=["routine practice cadence"],
            sensory_accommodations=["gamified_feedback"],
            pacing="standard",
            teacher_notes="Student performs well but needs encouragement to maintain daily habit.",
            modality_effectiveness={"visual": 0.82, "interactive": 0.85, "audio": 0.75, "kinesthetic": 0.80},
            telemetry_events=[
                TelemetryTemplate(days_ago=25, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.85, assistance_level=1, hints_used=1, response_time_ms=2500),
                TelemetryTemplate(days_ago=14, objective_id=OBJ_1_5_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=True, score=0.80, assistance_level=1, hints_used=1, response_time_ms=2700),
                TelemetryTemplate(days_ago=4, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="interactive", strategy="visual_cueing", correct=True, score=0.82, assistance_level=1, hints_used=1, response_time_ms=2600),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 10. HIGH ENGAGEMENT / LOW MASTERY (Cohort B)
    # Highest attempt count in cohort (25 events), but accuracy is only 46%.
    # Proves engagement != mastery. Triggers repetitive error interventions.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="highengagelowmastery",
            name="Test Student - High Engagement Low Mastery",
            email="test.highengagelowmastery@eduvia.local",
            cohort_key="cohort_b",
            teacher_id=COHORT_B_TEACHER_ID,
            age_group="primary",
            learning_level="beginner",
            summary_description="Practices very frequently with high effort, yet struggles to break through 50% accuracy threshold.",
            expected_mastery="Low (40-48%) despite massive volume of attempts",
            expected_engagement="Very high (20+ events in past 3 weeks)",
            expected_adaptive_behavior="Switch pedagogical strategy from drill-and-practice to multi-sensory concrete modeling",
            communication_primary_mode="visual_cues",
            receptive_preferences=["visual_cues", "tactile"],
            expressive_preferences=["tactile", "verbal"],
            numeracy_stage="emerging",
            literacy_stage="emerging",
            attention_span_minutes=14,
            strengths=["outstanding persistence", "positive attitude towards practice"],
            focus_areas=["retaining distinction between similar digits (6 vs 9)"],
            sensory_accommodations=["high_contrast_visuals", "tactile_audio_sync"],
            pacing="deliberate",
            teacher_notes="Extremely motivated. Needs pedagogical adjustment because repetitive trials are not yielding mastery.",
            modality_effectiveness={"visual": 0.50, "interactive": 0.45, "audio": 0.35, "kinesthetic": 0.60},
            telemetry_events=[
                TelemetryTemplate(days_ago=18, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=False, score=0.45, assistance_level=2, hints_used=3, response_time_ms=5400),
                TelemetryTemplate(days_ago=16, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.55, assistance_level=2, hints_used=2, response_time_ms=5100),
                TelemetryTemplate(days_ago=14, objective_id=OBJ_1_5_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=False, score=0.40, assistance_level=3, hints_used=3, response_time_ms=6200),
                TelemetryTemplate(days_ago=12, objective_id=OBJ_1_5_ID, activity_type="drag_drop", modality="interactive", strategy="step_by_step", correct=False, score=0.45, assistance_level=2, hints_used=2, response_time_ms=5800),
                TelemetryTemplate(days_ago=10, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=False, score=0.35, assistance_level=3, hints_used=4, response_time_ms=7100),
                TelemetryTemplate(days_ago=8, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=False, score=0.40, assistance_level=3, hints_used=3, response_time_ms=6900),
                TelemetryTemplate(days_ago=6, objective_id=OBJ_6_10_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=False, score=0.45, assistance_level=2, hints_used=3, response_time_ms=6500),
                TelemetryTemplate(days_ago=4, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="interactive", strategy="scaffolded", correct=False, score=0.50, assistance_level=2, hints_used=2, response_time_ms=6100),
                TelemetryTemplate(days_ago=2, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="visual_cueing", correct=True, score=0.55, assistance_level=2, hints_used=2, response_time_ms=5900),
                TelemetryTemplate(days_ago=0, objective_id=OBJ_6_10_ID, activity_type="visual_identification", modality="visual", strategy="visual_cueing", correct=False, score=0.48, assistance_level=2, hints_used=3, response_time_ms=5700),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 11. HIGH MASTERY / LOW ENGAGEMENT (Cohort A)
    # Mastered initial content with 98% accuracy, but has not logged in for 18 days.
    # Tests retention risk detection on high-capability students.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="highmasterylowengage",
            name="Test Student - High Mastery Low Engagement",
            email="test.highmasterylowengage@eduvia.local",
            cohort_key="cohort_a",
            teacher_id=COHORT_A_TEACHER_ID,
            age_group="secondary",
            learning_level="advanced",
            summary_description="Capable student who sailed through early material and may be under-challenged.",
            expected_mastery="Near perfect (95-100%)",
            expected_engagement="Stagnant in recent 2+ weeks",
            expected_adaptive_behavior="Propose advanced puzzle challenge to re-ignite curiosity",
            communication_primary_mode="verbal",
            receptive_preferences=["verbal", "visual_cues"],
            expressive_preferences=["verbal"],
            numeracy_stage="advanced",
            literacy_stage="fluent",
            attention_span_minutes=25,
            strengths=["high analytical aptitude", "self-directed"],
            focus_areas=["consistency of check-ins"],
            sensory_accommodations=["standard"],
            pacing="accelerated",
            teacher_notes="May be bored with introductory content. Needs higher complexity.",
            modality_effectiveness={"visual": 0.98, "interactive": 0.95, "audio": 0.90, "kinesthetic": 0.92},
            telemetry_events=[
                TelemetryTemplate(days_ago=22, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=1.0, assistance_level=0, hints_used=0, response_time_ms=1600),
                TelemetryTemplate(days_ago=20, objective_id=OBJ_1_5_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=True, score=0.98, assistance_level=0, hints_used=0, response_time_ms=1750),
                TelemetryTemplate(days_ago=18, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="interactive", strategy="visual_cueing", correct=True, score=0.96, assistance_level=0, hints_used=0, response_time_ms=1900),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 12. INCONSISTENT (Cohort B)
    # Volatile scores: swings from 1.00 down to 0.20 and back.
    # Tests stability and variance analytics.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="inconsistent",
            name="Test Student - Inconsistent",
            email="test.inconsistent@eduvia.local",
            cohort_key="cohort_b",
            teacher_id=COHORT_B_TEACHER_ID,
            age_group="primary",
            learning_level="intermediate",
            summary_description="Performance exhibits wide variance depending on daily focus, attention, and sensory load.",
            expected_mastery="Fluctuates between 20% and 100%, mean ~60%",
            expected_engagement="Regular participation with sporadic high/low sessions",
            expected_adaptive_behavior="Implement structured attention checks and predictable micro-pacing",
            communication_primary_mode="visual_cues",
            receptive_preferences=["visual_cues", "tactile"],
            expressive_preferences=["verbal"],
            numeracy_stage="intermediate",
            literacy_stage="emerging",
            attention_span_minutes=10,
            strengths=["capable of brilliant bursts of insight"],
            focus_areas=["attention stability", "fatigue management"],
            sensory_accommodations=["frequent_micro_breaks", "low_glare_screen"],
            pacing="flexible",
            teacher_notes="Performance heavily correlated with time of day and sensory environment.",
            modality_effectiveness={"visual": 0.70, "interactive": 0.65, "audio": 0.40, "kinesthetic": 0.75},
            telemetry_events=[
                TelemetryTemplate(days_ago=15, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=1.0, assistance_level=0, hints_used=0, response_time_ms=1900),
                TelemetryTemplate(days_ago=13, objective_id=OBJ_1_5_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=False, score=0.25, assistance_level=3, hints_used=3, response_time_ms=9200),
                TelemetryTemplate(days_ago=10, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="interactive", strategy="visual_cueing", correct=True, score=0.95, assistance_level=0, hints_used=0, response_time_ms=2100),
                TelemetryTemplate(days_ago=8, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=False, score=0.20, assistance_level=3, hints_used=4, response_time_ms=10500),
                TelemetryTemplate(days_ago=5, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.90, assistance_level=1, hints_used=1, response_time_ms=2500),
                TelemetryTemplate(days_ago=2, objective_id=OBJ_6_10_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=False, score=0.30, assistance_level=2, hints_used=3, response_time_ms=8800),
                TelemetryTemplate(days_ago=0, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="interactive", strategy="visual_cueing", correct=True, score=0.88, assistance_level=1, hints_used=1, response_time_ms=2800),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 13. FAST LEARNER (Cohort A)
    # Rapid mastery acquisition in few attempts with minimal latency.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="fastlearner",
            name="Test Student - Fast Learner",
            email="test.fastlearner@eduvia.local",
            cohort_key="cohort_a",
            teacher_id=COHORT_A_TEACHER_ID,
            age_group="early_childhood",
            learning_level="intermediate",
            summary_description="Quickly grasps new concepts and transitions from introductory to mastery in minimal iterations.",
            expected_mastery="High (90-95%) achieved rapidly",
            expected_engagement="Brisk, high-efficiency practice sessions",
            expected_adaptive_behavior="Skip redundant drills and advance to subsequent objectives",
            communication_primary_mode="verbal",
            receptive_preferences=["verbal", "visual_cues"],
            expressive_preferences=["verbal"],
            numeracy_stage="intermediate",
            literacy_stage="developing",
            attention_span_minutes=18,
            strengths=["quick pattern abstraction", "low hesitation"],
            focus_areas=["deepening problem explanation"],
            sensory_accommodations=["crisp_transitions"],
            pacing="accelerated",
            teacher_notes="Picks up new numerical concepts almost instantaneously.",
            modality_effectiveness={"visual": 0.92, "interactive": 0.90, "audio": 0.82, "kinesthetic": 0.85},
            telemetry_events=[
                TelemetryTemplate(days_ago=7, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.65, assistance_level=1, hints_used=1, response_time_ms=2800),
                TelemetryTemplate(days_ago=5, objective_id=OBJ_1_5_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=True, score=0.90, assistance_level=0, hints_used=0, response_time_ms=1900),
                TelemetryTemplate(days_ago=3, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="interactive", strategy="visual_cueing", correct=True, score=0.95, assistance_level=0, hints_used=0, response_time_ms=1700),
                TelemetryTemplate(days_ago=1, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=1.0, assistance_level=0, hints_used=0, response_time_ms=1500),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 14. SLOW LEARNER (Cohort B)
    # Gradual, steady improvement requiring high repetitions and patient pacing.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="slowlearner",
            name="Test Student - Slow Learner",
            email="test.slowlearner@eduvia.local",
            cohort_key="cohort_b",
            teacher_id=COHORT_B_TEACHER_ID,
            age_group="primary",
            learning_level="beginner",
            summary_description="Requires multiple gentle iterations to internalize rules, advancing steadily through patient repetition.",
            expected_mastery="Gradual climb from 35% to 65%",
            expected_engagement="High repetition count across extended timeline",
            expected_adaptive_behavior="Provide spaced repetition with small step increments",
            communication_primary_mode="visual_cues",
            receptive_preferences=["visual_cues", "tactile"],
            expressive_preferences=["tactile"],
            numeracy_stage="emerging",
            literacy_stage="emerging",
            attention_span_minutes=12,
            strengths=["steady determination", "benefits from calm repetition"],
            focus_areas=["reducing processing latency"],
            sensory_accommodations=["extended_time_limits", "gentle_encouragement"],
            pacing="deliberate",
            teacher_notes="Progresses solidly when not rushed. Multi-sensory reinforcement is key.",
            modality_effectiveness={"visual": 0.65, "interactive": 0.60, "audio": 0.45, "kinesthetic": 0.68},
            telemetry_events=[
                TelemetryTemplate(days_ago=25, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="scaffolded", correct=False, score=0.35, assistance_level=3, hints_used=3, response_time_ms=8200),
                TelemetryTemplate(days_ago=22, objective_id=OBJ_1_5_ID, activity_type="drag_drop", modality="interactive", strategy="scaffolded", correct=False, score=0.40, assistance_level=3, hints_used=3, response_time_ms=7900),
                TelemetryTemplate(days_ago=18, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="scaffolded", correct=True, score=0.50, assistance_level=2, hints_used=2, response_time_ms=7100),
                TelemetryTemplate(days_ago=14, objective_id=OBJ_1_5_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=True, score=0.55, assistance_level=2, hints_used=2, response_time_ms=6800),
                TelemetryTemplate(days_ago=10, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="visual_cueing", correct=True, score=0.62, assistance_level=1, hints_used=2, response_time_ms=6200),
                TelemetryTemplate(days_ago=6, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="interactive", strategy="scaffolded", correct=True, score=0.65, assistance_level=2, hints_used=2, response_time_ms=6000),
                TelemetryTemplate(days_ago=2, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.68, assistance_level=1, hints_used=1, response_time_ms=5800),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 15. NEARLY COMPLETE (Cohort A)
    # Mastered 1-5 and 6-10, working on final capstone challenge.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="nearlycomplete",
            name="Test Student - Nearly Complete",
            email="test.nearlycomplete@eduvia.local",
            cohort_key="cohort_a",
            teacher_id=COHORT_A_TEACHER_ID,
            age_group="primary",
            learning_level="advanced",
            summary_description="Has completed over 90% of the foundational curriculum standards and approaches graduation.",
            expected_mastery="Over 90% completion and competency",
            expected_engagement="High and steady across unit modules",
            expected_adaptive_behavior="Recommend final capstone synthesis activity",
            communication_primary_mode="verbal",
            receptive_preferences=["verbal", "visual_cues"],
            expressive_preferences=["verbal"],
            numeracy_stage="advanced",
            literacy_stage="fluent",
            attention_span_minutes=25,
            strengths=["comprehensive mastery", "high accuracy on diverse activity formats"],
            focus_areas=["readiness for next curriculum level"],
            sensory_accommodations=["standard"],
            pacing="accelerated",
            teacher_notes="Close to finishing demo curriculum. Ready for graduation certificate.",
            modality_effectiveness={"visual": 0.94, "interactive": 0.92, "audio": 0.88, "kinesthetic": 0.90},
            telemetry_events=[
                TelemetryTemplate(days_ago=20, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.95, assistance_level=0, hints_used=0, response_time_ms=1900),
                TelemetryTemplate(days_ago=16, objective_id=OBJ_1_5_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=True, score=1.0, assistance_level=0, hints_used=0, response_time_ms=1800),
                TelemetryTemplate(days_ago=12, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="interactive", strategy="visual_cueing", correct=True, score=0.92, assistance_level=0, hints_used=0, response_time_ms=2100),
                TelemetryTemplate(days_ago=8, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.95, assistance_level=0, hints_used=0, response_time_ms=1950),
                TelemetryTemplate(days_ago=4, objective_id=OBJ_PATTERNS_ID, activity_type="visual_identification", modality="visual", strategy="step_by_step", correct=True, score=0.90, assistance_level=0, hints_used=0, response_time_ms=2200),
                TelemetryTemplate(days_ago=1, objective_id=OBJ_PATTERNS_ID, activity_type="ordering", modality="interactive", strategy="chunking", correct=True, score=0.94, assistance_level=0, hints_used=0, response_time_ms=2050),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 16. EARLY PROGRESS (Cohort A)
    # Enrolled recently, completed first 3 activities on standard objective 1.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="earlyprogress",
            name="Test Student - Early Progress",
            email="test.earlyprogress@eduvia.local",
            cohort_key="cohort_a",
            teacher_id=COHORT_A_TEACHER_ID,
            age_group="early_childhood",
            learning_level="beginner",
            summary_description="Actively working through the first 20% of introductory curriculum units.",
            expected_mastery="Objective 1 in progress (70-75% accuracy)",
            expected_engagement="Active recent start",
            expected_adaptive_behavior="Complete foundational Objective 1 milestones",
            communication_primary_mode="verbal",
            receptive_preferences=["verbal", "visual_cues"],
            expressive_preferences=["verbal"],
            numeracy_stage="beginner",
            literacy_stage="emerging",
            attention_span_minutes=15,
            strengths=["quick start", "enthusiastic responses"],
            focus_areas=["number sequencing"],
            sensory_accommodations=["cheerful_audio_reinforcement"],
            pacing="moderate",
            teacher_notes="Off to a promising start. Showing good engagement.",
            modality_effectiveness={"visual": 0.80, "interactive": 0.75, "audio": 0.70, "kinesthetic": 0.72},
            telemetry_events=[
                TelemetryTemplate(days_ago=4, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.75, assistance_level=1, hints_used=1, response_time_ms=3100),
                TelemetryTemplate(days_ago=2, objective_id=OBJ_1_5_ID, activity_type="drag_drop", modality="interactive", strategy="step_by_step", correct=True, score=0.78, assistance_level=1, hints_used=1, response_time_ms=3300),
                TelemetryTemplate(days_ago=0, objective_id=OBJ_1_5_ID, activity_type="ordering", modality="interactive", strategy="visual_cueing", correct=True, score=0.80, assistance_level=1, hints_used=1, response_time_ms=2900),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 17. STRONG PRACTICE / WEAK CURRICULUM (Cohort B)
    # High activity score on repetitive familiar drills, but hasn't advanced in curriculum.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="strongpracticeweakcurr",
            name="Test Student - Strong Practice Weak Curriculum",
            email="test.strongpracticeweakcurr@eduvia.local",
            cohort_key="cohort_b",
            teacher_id=COHORT_B_TEACHER_ID,
            age_group="primary",
            learning_level="intermediate",
            summary_description="Excels at repetitive familiar practice items but resists advancing to new curriculum standards.",
            expected_mastery="High practice accuracy (90%), low curriculum breadth",
            expected_engagement="Frequent repetitive drills",
            expected_adaptive_behavior="Guide gently into untried curriculum objective 6-10",
            communication_primary_mode="visual_cues",
            receptive_preferences=["visual_cues"],
            expressive_preferences=["tactile"],
            numeracy_stage="intermediate",
            literacy_stage="developing",
            attention_span_minutes=15,
            strengths=["flawless on mastered drills"],
            focus_areas=["tolerance for novelty in curriculum"],
            sensory_accommodations=["familiar_layout_anchor"],
            pacing="moderate",
            teacher_notes="Comfortable with numbers 1 to 5. Needs nudging to tackle numbers 6 to 10.",
            modality_effectiveness={"visual": 0.90, "interactive": 0.88, "audio": 0.70, "kinesthetic": 0.85},
            telemetry_events=[
                TelemetryTemplate(days_ago=12, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.92, assistance_level=0, hints_used=0, response_time_ms=1900),
                TelemetryTemplate(days_ago=9, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.95, assistance_level=0, hints_used=0, response_time_ms=1800),
                TelemetryTemplate(days_ago=6, objective_id=OBJ_1_5_ID, activity_type="drag_drop", modality="visual", strategy="step_by_step", correct=True, score=0.90, assistance_level=0, hints_used=0, response_time_ms=2100),
                TelemetryTemplate(days_ago=3, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.94, assistance_level=0, hints_used=0, response_time_ms=1850),
                TelemetryTemplate(days_ago=1, objective_id=OBJ_1_5_ID, activity_type="visual_identification", modality="visual", strategy="step_by_step", correct=True, score=0.96, assistance_level=0, hints_used=0, response_time_ms=1750),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 18. STRONG CURRICULUM / WEAK PRACTICE (Cohort B)
    # Marked as progressed in units, but recent practice quizzes reveal dropped accuracy.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="strongcurrweakpractice",
            name="Test Student - Strong Curriculum Weak Practice",
            email="test.strongcurrweakpractice@eduvia.local",
            cohort_key="cohort_b",
            teacher_id=COHORT_B_TEACHER_ID,
            age_group="secondary",
            learning_level="intermediate",
            summary_description="Has high curriculum exposure on paper, but live practice telemetry reveals shaky retention.",
            expected_mastery="Nominally advanced, but empirical practice accuracy ~55%",
            expected_engagement="Moderate engagement",
            expected_adaptive_behavior="Recommend targeted diagnostic check on prior standards",
            communication_primary_mode="verbal",
            receptive_preferences=["verbal"],
            expressive_preferences=["verbal"],
            numeracy_stage="intermediate",
            literacy_stage="developing",
            attention_span_minutes=16,
            strengths=["participative", "rapid task switching"],
            focus_areas=["deep conceptual retention"],
            sensory_accommodations=["concept_reinforcement_cards"],
            pacing="deliberate",
            teacher_notes="May have skipped foundational steps earlier. Needs solid review.",
            modality_effectiveness={"visual": 0.60, "interactive": 0.55, "audio": 0.50, "kinesthetic": 0.52},
            telemetry_events=[
                TelemetryTemplate(days_ago=14, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="direct_instruction", correct=False, score=0.50, assistance_level=2, hints_used=2, response_time_ms=6200),
                TelemetryTemplate(days_ago=10, objective_id=OBJ_6_10_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=False, score=0.55, assistance_level=2, hints_used=2, response_time_ms=5900),
                TelemetryTemplate(days_ago=6, objective_id=OBJ_PATTERNS_ID, activity_type="drag_drop", modality="interactive", strategy="step_by_step", correct=False, score=0.48, assistance_level=3, hints_used=3, response_time_ms=6800),
                TelemetryTemplate(days_ago=2, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="visual_cueing", correct=True, score=0.62, assistance_level=1, hints_used=1, response_time_ms=4500),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 19. MIXED PERFORMANCE (Cohort B)
    # Distinct modality contrast: 92% on visual matching vs 35% on auditory/ordering.
    # Tests multi-sensory accommodation logic in the Adaptive Engine.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="mixedperformance",
            name="Test Student - Mixed Performance",
            email="test.mixedperformance@eduvia.local",
            cohort_key="cohort_b",
            teacher_id=COHORT_B_TEACHER_ID,
            age_group="primary",
            learning_level="intermediate",
            summary_description="Displays polarized sensory results: high accuracy in visual tasks, significant friction in auditory channels.",
            expected_mastery="Visual activities >90%, Auditory activities <40%",
            expected_engagement="High when presented visually, drops during auditory prompts",
            expected_adaptive_behavior="Prioritize Visual modality, exclude pure auditory instruction",
            communication_primary_mode="visual_cues",
            receptive_preferences=["visual_cues", "tactile"],
            expressive_preferences=["tactile", "visual_cues"],
            numeracy_stage="intermediate",
            literacy_stage="emerging",
            attention_span_minutes=15,
            strengths=["exceptional visual-spatial pattern recognition"],
            focus_areas=["auditory processing support"],
            sensory_accommodations=["always_include_visual_subtitles", "no_pure_audio_prompts"],
            pacing="moderate",
            teacher_notes="Auditory processing challenges. Shines brilliantly when information is presented visually.",
            modality_effectiveness={"visual": 0.92, "interactive": 0.85, "audio": 0.35, "kinesthetic": 0.80},
            telemetry_events=[
                # High score visual tasks
                TelemetryTemplate(days_ago=14, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="visual_cueing", correct=True, score=0.95, assistance_level=0, hints_used=0, response_time_ms=1900),
                TelemetryTemplate(days_ago=11, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="visual", strategy="visual_cueing", correct=True, score=0.90, assistance_level=0, hints_used=0, response_time_ms=2100),
                TelemetryTemplate(days_ago=8, objective_id=OBJ_1_5_ID, activity_type="visual_identification", modality="visual", strategy="step_by_step", correct=True, score=0.92, assistance_level=0, hints_used=0, response_time_ms=1850),
                # Low score audio/verbal tasks
                TelemetryTemplate(days_ago=6, objective_id=OBJ_1_5_ID, activity_type="matching", modality="audio", strategy="direct_instruction", correct=False, score=0.35, assistance_level=3, hints_used=3, response_time_ms=9200),
                TelemetryTemplate(days_ago=3, objective_id=OBJ_6_10_ID, activity_type="ordering", modality="audio", strategy="direct_instruction", correct=False, score=0.30, assistance_level=3, hints_used=4, response_time_ms=9800),
                # Back to visual success
                TelemetryTemplate(days_ago=1, objective_id=OBJ_PATTERNS_ID, activity_type="matching", modality="visual", strategy="visual_cueing", correct=True, score=0.94, assistance_level=0, hints_used=0, response_time_ms=2000),
            ],
        )
    )

    # ──────────────────────────────────────────────────────────────────────────
    # 20. AVERAGE (Cohort A)
    # Balanced, standard performance (~76% accuracy, Level 1 assistance).
    # Baseline benchmark for cohort comparisons.
    # ──────────────────────────────────────────────────────────────────────────
    students.append(
        LearnerScenarioDefinition(
            key="average",
            name="Test Student - Average",
            email="test.average@eduvia.local",
            cohort_key="cohort_a",
            teacher_id=COHORT_A_TEACHER_ID,
            age_group="primary",
            learning_level="intermediate",
            summary_description="Represents typical cohort progress with balanced accuracy and moderate scaffolding needs.",
            expected_mastery="75-80% accuracy across standard units",
            expected_engagement="Healthy routine cadence (7 sessions in 30 days)",
            expected_adaptive_behavior="Standard incremental curriculum progression",
            communication_primary_mode="verbal",
            receptive_preferences=["verbal", "visual_cues"],
            expressive_preferences=["verbal"],
            numeracy_stage="intermediate",
            literacy_stage="developing",
            attention_span_minutes=18,
            strengths=["consistent performance across all subjects"],
            focus_areas=["gradual independence from hints"],
            sensory_accommodations=["standard"],
            pacing="standard",
            teacher_notes="Typical, steady student. Solid baseline for cohort comparison.",
            modality_effectiveness={"visual": 0.78, "interactive": 0.76, "audio": 0.72, "kinesthetic": 0.75},
            telemetry_events=[
                TelemetryTemplate(days_ago=20, objective_id=OBJ_1_5_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.78, assistance_level=1, hints_used=1, response_time_ms=3200),
                TelemetryTemplate(days_ago=16, objective_id=OBJ_1_5_ID, activity_type="ordering", modality="interactive", strategy="step_by_step", correct=True, score=0.74, assistance_level=1, hints_used=1, response_time_ms=3400),
                TelemetryTemplate(days_ago=12, objective_id=OBJ_6_10_ID, activity_type="drag_drop", modality="interactive", strategy="visual_cueing", correct=True, score=0.76, assistance_level=1, hints_used=2, response_time_ms=3100),
                TelemetryTemplate(days_ago=8, objective_id=OBJ_6_10_ID, activity_type="matching", modality="visual", strategy="step_by_step", correct=True, score=0.80, assistance_level=1, hints_used=1, response_time_ms=2900),
                TelemetryTemplate(days_ago=4, objective_id=OBJ_PATTERNS_ID, activity_type="ordering", modality="interactive", strategy="chunking", correct=True, score=0.72, assistance_level=2, hints_used=2, response_time_ms=3600),
                TelemetryTemplate(days_ago=1, objective_id=OBJ_PATTERNS_ID, activity_type="drag_drop", modality="visual", strategy="step_by_step", correct=True, score=0.78, assistance_level=1, hints_used=1, response_time_ms=3000),
            ],
        )
    )

    return students
