# Eduvia MCP Server

Developer Model Context Protocol (MCP) server providing focused repository inspection and verification tools for Eduvia without repeated full-codebase scans.

## Transport Modes

The server supports dual transports using the official MCP Python SDK v2 (`mcp==2.2.0`):

1. **Local Stdio Transport** (default): For local IDEs, Antigravity CLI, or Codex agents over standard input/output pipes.
2. **Remote Streamable HTTP Transport**: For remote cloud hosting (Google Cloud Run) on `0.0.0.0:${PORT}` exposing `/mcp` and `/health`.

## Available Tools (11 Allowlisted)

1. `project_context`: Return concise summary of project metadata, architecture, locked phases, and boundaries.
2. `search_project`: Search text files across the repository for a query string, ignoring build/dependency folders.
3. `read_project_file`: Read file content from within the repository with line numbers (protected against traversal and secrets).
4. `list_project_files`: List files and directories in a given project folder, ignoring dependency and build directories.
5. `git_status`: Return repository and develop branch status information.
6. `git_diff`: Return bounded Git diff information without modifying Git state.
7. `run_backend_tests`: Run backend pytest regression suite (`pytest backend/tests/ -q`) with in-process concurrency protection.
8. `run_frontend_tests`: Run frontend test suite (`npm test` in `frontend/`) with in-process concurrency protection.
9. `run_typecheck`: Run frontend TypeScript check (`npm run type-check` in `frontend/`) with in-process concurrency protection.
10. `run_build`: Run frontend production build (`npm run build` in `frontend/`) with in-process concurrency protection.
11. `verify_project`: Sequentially run backend tests, frontend tests, type-check, and build, returning complete verification result.

## Setup Instructions

### 1. Local Stdio Configuration

In your MCP host configuration (`~/.gemini/config/mcp_config.json` or `.agents/mcp_config.json`):

```json
{
  "mcpServers": {
    "eduvia-local": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "tools/eduvia_mcp",
        "python",
        "-m",
        "eduvia_mcp"
      ]
    }
  }
}
```

### 2. Remote Streamable HTTP Configuration

When deployed to Google Cloud Run, configure your remote MCP client with:

```json
{
  "mcpServers": {
    "eduvia-remote": {
      "serverUrl": "https://<YOUR-CLOUD-RUN-URL>/mcp"
    }
  }
}
```

* **MCP Endpoint**: `POST /mcp` (Streamable HTTP, `text/event-stream` responses).
* **Health Endpoint**: `GET /health` (returns `{"status": "ok", "service": "eduvia-mcp"}`).
* **Port Binding**: Binds dynamically to `0.0.0.0:${PORT:-8080}`.
* **Authentication**: Optional Bearer token authentication via `EDUVIA_MCP_AUTH_TOKEN` environment variable.

## Security Model

* **Zero Shell Execution**: No generic shell execution tools. All commands (`pytest`, `npm test`, `npm run build`) are hard-coded with bounded timeouts.
* **Path Traversal Guards**: Every filesystem path is strictly resolved within `EDUVIA_ROOT`. Traversal attempts (`..`) or external paths are rejected.
* **Secret Protection**: `.env*`, `*.pem`, `*.key`, `secrets*`, `credentials*`, and `service-account*` files are strictly protected from inspection.
* **Concurrency Protection**: Thread locks prevent simultaneous heavy test/build executions to guard against resource exhaustion.

## Testing

Run the MCP test suite from the repository root:

```powershell
.\tools\eduvia_mcp\.venv\Scripts\python.exe -m pytest tools/eduvia_mcp/tests/ -v
```
