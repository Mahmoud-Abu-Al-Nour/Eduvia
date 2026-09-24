# Eduvia — Activity Modality Technical Contract

This document provides the authoritative technical contract for all five activity modalities supported across Eduvia.

## Architectural Guarantees
1. **Authoritative Server Evaluation**: Correctness is **never** evaluated or accepted from the frontend. The learner client submits interaction decisions only (`selected_option_id`, `pairs`, `ordered_ids`, `selected_element_id`, `item_to_zone_mapping`).
2. **Hidden Answer Keys**: Authoritative answer keys (`correct_answer_id`, `pairs`, `correct_sequence`, `target_id`, `correct_mapping`) are excluded from learner activity payloads where security demands it.
3. **Accessibility Parity**: All modalities support dual interaction modes: direct pointer/touch interaction and sequential keyboard/switch-accessible interaction.
4. **Deterministic Fallbacks**: Every objective has a deterministic Content Bank item ensuring the Zero-Strand Guarantee if LLM generation fails or times out.

---

## 1. Multiple Choice (`multiple_choice`)

- **Purpose**: Single-target selection among discrete alternative choices.
- **Input Content Schema**:
  ```json
  {
    "activity_type": "multiple_choice",
    "prompt": "How many apples are shown?",
    "options": [
      { "id": "opt-1", "text": "3", "icon": null },
      { "id": "opt-2", "text": "5", "icon": null },
      { "id": "opt-3", "text": "7", "icon": null }
    ],
    "correct_answer_id": "opt-2",
    "explanation": "Counting each apple gives a total of 5."
  }
  ```
- **Rendering & Interaction**:
  - Options rendered as large button tiles (minimum 48x48px target).
  - Keyboard navigation via `Tab`, `Arrow Up/Down`, `Space`/`Enter` to select.
  - Selected option highlighted with high-contrast border and check indicator.
- **Submission Payload**:
  ```json
  {
    "activity_type": "multiple_choice",
    "selected_option_id": "opt-2"
  }
  ```
- **Backend Evaluation**:
  - `is_correct = (selected_option_id == content.correct_answer_id)`
  - `score = 1.0` if correct, else `0.0`.
- **Telemetry**: Records `activity_type="multiple_choice"`, `modality="visual"`, `score`, `hints_used`.

---

## 2. Matching (`matching`)

- **Purpose**: Relational association connecting corresponding items between two domains.
- **Input Content Schema**:
  ```json
  {
    "activity_type": "matching",
    "prompt": "Match each uppercase letter to its lowercase letter.",
    "left_items": [
      { "id": "L1", "text": "A", "icon": null },
      { "id": "L2", "text": "B", "icon": null }
    ],
    "right_items": [
      { "id": "R1", "text": "b", "icon": null },
      { "id": "R2", "text": "a", "icon": null }
    ],
    "pairs": [
      { "left_id": "L1", "right_id": "R2" },
      { "left_id": "L2", "right_id": "R1" }
    ]
  }
  ```
- **Rendering & Interaction**:
  - Two distinct columns (left items and right items).
  - Accessible tap-to-select: click left item, then click right item to form pair.
  - Visual bridge / color badge indicates formed pairs. Clear button allows re-pairing.
- **Submission Payload**:
  ```json
  {
    "activity_type": "matching",
    "pairs": [
      { "left_id": "L1", "right_id": "R2" },
      { "left_id": "L2", "right_id": "R1" }
    ]
  }
  ```
- **Backend Evaluation**:
  - Authoritative pairs set comparison: `matched = submitted.intersection(target)`.
  - `score = round(len(matched) / len(target), 2)`.
  - `is_correct = (len(matched) == len(target) and len(submitted) == len(target))`.
- **Telemetry**: Records `activity_type="matching"`, `modality="interactive"`, `score`, partial credit preserved.

---

## 3. Ordering (`ordering`)

