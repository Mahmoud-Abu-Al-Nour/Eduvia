# Eduvia — Development & Test Data Scenarios Specification

This document provides the complete manual testing checklist and pedagogical scenario catalog for all test students seeded into Eduvia.

## Cohort Architecture & Access Control
- **Cohort A (High-Performing & Accelerated)**:
  - Teacher: `teacher@eduvia.app` (Alice Teacher)
  - Cohort ID: `11111111-1111-1111-1111-111111111111`
  - Characteristics: High average accuracy (~96%), high curriculum completion, proactive engagement.
- **Cohort B (Targeted Scaffolding & Foundational)**:
  - Teacher: `teacher.cohortb@eduvia.local` (Marcus Teacher)
  - Cohort ID: `bbbbbbbb-0000-0000-0000-000000000002`
  - Characteristics: Moderate/struggling average accuracy (~48%), varied assistance requirements, multiple intervention alerts.
- **Global Administrator**:
  - Admin: `admin@eduvia.app` (Eduvia Admin)
  - Characteristics: Cross-cohort visibility across all 21 learners, global telemetry analytics.

---

## Complete Test Student Scenario Catalog

### 1. Test Student - Excellent
- **Key**: `excellent`
- **Email**: `test.excellent@eduvia.local`
- **Cohort**: Cohort A (Alice Teacher)
- **Profile**: Visual & kinesthetic, high attention span (25 min).
- **Mastery**: 95–100% (Accuracy: 100%).
- **Engagement**: High frequency across 60 days, most recent session 1 day ago.
- **Curriculum Progress**: All objectives mastered; prerequisite chains fully unlocked.
- **Activity Behavior**: 8 attempts, 0 hints used, 0 assistance level needed.
- **Expected Adaptive Engine Behavior**:
  - Recommends advanced learning objectives (Obj 2: Numbers 6–10).
  - Promotes difficulty level to higher tier.
  - Applies `gradual_difficulty` strategy with `reinforce_mastered_curriculum` constraint.
- **Expected Analytics & Dashboard**:
  - Appears in Cohort A "Mastered" distribution.
  - No active risk alerts.

---

### 2. Test Student - High Performer
- **Key**: `high_performer`
- **Email**: `test.highperformer@eduvia.local`
- **Cohort**: Cohort A (Alice Teacher)
- **Profile**: Visual & auditory learner, solid self-regulation (20 min).
- **Mastery**: 85–95% (Accuracy: 88%).
- **Engagement**: Regular sessions, active in last 2 days.
- **Curriculum Progress**: Obj 1 mastered, Obj 2 in progress with high score.
- **Activity Behavior**: 8 attempts, occasional subtle hints (avg hints: 0.38, avg asst: 0.25).
- **Expected Adaptive Engine Behavior**:
  - Advances to unmastered objectives.
  - Applies `step_by_step` strategy with minimal scaffolding.
- **Expected Analytics & Dashboard**:
  - Appears in "Mastered" category.

---

### 3. Test Student - Improving
- **Key**: `improving`
- **Email**: `test.improving@eduvia.local`
- **Cohort**: Cohort A (Alice Teacher)
- **Profile**: Tactile/visual learner, growth mindset profile (15 min).
- **Mastery**: Historical 40% -> Recent 85% (Upward trend).
- **Engagement**: Consistent practice increasing in last 14 days.
- **Curriculum Progress**: Obj 1 completed, Obj 2 in active progress.
- **Activity Behavior**: Early attempts had low accuracy (0.4–0.5) with Level 2 assistance; recent attempts achieved 0.85–0.90 with 0 hints.
- **Expected Adaptive Engine Behavior**:
  - Detects positive slope in performance events.
  - Decreases scaffolding tier from Tier 2 to Tier 1.
  - Recommends standard practice with positive reinforcement.
- **Expected Analytics & Dashboard**:
  - Shows clear upward trajectory on performance trend charts.

---

### 4. Test Student - Struggling
- **Key**: `struggling`
- **Email**: `test.struggling@eduvia.local`
- **Cohort**: Cohort B (Marcus Teacher)
- **Profile**: Highly visual, short attention span (10 min), low distractor tolerance.
- **Mastery**: 30–45% (Accuracy: 33%).
- **Engagement**: Active attempts but high error rate.
- **Curriculum Progress**: Stalled on Obj 1 (Prerequisites locked for advanced modules).
- **Activity Behavior**: 6 attempts, high latency, average hints: 2.7, average assistance level: 2.0.
- **Expected Adaptive Engine Behavior**:
  - Locks advanced objectives (`prereq_locked`).
  - Recommends foundational objective Obj 1 with `demonstration` strategy.
  - Applies Tier 2 scaffolding with explicit sensory cueing.
