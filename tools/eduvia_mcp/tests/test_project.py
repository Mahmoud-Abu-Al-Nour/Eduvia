"""
Eduvia MCP — Test Suite
Tests path security, sensitive file protection, repository search, read operations,
Git integration, allowlisted command wrappers, and MCP tool registrations.
"""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from eduvia_mcp import project
from eduvia_mcp.server import create_server


# ── Fixtures & Setup ──────────────────────────────────────────────────────────
@pytest.fixture
def repo_root():
    return project.get_project_root()


# ── Path Resolution & Traversal Tests ─────────────────────────────────────────
def test_resolve_project_path_valid(repo_root):
    """Verify that legitimate project paths resolve within repository root."""
    resolved = project.resolve_project_path("backend/app/main.py")
    assert resolved.exists()
    assert resolved.is_file()
    assert resolved.relative_to(repo_root) == Path("backend/app/main.py")


def test_resolve_project_path_traversal_rejected():
    """Verify that relative directory traversal is rejected with PermissionError."""
    with pytest.raises(PermissionError):
        project.resolve_project_path("../outside_root")

    with pytest.raises(PermissionError):
        project.resolve_project_path("backend/../../outside_root")


def test_resolve_project_path_absolute_external_rejected():
    """Verify that absolute paths outside the repo root are rejected."""
    external_path = "C:\\Windows\\System32" if os.name == "nt" else "/etc/passwd"
    with pytest.raises(PermissionError):
        project.resolve_project_path(external_path)


# ── Sensitive Files & Ignored Directories ─────────────────────────────────────
@pytest.mark.parametrize(
    "sensitive_path",
    [
        ".env",
        ".env.production",
        "backend/.env",
        "secrets.json",
        "server.key",
        "cert.pem",
        "service-account.json",
        "credentials.yaml",
    ],
)
def test_sensitive_files_rejected(sensitive_path, repo_root):
    """Verify that sensitive patterns cannot be read or inspected."""
    target = repo_root / sensitive_path
    is_blocked, reason = project.is_sensitive_or_ignored(target)
    assert is_blocked is True
    assert len(reason) > 0


@pytest.mark.parametrize(
    "ignored_dir",
    [
        ".git/config",
        ".venv/pyvenv.cfg",
        "node_modules/react/index.js",
        "backend/__pycache__/cache.pyc",
    ],
)
def test_ignored_directories_blocked(ignored_dir, repo_root):
    """Verify that internal dependency and version control directories are blocked."""
    target = repo_root / ignored_dir
    is_blocked, reason = project.is_sensitive_or_ignored(target)
    assert is_blocked is True
    assert "restricted" in reason.lower() or "environment" in reason.lower()


def test_read_sensitive_file_raises_permission_error():
    """Verify read_project_file_content raises PermissionError on .env files."""
    with pytest.raises(PermissionError):
        project.read_project_file_content(".env")


# ── Search Project ────────────────────────────────────────────────────────────
def test_search_project_finds_known_source():
    """Verify that search finds known identifiers in legitimate project files."""
    res = project.search_project_files(query="FastAPI", max_results=10)
    assert res["query"] == "FastAPI"
    assert len(res["results"]) > 0
    first = res["results"][0]
    assert "path" in first
    assert "line" in first
    assert "text" in first


def test_search_project_respects_max_results():
    """Verify search caps results to the specified max_results."""
    max_res = 3
    res = project.search_project_files(query="import", max_results=max_res)
    assert len(res["results"]) <= max_res
    assert res["truncated"] is True or len(res["results"]) < max_res


def test_search_project_empty_query():
    """Verify empty query returns empty results."""
    res = project.search_project_files(query="")
    assert res["results"] == []


# ── Read Project File ─────────────────────────────────────────────────────────
def test_read_project_file_valid():
    """Verify read_project_file_content returns numbered lines."""
    res = project.read_project_file_content("cloudbuild.yaml", start_line=1, end_line=5)
    assert res["path"] == "cloudbuild.yaml"
    assert res["start_line"] == 1
    assert res["end_line"] == 5
    assert len(res["lines"]) == 5
    assert res["lines"][0].startswith("1: ")


def test_read_project_file_nonexistent():
    """Verify read_project_file_content raises FileNotFoundError for nonexistent paths."""
    with pytest.raises(FileNotFoundError):
        project.read_project_file_content("nonexistent_file_xyz.txt")


def test_read_project_file_directory():
    """Verify read_project_file_content raises IsADirectoryError when targeting a directory."""
    with pytest.raises(IsADirectoryError):
        project.read_project_file_content("backend")


# ── List Project Files ────────────────────────────────────────────────────────
def test_list_project_files_root():
    """Verify list_project_files_entries returns root entries without ignored directories."""
    res = project.list_project_files_entries("", max_results=50)
    assert res["base_path"] == "."
    assert len(res["entries"]) > 0
    paths = [e["path"] for e in res["entries"]]
    assert not any(p == ".git" or p.startswith(".git/") or p.startswith(".git\\") for p in paths)
    assert not any(p == "node_modules" or p.startswith("node_modules/") for p in paths)


# ── Git Operations ────────────────────────────────────────────────────────────
def test_git_status_returns_valid_structure():
    """Verify git_status_info returns branch, head, and status."""
    status = project.get_git_status_info()
    assert "branch" in status
    assert "head" in status
    assert "is_clean" in status
    assert isinstance(status["is_clean"], bool)


