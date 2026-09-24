# Activity Design: Ordering Modality

## Purpose
Structure sequential organization and chronological ordering tasks (e.g. number sequences, chronological routine steps, alphabetical ordering).

## When to Use
Use when teaching sequential thinking, before/after concepts, numerical progression, story sequencing, or procedure completion.

## Core Principles
1. **Explicit Directionality**: Always declare and display sequence direction (e.g. "Left to Right", "Smallest to Largest", "First to Last").
2. **Stable Component IDs**: Each card or element maintains a stable identifier regardless of current slot position.
3. **Dual Reordering Modes**:
   - Keyboard accessible reordering: Move Left / Move Right buttons or number-key slot placement.
   - Pointer accessible reordering: Drag or tap swap.
4. **Initial Scramble**: Initial display must present items in non-ordered arrangements to ensure active cognitive retrieval.

## Practical Guidance
- Sequence Lengths:
  - Level 1: 3 items (e.g. 1, 2, 3 or First, Next, Last).
  - Level 2: 4 items (e.g. 2, 4, 6, 8 or 4-step morning routine).
  - Level 3: 5 items maximum.
- Provide numbered slot indicators to help learners understand where each element will be positioned.

## Do and Do Not
- **Do**: Clearly display current position numbers (1st, 2nd, 3rd).
- **Do**: Give partial credit for items placed in their authoritative target slot.
- **Do Not**: Rely on drag-and-drop as the sole interaction mechanism.
- **Do Not**: Use ambiguous temporal steps where two events could occur interchangeably.

## Modality Contract Summary
- **Input Content**: `prompt`, `items` (id, text, icon, position), `correct_sequence` (ordered list of item IDs), `direction`.
- **Submission**: `ordered_ids: list[str]`.
- **Evaluation**: Server compares `ordered_ids` index-by-index against `correct_sequence`. `score = matching_slots / total_items`.

## References and Pedagogical Sources
- Case, R. The role of the central conceptual structure in the development of children's numerical and spatial thought.
- TEACCH Autism Program. Structured Teaching and Visual Sequences.
