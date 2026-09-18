# Eduvia — Development Guide

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12+ | Backend runtime |
| Node.js | 20+ | Frontend toolchain |
| Docker | 25+ | Container runtime |
| Docker Compose | v2+ | Multi-service orchestration |
| Git | 2.40+ | Version control |

---

## Quick Start

```bash
# 1. Clone the repository
git clone <repo-url> eduvia
cd eduvia

# 2. Set up environment variables
cp .env.example .env
# Edit .env — fill in GEMINI_API_KEY, POSTGRES_PASSWORD, JWT_SECRET at minimum

# 3. Start all services
docker compose up

# 4. Verify connectivity
curl http://localhost:8000/api/v1/health
# Should return: {"status": "ok", "service": "eduvia-api", "version": "0.1.0"}
```

---

## Backend Development

### Setup without Docker

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Unix/macOS

# Install all dependencies including dev tools
pip install -e ".[dev]"

# Create .env from example and configure
cp ../.env.example .env

# Start development server (hot reload)
uvicorn app.main:app --reload --port 8000
```

### Running Tests

```bash
cd backend
pytest                              # All tests
pytest tests/test_health.py -v     # Specific file
pytest -k "test_health" -v         # By keyword
pytest --cov=app --cov-report=html # Coverage report
```

### Code Quality

```bash
# Lint and format check
ruff check app/ tests/
ruff format app/ tests/

# Type checking
mypy app/

# Fix auto-fixable issues
ruff check --fix app/ tests/
ruff format app/ tests/
```

### Database Migrations

```bash
cd backend

# Run pending migrations
alembic upgrade head

# Create a new migration (after adding/changing models)
alembic revision --autogenerate -m "add_user_table"

# Rollback one step
alembic downgrade -1

# Check current state
alembic current
alembic history
```

---

## Frontend Development

### Setup without Docker

```bash
cd frontend

# Install dependencies
npm install

# Create local .env
cp .env.example .env.local

# Start development server
npm run dev
# Frontend: http://localhost:5173
```

### Available Scripts

```bash
npm run dev          # Start Vite dev server
npm run build        # Production build
npm run preview      # Preview production build
npm run lint         # ESLint check
npm run type-check   # TypeScript check
npm run test         # Run Vitest tests
```

### Adding shadcn/ui Components

```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add dialog
# ... etc
```

---

## Docker Compose Services

| Service | Container | Port | Purpose |
|---------|-----------|------|---------|
| frontend | eduvia-frontend | 5173 | Vite dev server |
| backend | eduvia-backend | 8000 | FastAPI + Uvicorn |
| postgres | eduvia-postgres | 5432 | Primary database |
| qdrant | eduvia-qdrant | 6333 | Vector database |

### Useful Docker Commands

```bash
# Start all services
docker compose up

# Start in background
docker compose up -d

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Restart single service
docker compose restart backend

# Stop all services
docker compose down

# Stop and remove volumes (reset data)
docker compose down -v

# Rebuild after code changes
docker compose build backend
```

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `POSTGRES_USER` | Yes | PostgreSQL username |
| `POSTGRES_PASSWORD` | Yes | PostgreSQL password |
| `POSTGRES_DB` | Yes | PostgreSQL database name |
| `QDRANT_URL` | No | Qdrant URL (default: localhost:6333) |
| `QDRANT_API_KEY` | No | Qdrant API key (empty for local) |
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `GEMINI_MODEL` | No | Gemini model name |
| `JWT_SECRET` | Yes | JWT signing secret (min 32 chars) |
| `JWT_ALGORITHM` | No | JWT algorithm (default: HS256) |
| `APP_ENV` | No | Environment (development/production) |
| `APP_DEBUG` | No | Enable debug logging |
| `CORS_ORIGINS_RAW` | No | Comma-separated allowed origins |
| `VITE_API_BASE_URL` | No | Backend URL for frontend |

---

## Project Structure Reference

```
eduvia/
├── frontend/
│   ├── src/
│   │   ├── app/           App shell + routing
│   │   ├── components/    Shared components
│   │   ├── features/      Feature modules (auth, learners, etc.)
│   │   ├── hooks/         Custom React hooks
│   │   ├── services/      API client
│   │   ├── types/         TypeScript types
│   │   └── utils/         Utilities
│   ├── Dockerfile
│   ├── vite.config.ts
│   └── tailwind.config.ts
│
├── backend/
│   ├── app/
│   │   ├── api/v1/        REST endpoints
│   │   ├── core/          Config, logging, errors
│   │   ├── database/      SQLAlchemy + migrations
│   │   ├── ai/            AI orchestrator + providers
│   │   ├── knowledge/     Qdrant client
│   │   └── [modules]/     Feature modules
│   ├── alembic/           Database migrations
│   ├── tests/             pytest tests
│   ├── Dockerfile
│   └── pyproject.toml
│
├── knowledge_base/        Educational knowledge documents
├── docs/                  Documentation
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Code Conventions

### Python
- Type hints on all functions and class attributes
- Docstrings on all public classes and functions
- Pydantic for all API schemas
- structlog for all logging (never `print()`)
- Dependencies injected via FastAPI `Depends()`
- Never call AI providers directly — use `AIOrchestrator`

### TypeScript/React
- Strict TypeScript — no `any` types
- Named exports for components
- Custom hooks for all data fetching
- API calls only through `src/services/api.ts`
- Accessibility attributes on all interactive elements
- Semantic HTML elements

### Git Conventions
- Branch naming: `phase-{N}/{feature-name}`
- Commit format: `feat|fix|docs|refactor|test: description`
- PR required for all changes to main
- Tests must pass before merge

---

## Adding a New Feature (Backend)

1. Create feature directory: `backend/app/{feature_name}/`
2. Create `models.py` — SQLAlchemy ORM models
3. Create `schemas.py` — Pydantic request/response schemas
4. Create `service.py` — Business logic
5. Create `router.py` — FastAPI endpoint handlers
6. Register router in `backend/app/api/v1/router.py`
7. Import models in `backend/alembic/env.py`
8. Run `alembic revision --autogenerate -m "add_{feature_name}"`
9. Write tests in `backend/tests/test_{feature_name}.py`

---

## Troubleshooting

### Backend won't start
- Check `DATABASE_URL` is set correctly in `.env`
- Verify PostgreSQL is running: `docker compose ps postgres`
- Check logs: `docker compose logs backend`

### Frontend can't reach backend
- Verify backend is healthy: `curl http://localhost:8000/api/v1/health`
- Check CORS settings in `.env` include frontend URL
- Verify `VITE_API_BASE_URL` in frontend `.env`

### Alembic migration fails
- Ensure `DATABASE_URL` is set in environment
- Check that all models are imported in `alembic/env.py`
- Run `alembic current` to see current migration state

### Gemini API errors
- Verify `GEMINI_API_KEY` is a real API key (not placeholder)
- Check `ai_provider.configured` in `/api/v1/health/detailed`
- AI features are optional — other features work without Gemini
