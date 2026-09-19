"""
Eduvia MCP — Core Project Operations & Allowlisted Command Execution
Provides secure repository inspection, bounded searches, Git integration,
and fixed test/build validation commands without arbitrary shell access.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


# ── Directory and File Security Constants ─────────────────────────────────────
IGNORED_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".turbo",
    ".next",
    ".cache",
}

SENSITIVE_PREFIXES = ("credentials", "secrets", "service-account")
SENSITIVE_EXTENSIONS = (".pem", ".key")


def get_project_root() -> Path:
    """
    Resolve the Eduvia project root.
    Uses EDUVIA_ROOT environment variable if set; otherwise traverses upwards
    from this file to locate the directory containing both 'backend' and 'frontend'.
    """
    env_root = os.environ.get("EDUVIA_ROOT")
    if env_root:
        candidate = Path(env_root).resolve()
        if candidate.is_dir():
            return candidate

    # Traverse upward from tools/eduvia_mcp/src/eduvia_mcp/project.py
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / "backend").is_dir() and (parent / "frontend").is_dir():
            return parent

    # Fallback to standard 4 levels above tools/eduvia_mcp/src/eduvia_mcp
    return Path(__file__).resolve().parents[4]


def resolve_project_path(rel_path: str = "") -> Path:
    """
    Resolve a path strictly relative to the Eduvia repository root.
    Raises PermissionError on directory traversal attempts or external paths.
    """
    root = get_project_root().resolve()
    clean_path = rel_path.strip().lstrip("/\\") if rel_path else ""
    target = (root / clean_path).resolve()

    try:
        target.relative_to(root)
    except ValueError:
        raise PermissionError(f"Access denied: path '{rel_path}' resolves outside the repository root.")

    return target


def is_sensitive_or_ignored(path: Path) -> tuple[bool, str]:
    """
    Check if a path points to sensitive credentials or ignored dependency directories.
    Returns (is_restricted, reason).
    """
    root = get_project_root().resolve()
    try:
        rel = path.resolve().relative_to(root)
    except ValueError:
        return True, "Path resolves outside repository root."

    for part in rel.parts:
        part_lower = part.lower()
        if part_lower in IGNORED_DIRS:
            return True, f"Directory '{part}' is restricted from MCP inspection."
        if part_lower == ".env" or part_lower.startswith(".env.") or part_lower.startswith(".env"):
            return True, "Environment files (.env*) are strictly protected."
        if any(part_lower.startswith(p) for p in SENSITIVE_PREFIXES):
            return True, f"Restricted sensitive credential pattern matching '{part}'."

    name_lower = rel.name.lower()
    if name_lower.startswith(".env"):
        return True, "Environment files (.env*) are strictly protected."
    if any(name_lower.endswith(ext) for ext in SENSITIVE_EXTENSIONS):
        return True, "Certificate and private key files are strictly protected."
    if any(name_lower.startswith(p) for p in SENSITIVE_PREFIXES):
        return True, "Credentials and secret files are strictly protected."

    return False, ""


# ── Project Context ───────────────────────────────────────────────────────────
def get_project_context() -> dict[str, Any]:
    """
    Return a concise, accurate JSON summary of the Eduvia project state.
    """
    root = get_project_root()
    git_info = get_git_status_info()

    return {
        "project": "Eduvia",
        "root": str(root),
        "current_branch": git_info.get("branch", "unknown"),
        "head_commit": git_info.get("head", "unknown"),
        "locked_phases": [
            "Phase 0 - Project Initialization & Environment Setup",
            "Phase 1 - Core Curriculum & Models",
            "Phase 2 - Vector Retrieval & Ingestion",
            "Phase 3 - Activity Engine & Progression",
            "Phase 4 - Dynamic Adaptation",
            "Phase 5 - Multi-Tier Auth & Role Boundaries",
            "Phase 6 - Analytics & Learner Modeling",
            "Phase 7 - Adaptive Recommendations",
            "Phase 8 - Content Authoring & Ingestion",
            "Phase 9 - Multi-Modal Activity Types",
            "Phase 10 - Teacher Dashboard & Insights",
            "Phase 11 - Hardening & Accessibility Audit",
            "Phase 12 - Production Cloud Deployment & Staging",
        ],
        "architecture": {
            "backend": "FastAPI, PostgreSQL 16 (SQLAlchemy asyncpg), Alembic, Qdrant vector store, Gemini 2.5 Pro",
            "frontend": "React 19, TypeScript, Vite, TailwindCSS, Accessible ARIA WCAG-compliant components",
            "cloud": "Google Cloud Run, Cloud SQL PostgreSQL, Secret Manager, Cloud Build CI/CD, Terraform",
            "tooling": "Eduvia Developer MCP (tools/eduvia_mcp)",
        },
        "key_boundaries": [
            "Eduvia MCP is strictly a local developer tool (never imported into FastAPI or React)",
            "Phases 0 through 12 are complete, verified, and LOCKED",
            "All filesystem access strictly bounded within EDUVIA_ROOT",
            "Zero arbitrary command execution; allowlisted test/build suites only",
        ],
    }


# ── Search & File Operations ──────────────────────────────────────────────────
def search_project_files(query: str, path: str = "", max_results: int = 50) -> dict[str, Any]:
    """
    Search text files across the repository for a query string.
    Bypasses ignored directories and sensitive files.
    """
    if not query:
        return {"query": "", "results": [], "total_matches": 0, "truncated": False}

    root = get_project_root()
    base_dir = resolve_project_path(path)
    if not base_dir.is_dir():
        if base_dir.is_file():
            base_dir = base_dir.parent
        else:
            return {"error": f"Path '{path}' is not a valid directory.", "results": []}

    results: list[dict[str, Any]] = []
    max_res = max(1, min(max_results, 200))
    query_lower = query.lower()

    for root_dir, dir_names, file_names in os.walk(base_dir):
        # Prune ignored and sensitive directories in-place
        dir_names[:] = [
            d for d in dir_names
            if d.lower() not in IGNORED_DIRS
            and not d.lower().startswith(".env")
            and not any(d.lower().startswith(p) for p in SENSITIVE_PREFIXES)
        ]

        for fname in file_names:
            file_path = Path(root_dir) / fname
            is_blocked, _ = is_sensitive_or_ignored(file_path)
            if is_blocked:
                continue

            # Skip files larger than 2MB
            try:
                if file_path.stat().st_size > 2 * 1024 * 1024:
                    continue
            except OSError:
                continue

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, start=1):
                        if query_lower in line.lower():
                            rel_file = str(file_path.relative_to(root)).replace("\\", "/")
                            results.append({
                                "path": rel_file,
                                "line": line_num,
                                "text": line.strip()[:200],
                            })
                            if len(results) >= max_res:
                                return {
                                    "query": query,
                                    "results": results,
                                    "total_matches": len(results),
                                    "truncated": True,
                                }
            except (OSError, UnicodeError):
                continue

    return {
        "query": query,
        "results": results,
        "total_matches": len(results),
        "truncated": False,
    }


def read_project_file_content(
    path: str,
    start_line: int | None = None,
    end_line: int | None = None,
) -> dict[str, Any]:
    """
    Read content from a project file with line numbering.
    Protects against path traversal, sensitive files, and excessively large files.
    """
    target = resolve_project_path(path)
    root = get_project_root()

    if not target.exists():
        raise FileNotFoundError(f"File '{path}' does not exist.")
    if not target.is_file():
        raise IsADirectoryError(f"Path '{path}' is a directory, not a file.")

    is_blocked, reason = is_sensitive_or_ignored(target)
    if is_blocked:
        raise PermissionError(f"Access denied: {reason}")

    # Maximum file size 1MB
    if target.stat().st_size > 1024 * 1024:
        raise ValueError("File exceeds maximum allowed size (1 MB).")

    try:
        content = target.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        raise OSError(f"Failed to read file '{path}': {exc}")

    lines = content.splitlines()
    total_lines = len(lines)

    start = max(1, start_line) if start_line is not None else 1
    end = min(total_lines, end_line) if end_line is not None else total_lines

    # Bound window if unboundedly large
    if end_line is None and total_lines > 500:
        end = min(total_lines, start + 499)

    numbered_lines = [
        f"{idx}: {lines[idx - 1]}"
        for idx in range(start, end + 1)
    ]

    rel_path = str(target.relative_to(root)).replace("\\", "/")
    return {
        "path": rel_path,
        "total_lines": total_lines,
        "start_line": start,
        "end_line": end,
        "lines": numbered_lines,
    }


def list_project_files_entries(
    path: str = "",
    max_results: int = 100,
) -> dict[str, Any]:
    """
    List files and directories within a given project folder.
    Skips ignored dependency directories and sensitive files.
    """
    target = resolve_project_path(path)
    root = get_project_root()

    if not target.exists():
        raise FileNotFoundError(f"Path '{path}' does not exist.")
    if not target.is_dir():
        raise NotADirectoryError(f"Path '{path}' is not a directory.")

    is_blocked, reason = is_sensitive_or_ignored(target)
    if is_blocked:
        raise PermissionError(f"Access denied: {reason}")

    entries: list[dict[str, Any]] = []
    max_res = max(1, min(max_results, 500))

    try:
        for item in target.iterdir():
            is_item_blocked, _ = is_sensitive_or_ignored(item)
            if is_item_blocked:
                continue

            rel_item = str(item.relative_to(root)).replace("\\", "/")
            if item.is_dir():
                entries.append({"path": rel_item, "type": "directory"})
            else:
                try:
                    size = item.stat().st_size
                except OSError:
                    size = 0
                entries.append({"path": rel_item, "type": "file", "size_bytes": size})

            if len(entries) >= max_res:
                break
    except OSError as exc:
        raise OSError(f"Failed to list directory '{path}': {exc}")

    rel_base = str(target.relative_to(root)).replace("\\", "/") if target != root else "."
    return {
        "base_path": rel_base,
        "total_entries": len(entries),
        "truncated": len(entries) >= max_res,
        "entries": entries,
    }


# ── Git Integration (Read-Only) ───────────────────────────────────────────────
def get_git_status_info() -> dict[str, Any]:
    """
    Return read-only Git status including current branch, HEAD commit, upstream, and short status.
    """
    root = get_project_root()
    git_bin = shutil.which("git") or "git"

    try:
        branch_proc = subprocess.run(
            [git_bin, "branch", "--show-current"],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=5,
        )
        branch = branch_proc.stdout.strip() or "HEAD detached"

        head_proc = subprocess.run(
            [git_bin, "rev-parse", "HEAD"],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=5,
        )
        head = head_proc.stdout.strip()[:7] if head_proc.returncode == 0 else "unknown"

        upstream_proc = subprocess.run(
            [git_bin, "rev-parse", "--abbrev-ref", "@{upstream}"],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=5,
        )
        upstream = upstream_proc.stdout.strip() if upstream_proc.returncode == 0 else None

        status_proc = subprocess.run(
            [git_bin, "status", "--short"],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=5,
        )
        short_status = status_proc.stdout.strip()
        is_clean = len(short_status) == 0

        return {
            "branch": branch,
            "head": head,
            "upstream": upstream,
            "short_status": short_status,
            "is_clean": is_clean,
        }
    except Exception as exc:
        return {
            "branch": "unknown",
            "head": "unknown",
            "upstream": None,
            "short_status": f"git unavailable: {exc}",
            "is_clean": False,
        }


def get_git_diff_info(path: str = "", staged: bool = False) -> dict[str, Any]:
    """
    Return bounded git diff information without modifying git state.
    """
    root = get_project_root()
    git_bin = shutil.which("git") or "git"

    args = [git_bin, "diff"]
    if staged:
        args.append("--cached")

    if path:
        target = resolve_project_path(path)
        rel_path = str(target.relative_to(root)).replace("\\", "/")
        args.extend(["--", rel_path])

    try:
        diff_proc = subprocess.run(
            args,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=10,
        )
        diff_output = diff_proc.stdout
        max_chars = 30000
        truncated = len(diff_output) > max_chars

        return {
            "staged": staged,
            "path": path or "repository_root",
            "diff": diff_output[:max_chars],
            "truncated": truncated,
        }
    except Exception as exc:
        return {
            "staged": staged,
            "path": path,
            "diff": f"git diff failed: {exc}",
            "truncated": False,
        }


# ── Allowlisted Test and Build Execution ──────────────────────────────────────
def _run_command(cmd: list[str], cwd: Path, timeout: float) -> dict[str, Any]:
    """
    Execute an internal allowlisted command with standard timing and capture.
    """
    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        duration = round(time.time() - start, 2)
        return {
            "success": proc.returncode == 0,
            "exit_code": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "duration_seconds": duration,
        }
    except subprocess.TimeoutExpired as exc:
        duration = round(time.time() - start, 2)
        return {
            "success": False,
            "exit_code": -1,
            "stdout": (exc.stdout or "").strip() if isinstance(exc.stdout, str) else "",
            "stderr": f"Command timed out after {timeout} seconds",
            "duration_seconds": duration,
        }
    except Exception as exc:
        duration = round(time.time() - start, 2)
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": str(exc),
            "duration_seconds": duration,
        }


def run_backend_tests_suite() -> dict[str, Any]:
    """
    Execute backend test suite: pytest backend/tests/ -q
    """
    root = get_project_root()
    if sys.platform == "win32":
        py_bin = root / "backend" / ".venv" / "Scripts" / "python.exe"
    else:
        py_bin = root / "backend" / ".venv" / "bin" / "python"

    if not py_bin.exists():
        return {
            "success": False,
            "exit_code": 1,
            "stdout": "",
            "stderr": f"Backend python virtual environment not found at {py_bin}",
            "duration_seconds": 0.0,
        }

    cmd = [str(py_bin), "-m", "pytest", "backend/tests/", "-q"]
    return _run_command(cmd, cwd=root, timeout=120.0)


def run_frontend_tests_suite() -> dict[str, Any]:
    """
    Execute frontend tests: npm test (from frontend/)
    """
    root = get_project_root()
    frontend_dir = root / "frontend"
    npm_bin = shutil.which("npm") or "npm"

    return _run_command([npm_bin, "test"], cwd=frontend_dir, timeout=60.0)


def run_typecheck_suite() -> dict[str, Any]:
    """
    Execute frontend typecheck: npm run type-check (from frontend/)
    """
    root = get_project_root()
    frontend_dir = root / "frontend"
    npm_bin = shutil.which("npm") or "npm"

    return _run_command([npm_bin, "run", "type-check"], cwd=frontend_dir, timeout=60.0)


def run_build_suite() -> dict[str, Any]:
    """
    Execute frontend production build: npm run build (from frontend/)
    """
    root = get_project_root()
    frontend_dir = root / "frontend"
    npm_bin = shutil.which("npm") or "npm"

    return _run_command([npm_bin, "run", "build"], cwd=frontend_dir, timeout=90.0)


def verify_project_suite() -> dict[str, Any]:
    """
    Sequentially run backend tests, frontend tests, type-check, and build.
    Preserves detailed step outputs and indicates overall status.
    """
    backend_res = run_backend_tests_suite()
    frontend_res = run_frontend_tests_suite()
    typecheck_res = run_typecheck_suite()
    build_res = run_build_suite()

    all_passed = (
        backend_res["success"]
        and frontend_res["success"]
        and typecheck_res["success"]
        and build_res["success"]
    )

    return {
        "all_passed": all_passed,
        "backend_tests": backend_res,
        "frontend_tests": frontend_res,
        "typecheck": typecheck_res,
        "build": build_res,
    }
