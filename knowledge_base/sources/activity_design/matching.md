# Activity Design: Matching Modality

## Purpose
Structure relational association tasks where learners connect corresponding pairs (e.g. uppercase to lowercase letters, numerals to visual quantities, words to pictures, or routines to stages).

## When to Use
Use when building associational fluency, cross-representation mapping, or vocabulary-to-image binding.

## Core Principles
1. **Discrete Column Layout**: Clearly separate the left-side domain items from right-side target items.
2. **Deterministic Stable IDs**: Every left item and right item must possess a unique, immutable identifier (`left_id`, `right_id`).
3. **Partial Credit Support**: Support proportional scoring based on the fraction of accurately connected pairs.
4. **Persistent Pair Visualization**: Connected pairs must display clear visual lines, color bridges, or badge indicators.

## Practical Guidance
- Pair Count Guidelines:
  - Level 1: 2 pairs.
  - Level 2: 3 pairs.
  - Level 3: 4 pairs maximum.
- Interaction Pattern: Click/tap to select a left item, then click/tap the matching right item.
- Provide a clear "Clear Pair" or "Reset" mechanism for easy correction.

## Do and Do Not
- **Do**: Shuffle the presentation order of the right column relative to the left column.
- **Do**: Announce connection states via screen-reader live regions.
- **Do Not**: Overcrowd the screen with more than 5 pairs simultaneously.
- **Do Not**: Require complex mouse-dragging motions; tap-to-select and tap-to-match is mandatory for motor accessibility.

## Modality Contract Summary
- **Input Content**: `prompt`, `left_items`, `right_items`, `pairs` (target authoritative mappings).
- **Submission**: `pairs: list[MatchingPair]` with `left_id` and `right_id`.
- **Evaluation**: Server checks submitted pairs against target pairs. `score = correct_pairs / total_pairs`.

## References and Pedagogical Sources
- Mastropieri, M. A., & Scruggs, T. E. The Inclusive Classroom: Strategies for Effective Differentiated Instruction.
- CAST. Universal Design for Learning: Providing Multiple Means of Representation.
