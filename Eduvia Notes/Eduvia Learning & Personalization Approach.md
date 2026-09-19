# Eduvia Learning & Personalization Approach

> **Empirical Telemetry, Deterministic Scaffolding, and Curricular Rigor Without Artificial Simplification**

---

## The Core Thesis: Standardized Curriculum + Personalized Delivery

Traditional special education tools frequently dilute the curriculum when a learner encounters difficulty. If a student struggles with multi-digit subtraction or phonics blending, standard software often drops them into lower-grade content. This practice creates compounding educational deficits.

Eduvia rejects this compromise. The **learning objectives remain standardized, academically rigorous, and tied directly to formal curriculum frameworks**. What adapts is the **delivery mechanism**:
* The sensory modality of presentation (text, structured visuals, tactile ordering, drag-and-drop manipulation).
* The density of visual stimuli on screen.
* The progressive level of assistance and scaffolding provided.
* The calibrated difficulty of supporting distractors.

```text
Standardized Curriculum Objective (Fixed Target)
                    │
                    ▼
     Dynamic Modality & Scaffolding
   [Visual ID / Ordering / Matching]
                    │
                    ▼
        Authoritative Server Eval
                    │
                    ▼
    Deterministic Adaptation Engine
                    │
   ┌────────────────┴────────────────┐
   ▼                                 ▼
Mastery Achieved             Prerequisite Required
(Advance Node)              (Step to Foundational Node)
```

---

## 1. Curriculum Architecture & Progression

The curriculum is structured as an authoritative 5-tier relational hierarchy:

```text
Subject (e.g., Mathematics)
  └── Grade (e.g., Grade 3)
        └── Domain (e.g., Number & Operations in Base Ten)
              └── Topic (e.g., Multi-Digit Addition)
                    └── Learning Objective (e.g., Add two 3-digit numbers with regrouping)
```

### Prerequisite Directed Acyclic Graph (DAG)
Learning Objectives are not isolated silos; they form a directed dependency graph. 
* Each objective defines explicit prerequisite links (`prerequisite_id`).
* When a learner exhibits persistent difficulty on an objective, the adaptation engine does not randomly guess an easier task; it traverses the DAG backward to isolate whether an unmastered prerequisite (e.g., place value decomposition) is the root cause.
* Teachers can inspect the graph and manually enforce or bypass prerequisite locks.

---

## 2. Activity Modalities & Controlled Generation

Eduvia implements **five distinct activity modalities**, each engineered to address specific cognitive and sensory profiles:

| Modality Key | Primary Interaction Model | Sensory & Cognitive Target |
| :--- | :--- | :--- |
| `matching` | Connecting related conceptual pairs (e.g., term to definition, number to quantity). | Associative memory, relational conceptualization, low working memory burden. |
| `multiple_choice` | Selecting the correct response from a set of options (2 to 4 choices). | Recognition over recall; predictable visual format with keyboard/switch support. |
| `ordering` | Sequencing items in sequential, chronological, or magnitude order. | Executive function, temporal processing, procedural and ordinal reasoning. |
| `visual_identification` | Identifying targets based on visual cues, symbols, or structured representations. | Visual-spatial learners, students with emerging literacy, iconographic matching. |
| `drag_and_drop` | Categorizing or placing interactive tokens into target drop zones. | Kinesthetic engagement, spatial categorization, fine-motor/touchscreen interaction. |

### Schema Enforcement & Discriminated Unions
Every generated activity must strictly validate against **Pydantic v2 discriminated union models** (`ActivityData`). Any payload failing validation is rejected immediately before reaching the learner client.

### Scaffolding Levels
Activities provide four discrete, deterministic tiers of scaffolding:
* **Level 0 (None)**: Baseline prompt without hints or accommodations.
* **Level 1 (Gentle Hint)**: Conceptual reminder or guiding question (e.g., "Remember what place value the middle digit represents").
* **Level 2 (Visual Cue / Elimination)**: Removes one or more incorrect distractors or highlights relevant features.
* **Level 3 (Step-by-Step Scaffolding / Demonstration)**: Decomposes the task into explicit sub-steps or walks through an analogous worked example.

---

## 3. Server-Side Authoritative Evaluation

A core security and data integrity invariant of Eduvia is that **the client is never trusted to evaluate student answers**. 

### The Evaluation Flow
1. The learner interacts with the UI (selecting an option, ordering an array, or placing tokens).
2. The frontend submits the **raw user submission** (e.g., `{"selected_option_id": "opt_2"}`) along with the current `assistance_level_used` (0–3) and client interaction timing.
3. The FastAPI `EvaluationService` loads the true activity definition from the server session, compares the learner's input against the authoritative answer key, calculates the numeric score, and determines correctness.
4. The server records the immutable interaction telemetry and returns a sanitized feedback payload.

This prevents client-side tampering, eliminates grading drift across different client versions, and ensures telemetry accurately reflects student ability.

---

## 4. Telemetry & Analytics Architecture

