# Eduvia Project MCP (Model Context Protocol)

> **Dedicated Developer Tooling & Remote Context Server for AI-Assisted Engineering and Automated Verification**

---

## What is the Model Context Protocol (MCP)?

The **Model Context Protocol (MCP)** is an open industry specification that establishes a standardized, bidirectional interface between AI development assistants (such as Google Antigravity, Claude, or Codex) and external software development environments. 

Rather than requiring an AI agent to blindly scan thousands of files, consume excessive context window tokens, or run unvetted shell commands, an MCP server provides **first-class, typed tools** that expose structured project context, file inspection, and test execution directly to the model.

---

## The Eduvia Project MCP Server

Located in `tools/eduvia_mcp/`, the **Eduvia Project MCP** is a purpose-built, isolated Python package engineered to give AI agents an authoritative, safe window into the Eduvia repository.

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                      AI Client / Agent                      │
 │          (Antigravity IDE • Claude Code • Cursor)           │
 └──────────────────────────────┬──────────────────────────────┘
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼ (Local Transport)                             ▼ (Remote Transport)
┌───────────────────────────────┐       ┌───────────────────────────────┐
│     Standard I/O (`stdio`)    │       │     Streamable HTTP (SSE)     │
│   FastMCP CLI Subprocess IPC  │       │  Starlette + Uvicorn Service  │
└───────────────┬───────────────┘       └───────────────┬───────────────┘
                │                                       │
                └───────────────────┬───────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                             Eduvia MCP Server Core Runtime                                  │
│                 Thread Concurrency Lock (`_EXECUTION_LOCK`) • Sandboxed Paths               │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ 11 Registered Developer Tools:                                                              │
│ • `project_context`     • `search_project`      • `read_project_file` • `list_project_files`│
│ • `git_status`          • `git_diff`            • `run_backend_tests` • `run_frontend_tests`│
│ • `run_typecheck`       • `run_build`           • `verify_project`                          │
└─────────────────────────────────────────────────────┬───────────────────────────────────────┘
                                                      │ Safe Subprocess Calls
                                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                           Eduvia Application Repository Context                             │
│     Backend Pytest (217) • Frontend Vitest (13) • TypeScript Build • Git Repository Logs    │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Registered Tool Inventory

The Eduvia MCP server exposes exactly **11 registered tools** across inspection, context, and test verification:

| Tool Name | Parameters | Functional Description |
| :--- | :--- | :--- |
| `project_context` | *None* | Returns structured metadata: repository name, active branch, latest commit hash, Python version, node version, and phase completion status. |
| `search_project` | `query: str`, `file_pattern: Optional[str]` | High-speed ripgrep/regex search across project source files, respecting `.gitignore` exclusions. |
| `read_project_file`| `relative_path: str`, `start_line: Optional[int]`, `end_line: Optional[int]` | Safely reads file contents within the project root. Rejects path traversal (`../`) attacks. |
| `list_project_files`| `directory: Optional[str]`, `pattern: Optional[str]` | Lists directory contents and file hierarchies relative to the repository root. |
| `git_status` | *None* | Returns current working tree status (`git status --short`), branch tracking, and uncommitted changes. |
| `git_diff` | `cached: bool = False`, `path: Optional[str] = None` | Returns standard unified diffs for staged or unstaged modifications. |
| `run_backend_tests`| `test_path: Optional[str] = None`, `verbose: bool = False` | Executes the backend `pytest` suite in an isolated subprocess using the project virtual environment. |
| `run_frontend_tests`| `filter: Optional[str] = None` | Runs frontend unit and component tests via `npm test` (`vitest run`). |
| `run_typecheck` | *None* | Runs strict TypeScript compiler check (`npm run type-check` $\rightarrow$ `tsc -b`). |
| `run_build` | *None* | Verifies production frontend compilation via `npm run build` (`vite build`). |
| `verify_project` | *None* | Master diagnostic tool: sequentially runs backend tests, frontend tests, type-check, and build, returning an atomic pass/fail summary. |

---

## 2. Dual Transport Architecture

The server supports two distinct operational modes:

### 1. Local Standard I/O (`stdio`)
* Ideal for local pair-programming with AI coding agents running on the same machine.
* Invoked via:
  ```powershell
  python -m eduvia_mcp
  ```
* Communication occurs over standard input/output streams using JSON-RPC 2.0 messages.

### 2. Remote Streamable HTTP (Cloud & Tunnel Ready)
* Enables remote AI assistants and distributed services to connect to the MCP server over HTTP/SSE.
* Invoked via:
  ```powershell
  python -m eduvia_mcp --remote --port 8088
  ```
* Implemented via Starlette and Uvicorn, mounting the FastMCP streamable HTTP transport at `/mcp`.
* Supports cross-origin requests via configurable CORS middleware.

---

## 3. Concurrency Protection & Safety Constraints

To ensure stability during automated AI development cycles:
1. **Thread Execution Locking (`_EXECUTION_LOCK`)**: Running full backend and frontend test suites is computationally expensive. An internal `threading.Lock` serializes execution requests. If multiple agent threads trigger `verify_project` simultaneously, requests queue cleanly rather than exhausting system CPU/memory.
2. **Path Traversal Sandboxing**: The `read_project_file` tool strictly resolves paths against the canonical project root. Any attempt to access files outside the workspace (e.g., `../../Windows/System32` or user home folders) raises an immediate security exception.
3. **Read-Only / Test-Only Boundaries**: The MCP server is strictly an inspection and verification utility. It exposes no file modification, git commit, or git push tools, ensuring the human developer and AI assistant maintain explicit control over file writes.

---

## 4. Verification & Testing of the MCP Server

The MCP server package maintains its own independent test suite under `tools/eduvia_mcp/tests/test_project.py`:
* **35 automated tests passing** (100% pass rate).
* Tests cover parameter validation, tool discovery, output formatting, git command parsers, path sandboxing, and subprocess failure handling.
* Verified under both local `stdio` loopback and remote `Streamable HTTP` network invocations.

---

## Related Documentation

* Master Overview: [[Eduvia Project Overview & Technical Abstract|Eduvia Project Overview & Technical Abstract]]
* System Architecture: [[Eduvia Architecture & System Design|Eduvia Architecture & System Design]]
* Testing & Verification: [[Eduvia Testing & Verification|Eduvia Testing & Verification]]
* Cloud Deployment: [[Eduvia Production & Cloud Deployment|Eduvia Production & Cloud Deployment]]
* MCP README: `tools/eduvia_mcp/README.md`
