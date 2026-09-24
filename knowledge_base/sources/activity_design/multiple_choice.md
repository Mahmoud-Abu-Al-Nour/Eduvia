# Activity Design: Multiple Choice Modality

## Purpose
Structure single-target recognition and discrete selection tasks while eliminating extraneous cognitive load, trickery, or sensory distraction.

## When to Use
Use when evaluating discrete identification, factual recognition, numeral identification, letter recognition, or simple problem solving.

## Core Principles
1. **Unambiguous Question Stem**: The prompt must explicitly state what is being asked in clear, concise language.
2. **Plausible, Non-Tricky Distractors**: Distractors should reflect common learner approximations without punning or semantic confusion.
3. **Controlled Option Count**:
   - Level 1: 2 options (1 correct, 1 distractor).
   - Level 2: 3 options (1 correct, 2 distractors).
   - Level 3: 4 options maximum.
4. **Stable Selection State**: Selected options must remain visually highlighted until submitted.

## Practical Guidance
- Maintain balanced option lengths and visual complexity.
- Support both text and icon/visual representations in option payloads.
- Use high-contrast focus rings and large tap targets (minimum 48x48px).

## Do and Do Not
- **Do**: Include reassuring, informative feedback upon evaluation.
- **Do**: Support full keyboard navigation (Tab, Arrow keys, Enter/Space to select).
- **Do Not**: Include "All of the above" or "None of the above" options, which introduce excessive logical negation.
- **Do Not**: Randomize options on retry without resetting the learner's focus context.

## Modality Contract Summary
- **Input Content**: `prompt`, `options` (id, text, icon), `correct_answer_id`, `explanation`.
- **Submission**: `selected_option_id`.
- **Evaluation**: Server checks `selected_option_id == content.correct_answer_id`. Score is 1.0 or 0.0.

## References and Pedagogical Sources
- Haladyna, T. M., Downing, S. M., & Rodriguez, M. C. A review of multiple-choice item-writing guidelines for classroom assessment.
- CAST (Center for Applied Special Technology). Universal Design for Learning Guidelines: Multiple Means of Action and Expression.
