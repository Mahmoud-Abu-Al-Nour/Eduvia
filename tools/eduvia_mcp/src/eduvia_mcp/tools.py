"""
Eduvia MCP — Tool Registrations
Registers the 11 allowlisted MCP developer tools on the MCPServer instance.
"""

from __future__ import annotations

from typing import Any, Optional
from mcp.server.mcpserver import MCPServer

from eduvia_mcp import project


def register_tools(server: MCPServer) -> None:
    """Register all 11 allowlisted Eduvia inspection and verification tools."""

    @server.tool(
        name="project_context",
        description="Return concise summary of project metadata, architecture, locked phases, and boundaries.",
    )
    def project_context() -> dict[str, Any]:
        return project.get_project_context()

    @server.tool(
        name="search_project",
        description="Search text files across the repository for a query string, ignoring build/dependency folders.",
    )
    def search_project(
        query: str,
        path: Optional[str] = "",
        max_results: Optional[int] = 50,
    ) -> dict[str, Any]:
        return project.search_project_files(
            query=query,
            path=path or "",
            max_results=max_results if max_results is not None else 50,
        )

    @server.tool(
        name="read_project_file",
        description="Read file content from within the repository with line numbers. Protected against path traversal and secrets.",
    )
    def read_project_file(
        path: str,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
    ) -> dict[str, Any]:
        return project.read_project_file_content(
            path=path,
            start_line=start_line,
            end_line=end_line,
        )

    @server.tool(
        name="list_project_files",
        description="List files and directories in a given project folder, ignoring node_modules, .venv, and build outputs.",
    )
    def list_project_files(
        path: Optional[str] = "",
        max_results: Optional[int] = 100,
    ) -> dict[str, Any]:
        return project.list_project_files_entries(
            path=path or "",
            max_results=max_results if max_results is not None else 100,
        )

    @server.tool(
        name="git_status",
        description="Return read-only Git status including current branch, HEAD commit, upstream, and short status.",
    )
    def git_status() -> dict[str, Any]:
        return project.get_git_status_info()

    @server.tool(
        name="git_diff",
        description="Return bounded Git diff information without modifying Git state.",
    )
    def git_diff(
        path: Optional[str] = "",
        staged: Optional[bool] = False,
    ) -> dict[str, Any]:
        return project.get_git_diff_info(
            path=path or "",
            staged=bool(staged),
        )

    @server.tool(
        name="run_backend_tests",
        description="Run backend pytest regression suite (pytest backend/tests/ -q) and return structured execution result.",
    )
    def run_backend_tests() -> dict[str, Any]:
        return project.run_backend_tests_suite()

    @server.tool(
        name="run_frontend_tests",
        description="Run frontend test suite (npm test in frontend/) and return structured execution result.",
    )
    def run_frontend_tests() -> dict[str, Any]:
        return project.run_frontend_tests_suite()

    @server.tool(
        name="run_typecheck",
        description="Run frontend TypeScript check (npm run type-check in frontend/) and return structured execution result.",
    )
    def run_typecheck() -> dict[str, Any]:
        return project.run_typecheck_suite()

    @server.tool(
        name="run_build",
        description="Run frontend production build (npm run build in frontend/) and return structured execution result.",
    )
    def run_build() -> dict[str, Any]:
        return project.run_build_suite()

    @server.tool(
        name="verify_project",
        description="Run sequentially backend tests, frontend tests, type-check, and build, returning complete verification result.",
    )
    def verify_project() -> dict[str, Any]:
        return project.verify_project_suite()