- **Expected Analytics & Dashboard**:
  - Generates Intervention Warning Alert: "High assistance dependency detected: Required Level 2 assistance across recent attempts."

---

### 5. Test Student - At Risk
- **Key**: `at_risk`
- **Email**: `test.atrisk@eduvia.local`
- **Cohort**: Cohort B (Marcus Teacher)
- **Profile**: Significant sensory sensitivities, low frustration tolerance (8 min).
- **Mastery**: 0–25% (Accuracy: 0%).
- **Engagement**: Prolonged inactivity (last active 28 days ago).
- **Curriculum Progress**: 0 completed objectives.
- **Activity Behavior**: 3 incomplete attempts, failed submissions, average assistance: 2.0, 3+ hints.
- **Expected Adaptive Engine Behavior**:
  - Locks all advanced curriculum.
  - Recommends remedial visual identification with Tier 2 scaffolding and `demonstration` strategy.
- **Expected Analytics & Dashboard**:
  - Generates Critical Action Required Alert: "Critical learning regression: Accuracy dropped below 30% with extended inactivity."

---

### 6. Test Student - Inactive
- **Key**: `inactive`
- **Email**: `test.inactive@eduvia.local`
- **Cohort**: Cohort B (Marcus Teacher)
- **Profile**: Auditory preference, 15 min attention span.
- **Mastery**: Historical 75% accuracy (solid when active).
- **Engagement**: Zero activity for 45+ days.
- **Curriculum Progress**: Obj 1 mastered historically, Obj 2 not started.
- **Activity Behavior**: 4 historical completed attempts from 45–60 days ago; nothing recent.
- **Expected Adaptive Engine Behavior**:
  - Recommends low-stakes re-engagement activity on Obj 1 to reassess retention.
- **Expected Analytics & Dashboard**:
  - Not counted in 7-day active learners.

---

### 7. Test Student - New
- **Key**: `new_learner`
- **Email**: `test.new@eduvia.local`
- **Cohort**: Cohort A (Alice Teacher)
- **Profile**: Recently onboarded learner (enrolled 2 days ago).
- **Mastery**: Emerging (1 completed activity, 80% score).
- **Engagement**: Active yesterday and today.
- **Curriculum Progress**: Initial diagnostic completed, Obj 1 in progress.
- **Activity Behavior**: 2 events total.
- **Expected Adaptive Engine Behavior**:
  - Baseline onboarding recommendation with default sensory modalities.
- **Expected Analytics & Dashboard**:
  - Appears in 7-day active learners; displays onboarding/early progress badge.

---

### 8. Test Student - No Activity
- **Key**: `no_activity`
- **Email**: `test.noactivity@eduvia.local`
- **Cohort**: Cohort B (Marcus Teacher)
- **Profile**: Visual preference, newly registered account.
- **Mastery**: 0% (Null/empty telemetry).
- **Engagement**: 0 sessions, 0 events, 0 attempts.
- **Curriculum Progress**: Enrolled in curriculum; all modules "Not Started".
- **Activity Behavior**: Empty list.
- **Expected Adaptive Engine Behavior**:
  - Serves unstarted foundational objective Obj 1 with Tier 1 gentle scaffolding.
- **Expected Analytics & Dashboard**:
  - Tests zero-state / empty analytics graphs; handles division by zero safely.

---

### 9. Test Student - Low Engagement
- **Key**: `low_engagement`
- **Email**: `test.lowengagement@eduvia.local`
- **Cohort**: Cohort A (Alice Teacher)
- **Profile**: Verbal & visual learner, high independence when practicing.
- **Mastery**: 85% accuracy on attempts made.
- **Engagement**: Infrequent sessions (last active 18 days ago).
- **Curriculum Progress**: Obj 1 mastered, Obj 2 untouched.
- **Activity Behavior**: 3 attempts with high scores (0.85–0.90) but sporadic dates.
- **Expected Adaptive Engine Behavior**:
  - Suggests interactive activity with gamified reinforcement to rebuild habit.
- **Expected Analytics & Dashboard**:
  - Generates Warning Alert: "Declining session frequency despite adequate historical accuracy."

---

