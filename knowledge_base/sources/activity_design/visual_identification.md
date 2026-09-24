# Activity Design: Visual Identification Modality

## Purpose
Structure visual search, spatial discrimination, and target identification within a structured sensory-safe scene or visual grid.

## When to Use
Use when teaching shape recognition, visual counting (e.g. "Find the group with 5 stars"), object discrimination, or identifying a target letter among visual distractors.

## Core Principles
1. **Local Deterministic Visuals**: Use clean SVG, structured CSS, or emoji/unicode symbols rather than external remote image dependencies.
2. **Sensory-Safe Visual Density**: Limit scene elements to prevent sensory overload (maximum 3–6 distinct items).
3. **High Figure-Ground Contrast**: Ensure visual targets stand out clearly against a calm, neutral background.
4. **Authoritative Target ID**: Server evaluation must match against a stable `target_id`, completely independent of visual rendering assets.

## Practical Guidance
- Element Placement: Arrange elements in an organized grid or calm tableau rather than random scatter.
- Target Distractors: Distractors should differ by 1 salient attribute (e.g. count or shape) rather than cluttered irrelevant differences.
- Feedback Clue: Provide a deterministic verbal or visual clue explaining why the target is correct.

## Do and Do Not
- **Do**: Support keyboard navigation across all visual scene elements.
- **Do**: Provide text alternatives (`label` / `aria-label`) for every visual element.
- **Do Not**: Include blinking, flashing, or rapid visual animations.
- **Do Not**: Depend on color alone to differentiate targets (e.g. combine color with shape or label).

## Modality Contract Summary
- **Input Content**: `prompt`, `scene_description`, `elements` (id, label, visual_data), `target_id`, `feedback_clue`.
- **Submission**: `selected_element_id`.
- **Evaluation**: Server checks `selected_element_id == content.target_id`. Score is 1.0 or 0.0.

## References and Pedagogical Sources
- Mayer, R. E. Cognitive Theory of Multimedia Learning.
- Treisman, A., & Gelade, G. A feature-integration theory of attention.