def test_git_diff_returns_bounded_output():
    """Verify git_diff_info returns diff structure."""
    diff = project.get_git_diff_info(staged=False)
    assert "staged" in diff
    assert "diff" in diff
    assert isinstance(diff["diff"], str)


# ── Project Context ───────────────────────────────────────────────────────────
def test_get_project_context():
    """Verify get_project_context returns accurate metadata."""
    ctx = project.get_project_context()
    assert ctx["project"] == "Eduvia"
    assert len(ctx["locked_phases"]) >= 13
    assert "Phase 12" in ctx["locked_phases"][-1]
    assert "backend" in ctx["architecture"]
    assert "frontend" in ctx["architecture"]
    assert len(ctx["key_boundaries"]) > 0


# ── Allowlisted Command Wrappers (Mocked) ─────────────────────────────────────
@patch("subprocess.run")
def test_run_backend_tests_mocked(mock_run):
    """Verify run_backend_tests_suite properly delegates to allowlisted command."""
    mock_run.return_value = MagicMock(returncode=0, stdout="217 passed", stderr="")
    result = project.run_backend_tests_suite()

    assert result["success"] is True
    assert result["exit_code"] == 0
    assert "217 passed" in result["stdout"]
    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args
    cmd = args[0]
    assert "pytest" in cmd
    assert "backend/tests/" in cmd


@patch("subprocess.run")
def test_run_frontend_tests_mocked(mock_run):
    """Verify run_frontend_tests_suite runs npm test."""
    mock_run.return_value = MagicMock(returncode=0, stdout="13 pass", stderr="")
    result = project.run_frontend_tests_suite()

    assert result["success"] is True
    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args
    assert "test" in args[0]


@patch("subprocess.run")
def test_run_typecheck_mocked(mock_run):
    """Verify run_typecheck_suite runs npm run type-check."""
    mock_run.return_value = MagicMock(returncode=0, stdout="0 errors", stderr="")
    result = project.run_typecheck_suite()

    assert result["success"] is True
    args, kwargs = mock_run.call_args
    assert "type-check" in args[0]


@patch("subprocess.run")
def test_run_build_mocked(mock_run):
    """Verify run_build_suite runs npm run build."""
    mock_run.return_value = MagicMock(returncode=0, stdout="built in 6.69s", stderr="")
    result = project.run_build_suite()

    assert result["success"] is True
    args, kwargs = mock_run.call_args
    assert "build" in args[0]


@patch("eduvia_mcp.project._run_command")
def test_verify_project_suite_mocked(mock_run):
    """Verify verify_project_suite chains all 4 checks."""
    mock_run.return_value = {"success": True, "exit_code": 0, "stdout": "ok", "stderr": "", "duration_seconds": 1.0}

    res = project.verify_project_suite()
    assert res["all_passed"] is True
    assert "backend_tests" in res
    assert "frontend_tests" in res
    assert "typecheck" in res
    assert "build" in res


# ── MCPServer Registration & Tool List ────────────────────────────────────────
def test_all_11_tools_registered():
    """Verify that all 11 required MCP tools are registered with proper names."""
    import asyncio
    server = create_server()
    tools = asyncio.run(server.list_tools())
    tool_names = {t.name for t in tools}

    expected_tools = {
        "project_context",
        "search_project",
        "read_project_file",
        "list_project_files",
        "git_status",
        "git_diff",
        "run_backend_tests",
        "run_frontend_tests",
        "run_typecheck",
        "run_build",
        "verify_project",
    }
    assert expected_tools == tool_names


# ── Remote Streamable HTTP & Health Endpoint Tests ────────────────────────────
def test_remote_health_endpoint():
    """Verify unauthenticated GET /health returns 200 with service status."""
    from starlette.testclient import TestClient
    from eduvia_mcp.server import create_streamable_http_app

    app = create_streamable_http_app()
    with TestClient(app) as client:
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("status") == "ok"
        assert data.get("service") == "eduvia-mcp"


def test_remote_streamable_http_initialize():
    """Verify POST /mcp initializes successfully over Streamable HTTP."""
    from starlette.testclient import TestClient
    from eduvia_mcp.server import create_streamable_http_app

    app = create_streamable_http_app()
    with TestClient(app) as client:
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-remote-client", "version": "1.0.0"},
            },
        }
        resp = client.post("/mcp", json=init_payload)
        assert resp.status_code == 200
        assert "text/event-stream" in resp.headers.get("content-type", "")
        assert "serverInfo" in resp.text
        assert "eduvia" in resp.text


def test_remote_auth_middleware():
    """Verify optional Bearer token authentication behavior on /mcp and /health."""
    from starlette.testclient import TestClient
    from eduvia_mcp.server import create_streamable_http_app

    app = create_streamable_http_app()
    os.environ["EDUVIA_MCP_AUTH_TOKEN"] = "eval-token-123"

    try:
        with TestClient(app) as client:
            # Health check must remain public
            health_resp = client.get("/health")
            assert health_resp.status_code == 200

            # Unauthenticated request to /mcp rejected with 401
            unauth_resp = client.post("/mcp")
            assert unauth_resp.status_code == 401

            # Authenticated request to /mcp accepted
            init_payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test-remote-client", "version": "1.0.0"},
                },
            }
            auth_resp = client.post(
                "/mcp",
                headers={"Authorization": "Bearer eval-token-123"},
                json=init_payload,
            )
            assert auth_resp.status_code == 200
    finally:
        os.environ.pop("EDUVIA_MCP_AUTH_TOKEN", None)