### 10. Test Student - High Engagement Low Mastery
- **Key**: `high_eng_low_mastery`
- **Email**: `test.highenglowmastery@eduvia.local`
- **Cohort**: Cohort B (Marcus Teacher)
- **Profile**: Enthusiastic, interactive preference, perseverative attempts (12 min).
- **Mastery**: 25% accuracy.
- **Engagement**: Very high (10 attempts across 5 sessions, active today).
- **Curriculum Progress**: Stuck on Obj 1 despite 10 attempts.
- **Activity Behavior**: 10 attempts, repeatedly failing without asking for hints, high rapid guessing.
- **Expected Adaptive Engine Behavior**:
  - Detects high persistence with low mastery; breaks cycle by forcing `simplification` or `demonstration` strategy.
  - Recommends reduced distractor count (matching 2 items instead of 4).
- **Expected Analytics & Dashboard**:
  - Shows high activity count in dashboard bar charts but low accuracy line.

---

### 11. Test Student - High Mastery Low Engagement
- **Key**: `high_mastery_low_eng`
- **Email**: `test.highmasteryloweng@eduvia.local`
- **Cohort**: Cohort A (Alice Teacher)
- **Profile**: Gifted / fast assimilator (20 min).
- **Mastery**: 100% accuracy.
- **Engagement**: Completed 2 activities quickly then stopped (last active 22 days ago).
- **Curriculum Progress**: Obj 1 mastered with 0 errors.
- **Activity Behavior**: 2 attempts, perfect 1.0 score, low latency (<2 sec).
- **Expected Adaptive Engine Behavior**:
  - Detects boredom / under-challenge risk; recommends accelerating directly to difficulty level 3.
- **Expected Analytics & Dashboard**:
  - Shows 100% mastery but inactive in 7-day view.

---

### 12. Test Student - Inconsistent
- **Key**: `inconsistent`
- **Email**: `test.inconsistent@eduvia.local`
- **Cohort**: Cohort B (Marcus Teacher)
- **Profile**: Sensory fluctuations based on environmental fatigue.
- **Mastery**: Oscillating (Scores: 1.0, 0.2, 0.9, 0.1, 1.0, 0.3).
- **Engagement**: Active every 2–3 days.
- **Curriculum Progress**: In progress, unstable mastery evidence.
- **Activity Behavior**: 6 attempts alternating between flawless and rapid failure.
- **Expected Adaptive Engine Behavior**:
  - Identifies variance in evidence; maintains conservative difficulty level 1.
- **Expected Analytics & Dashboard**:
  - Generates Info Alert: "High performance variance: Alternating between high scores and zero completion."

---

### 13. Test Student - Fast Learner
- **Key**: `fast_learner`
- **Email**: `test.fastlearner@eduvia.local`
- **Cohort**: Cohort A (Alice Teacher)
- **Profile**: Quick conceptual grasp, prefers self-directed exploration.
- **Mastery**: 95–100% (Rapid progression).
- **Engagement**: High frequency over 4 days.
- **Curriculum Progress**: Mastered Obj 1 in 2 attempts; mastered Obj 2 in 2 attempts.
- **Activity Behavior**: 4 attempts total, rapid response times (avg 1800 ms), 0 hints.
- **Expected Adaptive Engine Behavior**:
  - Accelerates curriculum traversal; auto-promotes difficulty level.
- **Expected Analytics & Dashboard**:
  - Highest learning rate in Cohort A.

---

### 14. Test Student - Slow Learner
- **Key**: `slow_learner`
- **Email**: `test.slowlearner@eduvia.local`
- **Cohort**: Cohort B (Marcus Teacher)
- **Profile**: Needs extensive repetition and multi-sensory reinforcement.
- **Mastery**: Gradual climb from 20% to 65%.
- **Engagement**: High diligence, daily sessions.
- **Curriculum Progress**: Obj 1 developing; requires 9 attempts to stabilize.
- **Activity Behavior**: 9 attempts, high hints used initially (3 hints), dropping to 1 hint recently.
- **Expected Adaptive Engine Behavior**:
  - Applies `repetition` strategy with `step_by_step` breakdown.
- **Expected Analytics & Dashboard**:
  - Steady positive slope with high session count.

---

### 15. Test Student - Nearly Complete
- **Key**: `nearly_complete`
- **Email**: `test.nearlycomplete@eduvia.local`
- **Cohort**: Cohort A (Alice Teacher)
- **Profile**: Senior tier learner (25 min attention span).
- **Mastery**: 92% across all units.
- **Engagement**: Active 1 day ago.
- **Curriculum Progress**: 90% curriculum completed; only 1 capstone objective remaining.
- **Activity Behavior**: 10 attempts across all lessons, high consistency.
- **Expected Adaptive Engine Behavior**:
  - Targets the final uncompleted capstone objective.
- **Expected Analytics & Dashboard**:
  - Highest curriculum completion bar in cohort overview.

