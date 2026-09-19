# Open Questions

Active design questions requiring research, user alignment, or experimental validation before future implementation.

---

### 1. Scoring & Weighting Formula for Modalities
- **Status**: Open
- **Detail**: How rapidly should modality scores decay when a learner succeeds or struggles? What minimum evidence count is required before high confidence is declared?

### 2. Exploration vs Exploitation Ratio
- **Status**: Open
- **Detail**: In Phase 8 (Adaptive Engine), what percentage of activities should explore less-tested modalities versus exploiting the learner's highest-performing modality?

### 3. Standardized Curriculum Ingestion Source
- **Status**: Open
- **Detail**: Which formal curriculum standard (e.g., Common Core, UK National Curriculum, or regional SEN frameworks) will provide the canonical demonstration dataset?

### 4. Production Text-to-Speech Engine
- **Status**: Open
- **Detail**: Should production TTS rely on browser Web Speech API (zero latency/cost, variable voice quality) or Google Cloud Text-to-Speech (high naturalness, requires cloud credentials)?
