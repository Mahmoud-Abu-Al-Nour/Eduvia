# Activity Design: Drag and Drop (Categorization) Modality

## Purpose
Structure classification, sorting, and categorization tasks where learners distribute items into designated destination zones.

## When to Use
Use when teaching classification by shape, size, color, letter category (vowel vs consonant), or sorting objects into daily routine buckets.

## Core Principles
1. **Modal Accessibility Requirement**: Pointer-based dragging must be paired with tap-to-select + tap-to-place and full keyboard navigation.
2. **Clear Drop Zones**: Drop zones must have distinct borders, clear category headers, and accessible count indicators.
3. **Item Independence**: Each draggable item maintains a stable identifier (`id`) and is mapped to an authoritative target zone (`zone_id`).
4. **Reversible Placement**: Learners must be able to move an item from one zone to another or back to the unassigned tray with ease.

## Practical Guidance
- Zone and Item Counts:
  - Level 1: 2 zones, 2–3 items total.
  - Level 2: 2 zones, 4 items total.
  - Level 3: 3 zones, 6 items maximum.
- Interaction Workflow for Motor Accessibility:
  1. Tab to or click/tap an item in the tray (item enters "selected" state).
  2. Tab to or click/tap the desired drop zone (item moves into zone).
  3. Announce the placement via ARIA live region (e.g. "Triangle placed in Shapes with 3 Sides").

## Do and Do Not
- **Do**: Support both mouse drag and tap-based two-step selection.
- **Do**: Allow partial credit scoring based on correctly placed items.
- **Do Not**: Fail or lock an interaction if a mouse drag event drops outside a designated zone.
- **Do Not**: Make drop zones smaller than 80x80px.

## Modality Contract Summary
- **Input Content**: `prompt`, `items` (id, text, icon), `zones` (id, label), `correct_mapping` (dict mapping `item_id` to `zone_id`).
- **Submission**: `item_to_zone_mapping: dict[str, str]`.
- **Evaluation**: Server checks submitted mapping against `correct_mapping`. `score = correct_items / total_items`.

## References and Pedagogical Sources
- W3C WAI-ARIA Authoring Practices: Drag and Drop Alternatives.
- UDL Guidelines: Multiple Means of Action and Expression (Principle 4).
