# Motor Accessibility and Switch-Access Compatibility

## Purpose
Ensure all activity modalities can be operated independently by learners with limited fine motor dexterity, tremors, cerebral palsy, or those using single/dual switch access and eye-gaze hardware.

## When to Use
Apply to all interactive components, drag-and-drop operations, matching bridges, and sequence ordering.

## Core Principles
1. **Full Keyboard Parity**: Every action achievable with a mouse or touch must be 100% achievable using standard keyboard navigation (Tab, Shift+Tab, Space, Enter, Arrow keys).
2. **Target Size & Spacing**: Generous click/touch targets (minimum 48x48px, ideally 64x64px for early childhood/elementary).
3. **No Precision Drag Requirement**: Provide step-by-step click/tap alternatives for drag-and-drop (select item, then select target slot).
4. **Switch Navigation Support**: Sequential linear focus paths without keyboard traps, compatible with single-switch scanning.

## Practical Guidance
- Drag & Drop: Tap item to select (highlighted with active ring) -> tap target drop zone to place.
- Matching: Tap item in left column -> tap corresponding item in right column.
- Ordering: Provide "Move Up / Move Down" or "Move Left / Move Right" buttons alongside direct slot reordering.

## Do and Do Not
- **Do**: Maintain focus stability; moving an item should keep keyboard focus on the relocated element or its container.
- **Do**: Allow ample time to respond without timing out.
- **Do Not**: Require complex multi-finger gestures, pinch-to-zoom, or high-velocity mouse swipes.
- **Do Not**: Trap keyboard focus within any modal or interactive canvas.

## References and Pedagogical Sources
- W3C Web Accessibility Initiative: Accessible Rich Internet Applications (WAI-ARIA) 1.2.
- Inclusive Design Research Centre (IDRC). Motor and Physical Accessibility Guidelines.
