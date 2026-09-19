# Technology Stack

| Layer | Technology | Version | Rationale |
| :--- | :--- | :--- | :--- |
| **Backend Framework** | FastAPI | >= 0.115.0 | Async performance, native OpenAPI generation, Pydantic v2 validation. |
| **Backend Runtime** | Python | >= 3.12 | Modern type hinting (`typing.override`, `match/case`), improved interpreter speed. |
| **Database ORM** | SQLAlchemy (async) | >= 2.0.36 | Robust relational modeling, type-safe queries, `selectinload` optimization. |
| **Database Driver** | asyncpg | >= 0.30.0 | High-performance asynchronous PostgreSQL client library. |
| **Relational Database**| PostgreSQL | 16-alpine | Enterprise ACID compliance, native JSONB support for localization. |
| **Vector Database** | Qdrant | latest | High-speed vector similarity search, robust filtering for RAG knowledge. |
| **AI / LLM** | Google Gemini API | gemini-1.5 | Structured JSON output capability, generous context window, multimodal. |
| **Frontend Framework**| React | 19.x | Modern concurrent rendering, clean component lifecycle. |
| **Frontend Language** | TypeScript | 5.x / 6.x | Strict type safety, shared domain interfaces with backend. |
| **Build Tooling** | Vite | 5.4.x | Fast HMR development server, optimized ES module production bundling. |
| **Styling** | Tailwind CSS | v4 | Utility-first, zero-runtime CSS, modern CSS design tokens. |
| **Linter / Formatter**| Ruff & Oxlint | latest | Blazing fast Rust-based static analysis for Python and TypeScript. |
| **Containerization** | Docker & Compose | v2 | Reproducible multi-service local development and deployment parity. |
