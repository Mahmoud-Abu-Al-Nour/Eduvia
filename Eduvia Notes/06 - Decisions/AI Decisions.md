# AI Decisions

Boundaries governing artificial intelligence within Eduvia.

---

### Decision 01: No Autonomous Pedagogical Decisions
- **Rule**: Gemini must **never** decide what a student learns or diagnose medical/cognitive conditions.
- **Enforcement**: Curriculum progression is determined by strict database mastery rules and teacher oversight.

### Decision 02: Strict Schema Generation
- **Rule**: AI output is restricted to typed JSON conforming to Pydantic models.
- **Enforcement**: Free-form markdown or HTML generation directly to the client is prohibited.

### Decision 03: Real Pedagogical Grounding
- **Rule**: Activity generation must be grounded in verified SEN and educational literature via Qdrant RAG.