---

### 16. Test Student - Early Progress
- **Key**: `early_progress`
- **Email**: `test.earlyprogress@eduvia.local`
- **Cohort**: Cohort A (Alice Teacher)
- **Profile**: Junior level learner.
- **Mastery**: 70%.
- **Engagement**: Regular sessions over last 5 days.
- **Curriculum Progress**: 20% of curriculum complete.
- **Activity Behavior**: 3 attempts, steady progression.
- **Expected Adaptive Engine Behavior**:
  - Recommends next sequential lesson in Unit 1.
- **Expected Analytics & Dashboard**:
  - Normal baseline progression.

---

### 17. Test Student - Strong Practice Weak Curriculum
- **Key**: `strong_practice_weak_curr`
- **Email**: `test.strongpracticeweakcurr@eduvia.local`
- **Cohort**: Cohort B (Marcus Teacher)
- **Profile**: Enjoys standalone game-like practice activities.
- **Mastery**: 85% on practice games, but low formal curriculum completion (15%).
- **Engagement**: High engagement on practice activities.
- **Curriculum Progress**: Has not advanced beyond lesson 1.
- **Activity Behavior**: 7 attempts, mostly on the same introductory practice activity.
- **Expected Adaptive Engine Behavior**:
  - Nudges learner into formal curriculum progression.
- **Expected Analytics & Dashboard**:
  - Disparity between total activities completed and curriculum completion %.

---

### 18. Test Student - Strong Curriculum Weak Practice
- **Key**: `strong_curr_weak_practice`
- **Email**: `test.strongcurrweakpractice@eduvia.local`
- **Cohort**: Cohort B (Marcus Teacher)
- **Profile**: Fast reader, skips practice exercises.
- **Mastery**: 50% on hands-on practice.
- **Engagement**: High completion of lesson reviews, low scores on application tasks.
- **Curriculum Progress**: High module traversal but fragile empirical mastery.
- **Activity Behavior**: 5 attempts with 50% accuracy; fails when assistance is removed.
- **Expected Adaptive Engine Behavior**:
  - Recommends remediation practice before allowing further progression.
- **Expected Analytics & Dashboard**:
  - High progress indicator with warning flag on mastery retention.

---

### 19. Test Student - Mixed Performance
- **Key**: `mixed_performance`
- **Email**: `test.mixedperformance@eduvia.local`
- **Cohort**: Cohort A (Alice Teacher)
- **Profile**: Strong in visual matching (100% accuracy), weak in sequential ordering (40% accuracy).
- **Mastery**: Domain-specific variance.
- **Engagement**: Consistent practice.
- **Curriculum Progress**: Obj 1 mastered, Obj 2 stalled.
- **Activity Behavior**: Flawless on Obj 1 (Visual identification), multiple failures on Obj 2 (Sequential ordering).
- **Expected Adaptive Engine Behavior**:
  - Leverages visual strengths to scaffold sequential ordering tasks (e.g. Visual Number Lines).
- **Expected Analytics & Dashboard**:
  - Shows clear contrast in objective breakdown charts.

---

### 20. Test Student - Average
- **Key**: `average`
- **Email**: `test.average@eduvia.local`
- **Cohort**: Cohort B (Marcus Teacher)
- **Profile**: Standard benchmark learner (15 min).
- **Mastery**: 65–70% accuracy.
- **Engagement**: 1–2 sessions per week.
- **Curriculum Progress**: Pacing on schedule with standard grade expectations.
- **Activity Behavior**: 5 attempts, occasional hint (avg hints: 1.0, avg asst: 0.8).
- **Expected Adaptive Engine Behavior**:
  - Standard linear progression with balanced practice.
- **Expected Analytics & Dashboard**:
  - Sits in the center of all cohort distributions.

---

## Data Management Commands

### 1. Seeding Data
To seed all test students, teachers, curriculum objectives, profiles, attempts, and telemetry:
```bash
# In PostgreSQL / Production-like environments:
python backend/scripts/seed_test_data.py

# In Local / Offline Development:
# The fixtures are automatically loaded into memory when running backend/dev_server.py
```

### 2. Clearing Test Data Safely
Removes ONLY records matching the deterministic namespace (`test.*@eduvia.local` and `teacher.cohortb@eduvia.local`), preserving core demo users (`admin@eduvia.app`, `teacher@eduvia.app`, `Tariq Al-Mansoor`):
```bash
python backend/scripts/clear_test_data.py
```

### 3. Resetting / Reseeding Test Data
Executes clear followed immediately by seed:
```bash
python backend/scripts/reset_test_data.py
```
