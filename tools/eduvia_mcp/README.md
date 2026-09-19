# Eduvia MCP Server

Local developer Model Context Protocol (MCP) server providing focused repository inspection and verification tools for Eduvia without scanning the whole codebase.

## Features

* **Strict Path Security**: All filesystem operations are strictly resolved within `EDUVIA_ROOT` with path traversal protections. Sensitive credentials (`.env*`, `*.pem`, `*.key`, `secrets*`, `credentials*`, `service-account*`) and internal build/dependency directories (`node_modules`, `.venv`, `.git`, `dist`, `build`, `__pycache__`) are blocked from inspection.
* **Bounded Searches & Reads**: Text search and file inspection with line-numbering, capped outputs, and size checks.
* **Read-Only Git Integration**: Non-mutating `git_status` and `git_diff` queries.
* **Allowlisted Test & Verification Commands**: Hardcoded, fixed command execution for test regression, type-checking, and frontend builds without generic shell access.

## Available Tools

1. `project_context`: Return concise summary of project metadata, architecture, locked phases, and boundaries.
2. `search_project`: Search text files across the repository for a query string, ignoring build/dependency folders.
3. `read_project_file`: Read file content from within the repository with line numbers (protected against traversal and secrets).
4. `list_project_files`: List files and directories in a given project folder, ignoring dependency and build directories.
5. `git_status`: Return read-only Git status including current branch, HEAD commit, upstream, and short status.
6. `git_diff`: Return bounded Git diff information without modifying Git state.
7. `run_backend_tests`: Run backend pytest regression suite (`pytest backend/tests/ -q`) and return structured execution result.
8. `run_frontend_tests`: Run frontend test suite (`npm test` in `frontend/`) and return structured execution result.
9. `run_typecheck`: Run frontend TypeScript check (`npm run type-check` in `frontend/`) and return structured execution result.
10. `run_build`: Run frontend production build (`npm run build` in `frontend/`) and return structured execution result.
11. `verify_project`: Sequentially run backend tests, frontend tests, type-check, and build, returning complete verification result.

## Host Configuration

To register the server in your MCP host (e.g. Antigravity, Claude Desktop, or Cursor), refer to `mcp_config.example.json`:

```json
{
  "mcpServers": {
    "eduvia": {
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

The server communicates via standard input/output (`stdio` transport).

## Running Tests

From the repository root:

```powershell
.\tools\eduvia_mcp\.venv\Scripts\python.exe -m pytest tools/eduvia_mcp/tests/ -v
```
