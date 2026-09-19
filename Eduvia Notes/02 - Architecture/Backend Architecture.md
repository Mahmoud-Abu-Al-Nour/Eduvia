# Backend Architecture

The Eduvia backend (`backend/app/`) follows a clean layered domain structure:

```text
backend/app/
├── core/           # Configuration, logging, global error handlers
├── database/       # Async engine, SessionLocal, base models, init scripts
├── api/v1/         # Central router aggregation & health check endpoints
├── auth/           # OAuth2, JWT generation, password hashing, dependencies
├── users/          # User model (Admin, Teacher), CRUD service, schemas, router
├── curriculum/     # 5-tier curriculum models, schemas, service, router
├── knowledge/      # Qdrant client abstraction & collection management
├── ai/             # AI orchestrator, LLMProvider abstractions, Gemini client
├── learners/       # (Phase 3) Learner profile domain
├── activities/     # (Phase 4) Activity generation schemas
└── analytics/      # (Phase 7) Performance tracking & analytics
```

---

## Key Design Patterns

1. **Async Session Management**:
   ```python
   async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
       async with SessionLocal() as session:
           try:
               yield session
           except Exception:
               await session.rollback()
               raise
   ```
2. **Service Layer Isolation**: Routers handle HTTP validation and response serialization; business logic resides strictly inside domain Services (`UserService`, `CurriculumService`).
3. **Structured JSON Errors**: Exceptions inherit from `EduviaError` and are transformed by custom FastAPI exception handlers into unified JSON errors with explicit error codes.
