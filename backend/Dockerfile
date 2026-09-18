# ─────────────────────────────────────────────────────────────
# Eduvia Backend — Multi-stage Dockerfile
# ─────────────────────────────────────────────────────────────

# ── Stage 1: Base ──────────────────────────────────────────────
FROM python:3.12-slim AS base

# Security: run as non-root user
RUN groupadd --gid 1001 eduvia \
    && useradd --uid 1001 --gid eduvia --shell /bin/bash --create-home eduvia

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ── Stage 2: Dependencies ──────────────────────────────────────
FROM base AS dependencies

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e "."

# ── Stage 3: Development ───────────────────────────────────────
FROM dependencies AS development

# Install dev dependencies
RUN pip install --no-cache-dir -e ".[dev]"

COPY --chown=eduvia:eduvia . .

USER eduvia

EXPOSE 8000

# Development: hot reload with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ── Stage 4: Production ────────────────────────────────────────
FROM dependencies AS production

COPY --chown=eduvia:eduvia . .

USER eduvia

EXPOSE 8000

# Health check for Docker/Kubernetes
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Production: multiple workers
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
