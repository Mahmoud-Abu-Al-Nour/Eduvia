# Predictable Interaction and Consistent Navigation

## Purpose
Foster emotional security and confidence by keeping interface behaviors, component states, and layout transitions completely predictable.

## When to Use
Apply across the learner activity shell, submission workflows, feedback displays, and transition dialogs.

## Core Principles
1. **Stable Spatial Anchor Points**: The prompt is always at the top, content in the center, and action buttons (Hints, Submit, Next) at the bottom.
2. **Immediate Visible State Changes**: Tapping an item immediately displays an active border, shadow, or checkmark.
3. **No Unprompted Layout Jumps**: Elements must not shift position unexpectedly while the user is reading or interacting.
4. **Uniform Submission Pattern**: Every activity requires an explicit, deliberate "Submit" action; no premature accidental submissions on single tap.

## Practical Guidance
- Button Locations:
  - "Need a Hint" always in a consistent bottom-left or top-right secondary location.
  - "Submit" button always prominently anchored at bottom-center or bottom-right.
- After submission, feedback card expands smoothly below the content without disorienting the learner.

## Do and Do Not
- **Do**: Require explicit confirmation or two-step tap before irreversible actions.
- **Do**: Announce page and state changes clearly using ARIA landmarks.
- **Do Not**: Automatically advance to the next activity before the learner chooses to proceed.
- **Do Not**: Reposition primary navigation controls across different activity types.

## References and Pedagogical Sources
- Nielsen, J. 10 Usability Heuristics for User Interface Design: Consistency and Standards.
- Mesibov, G. B., Shea, V., & Schopler, E. The TEACCH Approach to Autism Spectrum Disorders.
