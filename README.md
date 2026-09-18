# Eduvia

> **Standardized Curriculum + Personalized Delivery**

Eduvia is an adaptive educational web platform designed to support learners with intellectual disabilities and special educational needs.

The system helps teachers deliver the **same learning objectives** through **different teaching and activity approaches** based on each learner's observed learning patterns and performance.

## Core Principle

```
Same Curriculum
       ↓
Same Learning Objective
       ↓
Different Delivery Method
       ↓
Track Performance
       ↓
Analyze Learning Pattern
       ↓
Adapt Future Activities
```

Eduvia is **not** a medical diagnostic tool. It is an educational support system.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui, Framer Motion |
| Backend | Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, Uvicorn |
| Database | PostgreSQL (primary), Qdrant (vector / RAG) |
| AI | Gemini API (abstracted via LLM provider interface) |
| Infrastructure | Docker, Docker Compose |

---

## Quick Start (Local Development)

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.12+

### 1. Clone and configure
```bash
git clone <repo-url> eduvia
cd eduvia
cp .env.example .env
# Edit .env and fill in your real values
```

### 2. Start all services
```bash
docker compose up
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |
| Qdrant | http://localhost:6333 |

### 3. Backend development (without Docker)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

### 4. Frontend development (without Docker)
```bash
cd frontend
npm install
npm run dev
```

### 5. Run tests
```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm run test
```

---

## Repository Structure

```
eduvia/
├── frontend/           React + TypeScript + Vite app
├── backend/            FastAPI Python application
├── knowledge_base/     Educational knowledge for RAG
├── infrastructure/     Docker configurations
├── docs/               Architecture + product documentation
├── tests/              Integration tests
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/architecture.md) | System architecture overview |
| [Product Requirements](docs/product-requirements.md) | Full product specification |
| [AI Architecture](docs/ai-architecture.md) | Adaptive intelligence design |
| [Data Model](docs/data-model.md) | Domain model and database schema |
| [API Design](docs/api-design.md) | REST API specification |
| [Accessibility](docs/accessibility.md) | Accessibility requirements |
| [Security](docs/security.md) | Security design |
| [Development Guide](docs/development-guide.md) | Developer onboarding |

---

## Important Notices

- **This system does NOT diagnose medical or psychological conditions.**
- **The AI provides recommendations — teachers remain the decision makers.**
- **Never commit `.env` files with real credentials.**

---

## Current Phase

**Phase 0 — Project Initialization** ✅

See [Architecture](docs/architecture.md) for the full development roadmap.

---

## License

MIT — see [LICENSE](LICENSE)
