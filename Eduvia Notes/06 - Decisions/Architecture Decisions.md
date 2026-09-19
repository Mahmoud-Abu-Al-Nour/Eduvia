# Architecture Decisions (ADRs)

Key architectural decisions recorded across the project lifecycle.

---

### ADR 01: Modular Monolith Architecture
- **Decision**: Build Eduvia as a structured modular monolith rather than microservices for MVP.
- **Rationale**: Reduces distributed systems complexity, network latency, and operational overhead while maintaining clean boundaries between domains.

### ADR 02: PostgreSQL 16 + AsyncPG + SQLAlchemy 2.0
- **Decision**: Adopt native async PostgreSQL with SQLAlchemy 2.0.
- **Rationale**: High concurrency handling for classroom environments; native JSONB handles multi-lingual educational content cleanly.

### ADR 03: Qdrant Vector Database
- **Decision**: Select Qdrant as the dedicated vector database.
- **Rationale**: Superior payload filtering, robust gRPC/REST APIs, fast local development container, and production readiness.

### ADR 04: Decoupled LLM Provider Interface
- **Decision**: Isolate LLM operations behind `LLMProvider` abstract base class.
- **Rationale**: Prevents vendor lock-in to Gemini and enables deterministic mocking during automated testing.
