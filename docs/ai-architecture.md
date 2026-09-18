# Eduvia — AI Architecture

## Design Principle

Eduvia uses AI as an informed generator, not an autonomous decision maker.

```
Educational Knowledge (RAG)
       +
Learner Profile (Data)
       +
Curriculum Objective (Structure)
       ↓
AI Orchestrator
       ↓
Structured Activity Schema
       ↓
Pydantic Validation
       ↓
Learner Interface
```

Gemini is responsible for:
- Generating structured activity content from validated context
- Producing strategy explanations from observed data

Gemini is NOT responsible for:
- Inventing curriculum
- Diagnosing learners
- Making autonomous adaptation decisions
- Generating arbitrary HTML or UI code

---

## LLM Provider Interface

All AI access goes through the abstract `LLMProvider` interface:

```python
class LLMProvider(ABC):
    @property
    def provider_name(self) -> str: ...
    @property
    def is_available(self) -> bool: ...

    async def generate(messages, config) -> LLMResponse: ...
    async def generate_structured(messages, schema, config) -> dict: ...
    async def health_check() -> bool: ...
```

Current implementation: `GeminiProvider`

To add a new provider: implement `LLMProvider` → register in `get_ai_orchestrator()`

---

## Activity Generation

Activities are generated as validated JSON schemas — not UI code:

```
Gemini → Structured JSON → Pydantic Model → React Renderer
```

Supported activity types (Phase 4+):
1. `matching` — Pair left/right items
2. `multiple_choice` — Select correct answer
3. `ordering` — Arrange items in sequence
4. `visual_identification` — Identify target in image
5. `drag_drop` — Map items to targets

---

## Learning Modalities Tracked

| Modality | Description |
|----------|-------------|
| `visual` | Image/diagram-based activities |
| `reading` | Text-heavy content |
| `writing` | Written response activities |
| `audio` | Audio-supported activities |
| `interactive` | Hands-on drag, match activities |

Each modality maintains: `score`, `confidence`, `evidence_count`

---

## Teaching Strategies Tracked

| Strategy | Description |
|----------|-------------|
| `step_by_step` | Sequential instruction |
| `repetition` | Repeat until mastered |
| `scaffolding` | Progressive support |
| `prompting` | Cue-based guidance |
| `simplification` | Reduced complexity |
| `demonstration` | Model first |
| `positive_reinforcement` | Reward-based |
| `gradual_difficulty` | Incremental challenge |

---

## Adaptation Logic (Phase 8)

```
Level 1: Adjust Difficulty
         ↓ (if still struggling)
Level 2: Add Hints / Scaffolding
         ↓ (if still struggling)
Level 3: Change Activity Type
         ↓ (with sufficient evidence)
Level 4: Change Teaching Strategy
         ↓ (with strong evidence)
Level 5: Change Modality
```

Evidence required before modality change: configurable threshold (default: 5+ interactions).

---

## RAG Knowledge Base (Phase 9)

Collections in Qdrant:
- `eduvia_knowledge` — General educational/pedagogical knowledge
- `eduvia_curriculum` — Curriculum objectives and content

Knowledge categories:
- Learning objectives
- Educational strategies
- Scaffolding approaches
- Visual learning strategies
- Prompting techniques
- Repetition strategies
- Simplification approaches
- Reinforcement principles
- Accessibility guidelines
- Activity design principles

---

## Responsible AI Guidelines

The AI system MUST NOT:
- Diagnose intellectual disability
- Diagnose autism or psychological conditions
- Make medical claims about learners
- Replace teacher judgment
- Make unsupported cognitive claims

The AI system MUST:
- Use educational language only (e.g., "observed performance", "activity effectiveness")
- Provide explainable recommendations
- Base recommendations on measured interaction data
- Allow teacher override of all recommendations
- Flag low-confidence recommendations clearly

---

## Explainability Format (Phase 8+)

```
Recommended Approach

Visual + Interactive

Why?

Recent activities using visual and interactive presentation
produced higher accuracy (0.78) and lower assistance requirements
(1.2 avg hints) for this learner over the last 12 activities.

Confidence: High (0.89 | 27 evidence events)
```

All explanations must be derived from measurable learner data — no speculation.
