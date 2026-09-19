# Eduvia Accessibility & Cognitive Calm

> **First-Class Accessibility Engineering and Sensory-Attuned User Experience for Neurodivergent Learners**

---

## The Philosophy of Cognitive Calm

Many educational platforms designed for children adopt high-intensity gamification: loud sound effects, flashing animations, countdown timers, and visually cluttered reward streaks. While intended to engage, these elements are actively exclusionary for neurodivergent learners—particularly students on the autism spectrum, individuals with ADHD, or those with sensory processing sensitivities. High sensory stimulation induces cognitive fatigue, triggers sensory overload, and shifts mental resources away from the academic concept toward processing environmental noise.

Eduvia is built on the engineering principle of **Cognitive Calm**:
1. **Zero Punitive Feedback**: An incorrect response does not trigger harsh red flashes, jarring buzzers, or penalty counters. The system responds with calm, constructive scaffolding (e.g., "Let's look at this together", "Here is a hint to help you think about it").
2. **Visual Economy & Generous Whitespace**: Screens present only the necessary interactive elements. Secondary toolbars and sidebars collapse during active learner sessions.
3. **Pacing Autonomy**: There are no artificial countdown timers or pressure-inducing timers. Students interact at their own cognitive tempo.
4. **Predictable Interaction Patterns**: The layout, typography, and response mechanisms remain consistent across all activity modalities, reducing procedural anxiety.

---

## 1. WCAG 2.1 AA Compliance & Implementation Architecture

Eduvia's frontend is certified against **WCAG 2.1 Level AA** standards across all learner and teacher interfaces. Accessibility is treated as a core architectural constraint rather than a cosmetic overlay.

### Architectural Accessibility Matrix

| Feature / Standard | Technical Implementation in Eduvia | Target Benefit |
| :--- | :--- | :--- |
| **Skip Navigation** | `<a href="#main-content" className="skip-link">` as first DOM node. Visible on focus. | Enables keyboard and screen-reader users to bypass navigation headers directly to the activity player. |
| **Keyboard Navigation** | Strict sequential `tabindex` management, visible high-contrast focus rings (`outline: 3px solid #2563EB`). | Full parity for users unable to operate a pointing device. |
| **Focus Trapping & Restoration** | Custom `useFocusTrap` hook intercepts `Tab` / `Shift+Tab` within modal dialogs, storing previous active element and restoring focus upon modal dismissal. | Prevents keyboard focus from escaping into obscured background DOM layers. |
| **ARIA Live Regions** | Dual live regions (`aria-live="polite"` for state updates; `aria-live="assertive"` for critical alerts) managed via `useAnnounce`. | Immediate, intelligible status feedback for non-visual screen-reader users. |
| **Touch Target Sizing** | Minimum interactive surface area of **$44 \times 44\text{ px}$** with adequate spacing margins. | Accommodates tremors, motor coordination differences, and touch screen tablets. |
| **High Contrast & Forced Colors** | Text contrast ratio exceeding **4.5:1** for standard text and **3:1** for large elements. Native support for Windows High Contrast Mode (`@media (forced-colors: active)`). | Legibility for low-vision learners and visual clarity in diverse lighting environments. |
| **Reduced Motion** | CSS animations and transitions are wrapped in `@media (prefers-reduced-motion: reduce)` to disable non-essential motion. | Prevents vestibular disorientation, motion sickness, and distraction. |
| **Color-Independent State** | Error, success, and warning states pair color changes with text labels and distinct semantic icons (e.g., Checkmark, Information Circle, Exclamation Triangle). | Full intelligibility for learners with color vision deficiencies. |

---

## 2. Keyboard & Single-Switch Interaction Bindings

Eduvia provides dedicated, global switch-accessible keybindings within the `ActivityPlayer` to ensure learners with motor impairments or assistive switch interfaces can operate the software independently:

```text
┌─────────────────────────────────────────────────────────────┐
│                 Accessible Input Bindings                   │
├──────────────────┬──────────────────────────────────────────┤
│ Key [ 1 ] – [ 4 ]│ Direct selection of options 1 through 4   │
├──────────────────┼──────────────────────────────────────────┤
│ Key [ Space ]    │ Activate selected element / Toggle check │
├──────────────────┼──────────────────────────────────────────┤
│ Key [ Enter ]    │ Submit response / Confirm current action │
├──────────────────┼──────────────────────────────────────────┤
│ Key [ H ]        │ Request hint / Escalate scaffolding level│
├──────────────────┼──────────────────────────────────────────┤
│ Key [ R ]        │ Replay audio narration via TTS           │
└──────────────────┴──────────────────────────────────────────┘
```

### Switch Access Compatibility
Assistive hardware switches (such as sip-and-puff devices, foot pedals, or large head switches) commonly map hardware clicks to `Space`, `Enter`, or number keys. Eduvia's predictable key mapping enables single-switch and dual-switch users to navigate and submit activities without requiring third-party remapping software.

---

## 3. Text-to-Speech (TTS) Integration

Eduvia integrates native multi-modal speech support via the browser's **Web Speech API (`SpeechSynthesis`)**:
* **Automated Audio Narration**: Activity instructions, option labels, and scaffolding hints can be spoken aloud automatically upon presentation.
* **Non-Blocking Control**: The speech controller provides clear visual indicators when audio is playing, allowing the student to pause, resume, or replay narration using the `[R]` shortcut or a high-contrast speaker button.
* **Rate & Pitch Calibration**: Speech rate is calibrated to a gentle, intelligible pace ($0.9\times$ normal speed) to accommodate auditory processing differences.

---

## 4. Visual Ergonomics & Semantic Layout

### Typographic Hierarchy
* Standardized font stack prioritizing clean, open letterforms (e.g., Inter, system sans-serif) with generous line heights ($1.5\times$) and letter spacing.
* Clear distinctions between headings (`<h1>`, `<h2>`) and interactive text, maintaining an unbroken document outline.

### Sensory Accommodation Profiles
Through the `LearnerProfile` domain model, teachers can configure individualized UI accommodations for specific learners:
* **High Contrast Mode**: Forces extreme dark-on-light or light-on-dark contrast palettes.
* **Reduced Visual Density**: Increases font sizes and element spacing while hiding decorative illustrations.
* **Audio-First Delivery**: Automatically triggers TTS narration upon loading each activity step.

---

## Related Documentation

* Master Overview: [[Eduvia Project Overview & Technical Abstract|Eduvia Project Overview & Technical Abstract]]
* System Architecture: [[Eduvia Architecture & System Design|Eduvia Architecture & System Design]]
* Personalization & Adaptation: [[Eduvia Learning & Personalization Approach|Eduvia Learning & Personalization Approach]]
* Frontend Architecture: [[02 - Architecture/Frontend Architecture|Frontend Architecture]]
* Accessibility Deep Dive: [[02 - Architecture/Accessibility|Accessibility (a11y)]]
* Phase 11 Hardening History: [[05 - Development History/Phase 11 — System Hardening & Accessibility Audit|Phase 11 — System Hardening & Accessibility Audit]]
