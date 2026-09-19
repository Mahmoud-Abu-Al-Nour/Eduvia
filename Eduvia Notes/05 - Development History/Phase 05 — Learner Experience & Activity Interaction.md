# Phase 05 — Learner Experience & Activity Interaction

## Objective
Create the distraction-free, accessible learner interaction environment and real-time activity execution engine. SEN learners interact directly with multi-modal learning content through intuitive, low-friction interfaces, supported by multi-tiered scaffolding, text-to-speech audio guidance, and authoritative server-side evaluation.

---

## Requirements & Scope
- **Distraction-Free Learner UI**: Full-screen, cognitive calm environment stripping away complex navigation, sidebars, and confusing notifications. Accessible via `/learn/:activityId` and `/learn/preview`.
- **Activity Player Orchestration**: `ActivityPlayer.tsx` coordinates question rendering, interaction timing, hint state, attempt counting, and submission payload assembly.
- **5 Multi-Modal Interaction Renderers**:
  1. `MatchingActivity.tsx`: Tap-to-select and drag-to-match concept pairs.
  2. `MultipleChoiceActivity.tsx`: High-contrast choice cards with keyboard focus indicators.
  3. `OrderingActivity.tsx`: Step sequencer with up/down arrows and drag reordering.
  4. `VisualIdentificationActivity.tsx`: Target image identification with clear borders.
  5. `DragDropActivity.tsx`: Accessible spatial item placement into bucket targets.
- **Multi-Tier Scaffolding**: 3-level progressive hint mechanism:
  * *Level 1 (Subtle Prompt)*: General encouragement or concept reminder.
  * *Level 2 (Direct Hint)*: Eliminates half of incorrect distractors or highlights primary clue.
  * *Level 3 (Demonstration)*: Explicit step-by-step walkthrough of the solution.
- **Text-to-Speech (TTS)**: Built-in voice readout via Web Speech API custom hook (`useSpeechSynthesis.ts`), allowing auditory learners to hear prompts and choices read aloud.
- **Cognitive Calm Feedback**: `CognitiveCalmFeedback.tsx` provides gentle visual and auditory positive reinforcement without punitive red failure banners, loud buzzer noises, or anxiety-inducing timers.
- **Authoritative Backend Evaluation**: `POST /api/v1/activities/evaluate` evaluates submitted answers against server-side ground truth, computing score, correctness, and rubric feedback.

---

## Key Architecture & Components
* **Orchestrator**: `frontend/src/features/learning/ActivityPlayer.tsx`
* **Renderers**: `frontend/src/features/learning/components/` (`MatchingActivity`, `MultipleChoiceActivity`, `OrderingActivity`, `VisualIdentificationActivity`, `DragDropActivity`)
* **Feedback**: `frontend/src/features/learning/components/CognitiveCalmFeedback.tsx`
* **Audio Hook**: `frontend/src/hooks/useSpeechSynthesis.ts`
* **Evaluation Service**: `backend/app/activities/service.py` (`evaluate_submission`)
* **Evaluation Schemas**: `backend/app/activities/schemas.py` (`ActivitySubmissionRequest`, `ActivityEvaluationResponse`)

---

## Phase Boundary Discipline
Phase 5 maintains strict architectural isolation:
* **No Persistent Telemetry**: Interaction state and attempt counters are strictly scoped to the individual activity session.
* **No Long-Term Mastery**: Evaluation calculates the immediate score of the attempt; it does not compute cumulative objective mastery.
* **No Adaptive Sequencing**: Phase 5 renders the designated activity without sequencing subsequent activities.

---

## Verification & Testing
* **Test Coverage**: 31 comprehensive backend tests in `backend/tests/test_activity_interaction.py` verifying:
  * Authoritative evaluation across all 5 activity modalities.
  * Accurate calculation of scores and partial credits.
  * Correct tracking of assistance levels and hints requested.
  * Strict rejection of malformed submission payloads.
  * Retrieval of generated activities by ID.
* **Full Backend Regression**: **111/111 tests passed** (31 Phase 5 + 80 previous).
* **Frontend Build**: Vite production build succeeded cleanly.

---

## Gate Status
# **PHASE 5 — LOCKED**

---

## Navigation & Related Notes
* Back to: [[05 - Development History/Eduvia Development History|Eduvia Development History]]
* Archived Report: [[05 - Development History/Reports/Phase 05 Report|Phase 05 Implementation Report]]
* Architecture: [[03 - AI & Adaptive Learning/Activity Evaluation|Activity Evaluation Architecture]]
* Previous Phase: [[05 - Development History/Phase 04 — Activity Generation Engine|Phase 04 — Activity Generation Engine]]
* Next Phase: [[05 - Development History/Phase 06 — Performance Tracking & Telemetry|Phase 06 — Performance Tracking & Telemetry]]

