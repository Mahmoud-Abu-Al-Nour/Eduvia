# Adaptive Learning Intelligence Engine

The Adaptive Learning Intelligence Engine is the core system responsible for personalizing instructional delivery while preserving curriculum integrity.

---

## Subsystem Architecture

```text
Adaptive Learning Intelligence Engine
│
├── Learner Profiler        → Maintains dynamic modality & strategy affinity states
├── Learning Analytics      → Computes mastery levels, error patterns, and latencies
├── Strategy Engine         → Selects optimal pedagogical strategy using deterministic logic
├── Curriculum Engine       → Supplies validated objectives, prerequisites, and standards
├── Activity Generator      → Produces structured activity JSON via Gemini + RAG
├── Activity Evaluator      → Scores learner submissions and calculates assistance required
├── Adaptation Engine       → Orchestrates real-time hints, difficulty shifts, and transitions
├── Recommendation Engine   → Recommends next objectives along the prerequisite graph
└── Strategy Explainer      → Generates clear, human-readable rationale for teachers
```

---

## The Non-Negotiable Rule: Determinism vs Generation

> **Gemini is NOT the decision maker.**

- **Deterministic Rules Engine**: Calculates whether a learner has met the mastery threshold (e.g., accuracy >= 80% with assistance <= level 1), when to step back to a prerequisite, and which modality has the highest empirical confidence.
- **Generative LLM (Gemini)**: Generates the pedagogical text, questions, distractors, and narrative scaffolding fitting the parameters specified by the Strategy Engine.
