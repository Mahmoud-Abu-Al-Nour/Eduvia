# Strategy Engine

The Strategy Engine is the deterministic decision layer that matches a learning objective to the optimal teaching strategy.

---

## The Adaptation Hierarchy

When a learner struggles or succeeds, adjustments occur in a defined order of precedence:

```text
1. Adjust Difficulty Level (within 1-5 scale)
        ↓ (if struggle persists)
2. Introduce Scaffolding / Adaptive Hints (Levels 1 to 3)
        ↓ (if struggle persists)
3. Change Activity Type (e.g., MCQ → Matching)
        ↓ (if struggle persists)
4. Change Teaching Strategy (e.g., Repetition → Step-by-Step)
        ↓ (if struggle persists)
5. Change Sensory Modality (e.g., Reading → Visual/Interactive)
```

This ensures continuity: we do not drastically jump modalities before exploring simple scaffolding adjustments.
