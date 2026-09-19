# Eduvia User Workflows

> **End-to-End Operational Lifecycle for Special Educators and Sensory-Attuned Learners**

---

## The Dual-Experience Paradigm

Eduvia operates two distinct, purpose-built interfaces connected by a shared data and evaluation engine:
1. **The Learner Experience**: A distraction-free, accessible workspace focused on calm engagement, multi-sensory representation, and progressive scaffolding.
2. **The Teacher Experience**: A governance, analytics, and reporting dashboard providing cohort mastery matrices, deterministic intervention alerts, and exportable IEP progress records.

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                      Teacher Workflow                       │
 │  Cohort Setup ➔ Curriculum Assign ➔ Monitoring ➔ IEP Export │
 └──────────────────────────────┬──────────────────────────────┘
                                │ Controls & Assignments
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                      Learner Workflow                       │
 │  Select Activity ➔ Interact ➔ Scaffolding ➔ Eval ➔ Telemetry│
 └──────────────────────────────┬──────────────────────────────┘
                                │ Telemetry & Mastery Events
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                 Aggregated Intelligence                     │
 │  Alert Generation ➔ Recommendations ➔ Longitudinal Insights │
 └─────────────────────────────────────────────────────────────┘
```

---

## 1. The Learner Lifecycle & Activity Flow

```text
[1. Objective Presentation]
             │
             ▼
[2. Dynamic Activity Generation] (Visual ID, Matching, Ordering, MC, Drag-and-Drop)
             │
             ▼
[3. Accessible Presentation] (TTS Narration, Keyboard Bindings, High-Contrast)
             │
             ├── Learner requests assistance ──▶ [4. Progressive Scaffolding]
             │                                   (Level 1 Hint ➔ Level 2 Cue ➔ Level 3 Demo)
             ▼
[5. Learner Submission] (Selected Option, Ordered Items, Matched Targets)
             │
             ▼
[6. Authoritative Server Evaluation] (Server compares against answer key; calculates score)
             │
             ▼
[7. Cognitive Calm Feedback] (Encouraging guidance, zero harsh buzzers/red flashes)
             │
             ▼
[8. Immutable Telemetry Logging] (Latency, attempts, and assistance level persisted)
             │
             ▼
[9. Adaptive Next Activity] (Difficulty adjusted or prerequisite reinforced)
```

### Key Stages in the Learner Journey
1. **Entry & Context**: The learner enters a clean, uncluttered session. Any unnecessary navigation bars are minimized.
2. **Audio-Visual Grounding**: The activity prompt is displayed in clear typography and can be read aloud automatically via native Text-to-Speech (TTS).
3. **Multi-Modal Interaction**: The learner responds using touch, mouse, keyboard shortcuts (`[1]–[4]`, `[Space]`, `[Enter]`), or assistive single switches.
4. **Scaffolding on Demand**: If uncertain, the learner presses `[H]` or clicks the lightbulb icon. Scaffolding escalates gently:
   * First request: Gentle conceptual hint.
   * Second request: Elimination of incorrect choices.
   * Third request: Explicit step-by-step guidance.
5. **Calm Resolution**: Regardless of outcome, the feedback is constructive, reinforcing effort and providing an immediate path forward.

---

## 2. The Teacher Lifecycle & Governance Flow

```text
[1. Cohort & Learner Management] (Create learner profiles, assign sensory preferences)
             │
             ▼
[2. Curriculum Assignment & Locking] (Set target objectives, toggle prerequisite locks)
             │
             ▼
[3. Real-Time Cohort Monitoring] (Inspect active sessions, accuracy rates, attempt volumes)
             │
             ▼
[4. Deterministic Intervention Alerts] (Review system-flagged students needing support)
             │
             ▼
[5. Recommendation Review] (Examine system-suggested next steps and pedagogical rationale)
             │
             ├── Teacher agrees ──▶ System applies recommendation
             │
             └── Teacher overrides ──▶ Manual curriculum or modality lock enforced
             │
             ▼
[6. IEP Progress Report Generation] (Export multi-format audit reports: Print, Markdown, JSON)
```

### Key Stages in the Teacher Journey
1. **Learner Onboarding**: The teacher records the learner's grade, age, and initial accommodation settings (e.g., preferred sensory modalities, high-contrast preference).
2. **Curriculum Pacing**: The teacher selects standardized objectives from the 5-level curriculum browser. They can lock specific objectives or allow the adaptive engine to traverse prerequisites automatically.
3. **Classroom Cohort Dashboard**: The teacher monitors the aggregate progress of their assigned students, viewing mastery rates, active attempts, and average scaffolding reliance across the classroom.
4. **Intervention Alert Analysis**: The system triggers non-diagnostic alerts when a learner exhibits persistent failure ($\ge 3$ consecutive incorrect attempts) or heavy scaffolding dependence. The teacher reviews the specific error pattern.
5. **IEP Progress Reporting**: When preparing for quarterly IEP reviews or parent-teacher conferences, the educator generates a comprehensive longitudinal report with a single click, detailing objective-level mastery, independence ratios, and historical attempt timelines.

---

## 3. Separation of Responsibilities

Eduvia enforces a strict separation between learner and teacher roles:

| Dimension | Learner Role | Teacher Role |
| :--- | :--- | :--- |
| **Curriculum Scope** | Experiences activities assigned or dynamically recommended within active objectives. | Full governance: can add, remove, lock, or override objectives and prerequisite dependencies. |
| **Sensory Accommodations** | Interacts through pre-configured visual and auditory accommodations. | Configures baseline sensory settings, high-contrast mode, and TTS defaults on learner profile. |
| **Evaluation Authority** | Submits interaction payloads; receives constructive feedback. | Inspects raw interaction telemetry, error distributions, and assistance level analytics. |
| **Adaptation Governance** | Beneficiary of calibrated difficulty and scaffolding shifts. | Ultimate authority: can override algorithmic recommendations at any time. |
| **Data Visibility** | Sees immediate personal activity feedback and calm progress indicators. | Multi-tenant access to all assigned learners, cohort mastery matrices, and IEP audit exports. |

---

## Related Documentation

* Master Overview: [[Eduvia Project Overview & Technical Abstract|Eduvia Project Overview & Technical Abstract]]
* System Architecture: [[Eduvia Architecture & System Design|Eduvia Architecture & System Design]]
* Personalization & Adaptation: [[Eduvia Learning & Personalization Approach|Eduvia Learning & Personalization Approach]]
* Accessibility & Cognitive Calm: [[Eduvia Accessibility & Cognitive Calm|Eduvia Accessibility & Cognitive Calm]]
* Teacher Dashboard Details: [[05 - Development History/Phase 10 — Teacher Dashboard & Insights|Phase 10 — Teacher Dashboard & Insights]]
