# System Architecture

Eduvia is engineered as a **Modular Monolith** optimized for reliability, testability, and low operational complexity, with a clear cloud-native evolution path.

---

## High-Level Topology

```text
       [ Browser / Client ]
                 │
                 │ HTTP/JSON
                 ▼
       ┌──────────────────┐
       │   FastAPI App    │ (Uvicorn ASGI)
       └─────────┬────────┘
                 │
  ┌──────────────┼──────────────┬──────────────┐
  ▼              ▼              ▼              ▼
[PostgreSQL]  [Qdrant]      [Gemini API]  [File Storage]
(Relational)  (Vector RAG)  (LLM Gen)     (Static Assets)
```

## Architectural Characteristics
- **Bounded Domains**: Each domain (`auth`, `users`, `curriculum`, `learners`, `activities`, `analytics`) owns its data models, schemas, and services.
- **Dependency Injection**: FastAPI's `Depends` pattern injects database sessions, services, and current user contexts cleanly without global state.
- **Asynchronous I/O**: Fully async pipeline utilizing `SQLAlchemy 2.0` async engine + `asyncpg` driver for maximum throughput under concurrent learner sessions.
- **Pluggable AI Boundary**: AI orchestrator decoupled behind abstract `LLMProvider` contracts.
