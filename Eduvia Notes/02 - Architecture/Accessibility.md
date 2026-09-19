# Accessibility (a11y)

Special educational needs software must set the gold standard for accessibility.

---

## Implementation Standards (WCAG 2.1 AA)

1. **Semantic Structure**:
   - Strict hierarchical headings (`<h1>` through `<h5>`).
   - Landmark regions (`<nav>`, `<main>`, `<section>`).
   - Breadcrumb navigation for nested hierarchy orientation.

2. **Keyboard Navigation & Focus**:
   - All interactive elements are native `<button>` or `<a>` elements with visible focus rings (`focus:ring-2 focus:ring-blue-500`).
   - Modal and drill-down flows preserve focus context.

3. **Cognitive Calm**:
   - Avoid strobe effects, flashing animations, and auto-playing sound.
   - High contrast text (exceeding 4.5:1 ratio for standard text).
   - Arabic RTL support with appropriate font families and spacing.

4. **Planned Multi-Modal Accessibility (Phase 5+)**:
   - Integrated Web Speech API / TTS for audio narration of activity prompts.
   - High-contrast switch-accessible layouts.
