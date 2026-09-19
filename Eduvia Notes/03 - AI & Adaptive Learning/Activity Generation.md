# Activity Generation

All activities in Eduvia are structured JSON documents conforming strictly to Pydantic schemas.

---

## The 5 Initial Activity Types

1. **`matching`**: Connecting corresponding items across two columns (e.g., numeral "3" to three apples).
2. **`multiple_choice`**: Selecting the target item among 2 to 4 options with accessible distractors.
3. **`ordering`**: Arranging items along a sequential continuum (e.g., numbers 1, 2, 3, 4, 5).
4. **`visual_identification`**: Selecting an object or region within a visual scene.
5. **`drag_drop`**: Placing items into designated target zones.

---

## Validation Pipeline

```text
Prompt Template + Context (RAG + Profile)
                 │
                 ▼
          Gemini 1.5 Flash
                 │
                 ▼
         Raw JSON Response
                 │
                 ▼
     Pydantic Schema Validation ──(Fails)──► Fallback Deterministic Activity
                 │
             (Passes)
                 ▼
        Rendered Activity UI
```
