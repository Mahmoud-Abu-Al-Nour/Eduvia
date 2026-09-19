# Learner Profile

The Learner Profile represents the evolving model of a student's learning affinities.

---

## Modality Representation

Rather than rigid categorizations ("Visual Learner"), the profile tracks five sensory modalities:

```text
- Visual        (image, diagram, color coding)
- Reading/Text  (written instructions, narrative)
- Writing       (typed or written input)
- Audio         (spoken instructions, sound cues)
- Interactive   (drag-and-drop, manipulation, ordering)
```

Each modality maintains:
1. **Score**: Current estimated effectiveness ($0.0 - 1.0$).
2. **Confidence**: Statistical confidence in the score ($0.0 - 1.0$).
3. **Evidence Count**: Total historical attempts using this modality.

---

## Teaching Strategy Representation

The profile similarly tracks responsiveness to eight evidence-based pedagogical strategies:

1. `step_by_step` (deconstructing tasks into atomic sequential units)
2. `repetition` (structured spaced recurrence)
3. `scaffolding` (initial heavy prompting faded over time)
4. `prompting` (verbal, visual, or physical hints)
5. `simplification` (reducing vocabulary or syntactic complexity)
6. `demonstration` (worked examples shown prior to attempt)
7. `positive_reinforcement` (immediate encouraging milestone feedback)
8. `gradual_difficulty` (incremental challenge progression)