- **Purpose**: Sequential and chronological arrangement.
- **Input Content Schema**:
  ```json
  {
    "activity_type": "ordering",
    "prompt": "Arrange the numbers from smallest to largest.",
    "items": [
      { "id": "num-3", "text": "3", "icon": null, "position": 0 },
      { "id": "num-1", "text": "1", "icon": null, "position": 1 },
      { "id": "num-2", "text": "2", "icon": null, "position": 2 }
    ],
    "correct_sequence": ["num-1", "num-2", "num-3"],
    "direction": "ascending"
  }
  ```
- **Rendering & Interaction**:
  - Horizontal or vertical slot grid with position badges (1st, 2nd, 3rd).
  - Supports both pointer drag-and-drop and accessible "Move Left / Move Right" action buttons.
- **Submission Payload**:
  ```json
  {
    "activity_type": "ordering",
    "ordered_ids": ["num-1", "num-2", "num-3"]
  }
  ```
- **Backend Evaluation**:
  - Slot-by-slot comparison: `matching_slots = sum(1 for a, b in zip(ordered_ids, correct_sequence) if a == b)`.
  - `score = round(matching_slots / total, 2)`.
  - `is_correct = (ordered_ids == correct_sequence)`.
- **Telemetry**: Records `activity_type="ordering"`, `modality="interactive"`.

---

## 4. Visual Identification (`visual_identification`)

- **Purpose**: Visual search, discrimination, and target identification in sensory-calm scenes.
- **Input Content Schema**:
  ```json
  {
    "activity_type": "visual_identification",
    "prompt": "Find the circle in the group below.",
    "scene_description": "Four basic geometric shapes arranged in a 2x2 grid.",
    "elements": [
      { "id": "shape-sq", "label": "Square", "visual_data": { "shape": "square" } },
      { "id": "shape-circ", "label": "Circle", "visual_data": { "shape": "circle" } }
    ],
    "target_id": "shape-circ",
    "feedback_clue": "A circle is perfectly round with no sharp corners."
  }
  ```
- **Rendering & Interaction**:
  - High-contrast visual representations (deterministic SVG / CSS / symbols).
  - Keyboard tab navigation across elements; selected element highlighted.
- **Submission Payload**:
  ```json
  {
    "activity_type": "visual_identification",
    "selected_element_id": "shape-circ"
  }
  ```
- **Backend Evaluation**:
  - `is_correct = (selected_element_id == content.target_id)`.
  - `score = 1.0` if correct, else `0.0`.
- **Telemetry**: Records `activity_type="visual_identification"`, `modality="visual"`.

---

## 5. Drag and Drop (`drag_drop`)

- **Purpose**: Categorization, bin sorting, and set distribution.
- **Input Content Schema**:
  ```json
  {
    "activity_type": "drag_drop",
    "prompt": "Sort the objects into Big and Small boxes.",
    "items": [
      { "id": "item-elephant", "text": "Elephant", "icon": "🐘" },
      { "id": "item-ant", "text": "Ant", "icon": "🐜" }
    ],
    "zones": [
      { "id": "zone-big", "label": "Big Objects" },
      { "id": "zone-small", "label": "Small Objects" }
    ],
    "correct_mapping": {
      "item-elephant": "zone-big",
      "item-ant": "zone-small"
    }
  }
  ```
- **Rendering & Interaction**:
  - Draggable items in unassigned source tray, drop zones clearly labeled.
  - Dual interaction: Mouse/touch drag-and-drop OR accessible two-step click (tap item -> tap destination zone).
- **Submission Payload**:
  ```json
  {
    "activity_type": "drag_drop",
    "item_to_zone_mapping": {
      "item-elephant": "zone-big",
      "item-ant": "zone-small"
    }
  }
  ```
- **Backend Evaluation**:
  - Mapping comparison: `correct_count = sum(1 for k, v in submitted.items() if correct_mapping.get(k) == v)`.
  - `score = round(correct_count / total, 2)`.
  - `is_correct = (correct_count == total and len(submitted) == total)`.
- **Telemetry**: Records `activity_type="drag_drop"`, `modality="interactive"`.
