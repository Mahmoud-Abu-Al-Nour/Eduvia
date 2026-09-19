# ─────────────────────────────────────────────────────────────────────────────
#  Eduvia MCP — Production Container for Cloud Run (Streamable HTTP)
#  Hosts the remote Eduvia MCP developer server with bundled project snapshot
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim

# Install system dependencies, Node.js 20, and npm for frontend test execution
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast, reliable Python dependency management
COPY --from=ghcr.io/astral-sh/uv:0.12.7 /uv /bin/uv

# Set working directory to project root
WORKDIR /app

# Copy project source tree (excluding secrets and build artifacts via .dockerignore)
COPY backend /app/backend
COPY frontend /app/frontend
COPY knowledge_base /app/knowledge_base
COPY docs /app/docs
COPY tools /app/tools
COPY docker-compose.yml /app/docker-compose.yml
COPY cloudbuild.yaml /app/cloudbuild.yaml
COPY .env.example /app/.env.example
COPY README.md /app/README.md
COPY LICENSE /app/LICENSE
COPY .gitignore /app/.gitignore

# Set up test environment for backend
RUN cd /app/backend \
    && uv venv \
    && uv pip install -e ".[dev]"

# Set up test environment for frontend
RUN cd /app/frontend \
    && npm ci --ignore-scripts || npm install

# Install Eduvia MCP server dependencies
RUN cd /app/tools/eduvia_mcp \
    && uv venv \
    && uv pip install -e .

# Environment settings for Cloud Run and Streamable HTTP
ENV PORT=8080 \
    EDUVIA_ROOT=/app \
    EDUVIA_MCP_TRANSPORT=streamable-http \
    PYTHONUNBUFFERED=1

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f "http://localhost:${PORT:-8080}/health" || exit 1

# Launch MCP in Streamable HTTP remote mode binding to 0.0.0.0:${PORT}
CMD ["uv", "run", "--project", "/app/tools/eduvia_mcp", "python", "-m", "eduvia_mcp", "--remote"]
