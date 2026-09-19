# Solution Overview

Eduvia acts as an intelligent adaptive mediation layer between a standardized educational curriculum and a neurodivergent learner.

---

## How It Works

```text
┌────────────────────────────────────────────────────────┐
│               Standard Curriculum Store                │
│    (Curriculum → Subject → Unit → Lesson → Objective)  │
└───────────────────────────┬────────────────────────────┘
                            │ Standard Objective
                            ▼
┌────────────────────────────────────────────────────────┐
│             Dynamic Personalization Engine             │
│   1. Inspects Learner Profile affinity & confidence    │
│   2. Retrieves evidence-based strategies from Qdrant   │
│   3. Generates structured activities using Gemini      │
│   4. Enforces accessible, distraction-free rendering   │
└───────────────────────────┬────────────────────────────┘
                            │ Interactive Session
                            ▼
┌────────────────────────────────────────────────────────┐
│             Mastery & Analytics Feedback               │
│   - Records time, accuracy, assistance required        │
│   - Updates modality & strategy effectiveness scores   │
│   - Feeds real-time progress to Teacher Dashboard      │
└────────────────────────────────────────────────────────┘
```

### Key Pillars
- **Curriculum Stability**: Curricula, units, and objectives are authored and reviewed by educational authorities or teachers. They are never hallucinated by AI.
- **Multi-Modal Generation**: Activities are structured JSON data rendered dynamically using clean, accessible UI components.
- **Assistive Technology Integration**: Integrated Text-to-Speech (TTS), keyboard-navigable layouts, and high-contrast colorways.