### Immutable Raw Event Logging
Eduvia records interaction telemetry into two core relational tables:
* **`PerformanceEvent`**: Fine-grained interaction timestamps, including hint requests, intermediate errors, replay triggers, and time-on-task.
* **`ActivityAttempt`**: Completed activity sessions containing the final correctness flag, score, assistance level used, modality type, and session duration.

### Dynamic Metric Synthesis (Zero Speculative Tables)
Unlike legacy LMS architectures that maintain pre-computed summary tables (which inevitably drift out of sync with raw logs), Eduvia **calculates all analytics dynamically** from the immutable event log. The system computes:
* **Objective-Level Accuracy**: Percentage of correct attempts over historical sessions.
* **Modality Breakdown**: Comparative accuracy and error rates across all 5 modalities, isolating whether a learner performs significantly better in visual vs. text-based tasks.
* **Assistance Level Distribution**: Proportion of attempts solved independently vs. with Level 1, 2, or 3 assistance.
* **Longitudinal Progress**: Rolling mastery trajectory across calendar weeks.

---

## 5. Pedagogical Independence & The Mastery Rubric

Standard educational software often relies on a naive metric: if a student answers 80% of questions correctly, they are marked as having "mastered" the topic.

Eduvia enforces a strict standard of **Pedagogical Independence**:

$$
\text{Mastery Status} = 
\begin{cases} 
\text{Mastered} & \text{if } \text{Accuracy} \ge 80\% \land \text{Average Assistance} \le 1.0 \land \text{Attempts} \ge 3 \\
\text{In Progress} & \text{if } \text{Accuracy} \ge 80\% \land \text{Average Assistance} > 1.0 \\
\text{Needs Support} & \text{if } \text{Accuracy} < 60\% \text{ across } \ge 3 \text{ attempts} \\
\text{Not Started} & \text{if } \text{Attempts} = 0
\end{cases}
$$

### Why Independence Matters
If a learner scores 100% on a series of subtraction exercises, but required **Level 3 scaffolding** (full step-by-step guidance) on every question, they have **not** achieved mastery. Marking such a student as "proficient" masks their true educational needs and leads to failure on subsequent concepts. In Eduvia, that learner is marked as `in_progress` with an explicit signal to the teacher regarding scaffolding reliance.

---

## 6. The Deterministic Adaptation Hierarchy

Phase 8 established the **Adaptive Learning Intelligence Engine**, governed by a strict five-tier deterministic adaptation hierarchy:

```text
                 1. Difficulty Calibration
                            ↓
                 2. Hints & Scaffolding
                            ↓
                 3. Activity Type / Modality
                            ↓
                 4. Teaching Strategy
                            ↓
                 5. Sensory Modality Shift
```

### Adaptation Rules & Thresholds
1. **Difficulty Calibration**: If accuracy is between 70% and 80%, the engine modulates item difficulty (e.g., decreasing distractor plausibility) within the current modality.
2. **Scaffolding Escalation**: Upon an incorrect attempt, the engine automatically steps up the assistance level ($0 \rightarrow 1 \rightarrow 2 \rightarrow 3$) on subsequent items of the same objective.
3. **Modality Optimization**: Modality switching requires a minimum threshold of observed attempts ($\ge 3$) to prevent erratic jumping. The engine shifts the learner toward their empirically proven highest-performing modality.
4. **Prerequisite Step-Back**: If a learner fails $\ge 3$ consecutive attempts despite Level 2+ assistance, the engine recommends stepping back to the immediate unmastered prerequisite objective in the curriculum DAG.
5. **Teacher Override Precedence**: Any teacher lock or manual assignment **immediately supersedes** all algorithmic recommendations.

### The Non-Negotiable Boundary: Gemini Does NOT Make Adaptation Decisions
> **The Generative AI model is strictly prohibited from deciding what a student learns next.**
> 
> Gemini is utilized exclusively for generating text, questions, and contextual descriptions. All adaptation calculations, prerequisite routing, mastery evaluations, and intervention alerts are executed by deterministic Python logic with mathematical transparency and zero hallucination risk.

---

## Related Documentation

* Master Overview: [[Eduvia Project Overview & Technical Abstract|Eduvia Project Overview & Technical Abstract]]
* System Architecture: [[Eduvia Architecture & System Design|Eduvia Architecture & System Design]]
* AI & RAG Pipeline: [[Eduvia AI & RAG Technical Approach|Eduvia AI & RAG Technical Approach]]
* Accessibility Standards: [[Eduvia Accessibility & Cognitive Calm|Eduvia Accessibility & Cognitive Calm]]
* Teacher & Learner Workflows: [[Eduvia User Workflows|Eduvia User Workflows]]
* Telemetry History (Phase 6): [[05 - Development History/Phase 06 — Performance Tracking & Telemetry|Phase 06 — Performance Tracking & Telemetry]]
* Mastery Engine History (Phase 7): [[05 - Development History/Phase 07 — Learner Analytics & Mastery Tracking|Phase 07 — Learner Analytics & Mastery Tracking]]
* Adaptation Engine History (Phase 8): [[05 - Development History/Phase 08 — Adaptive Learning Intelligence Engine|Phase 08 — Adaptive Learning Intelligence Engine]]
