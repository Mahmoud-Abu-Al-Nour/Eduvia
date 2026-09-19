# Gemini Integration

Eduvia integrates Google Gemini as its primary generative foundation.

---

## Boundary Implementation

All LLM calls pass through the abstract interface `LLMProvider` (`backend/app/ai/providers/base.py`):
- Concrete provider: `GeminiProvider` (`backend/app/ai/providers/gemini.py`).
- Decoupled from business logic via `AIOrchestrator`.
- Lazy loading: The `google.generativeai` package is imported only on demand; absence of an API key in local development does not prevent the web server from booting or curriculum browsing from working.
- Structured output: Gemini's JSON mode is leveraged with strict system prompt schemas.
- Known Non-Blocking Notice: Package deprecation warning from `google.generativeai` is cataloged and formally deferred to Phase 9.


