"""
Eduvia MCP — Server Setup & Dual-Transport Entrypoint
Provides:
  - Local stdio transport (default or when invoked in CLI)
  - Remote Streamable HTTP transport on /mcp with Cloud Run compatibility on 0.0.0.0:${PORT}
  - Unauthenticated health check on /health
  - Optional Bearer token authentication via EDUVIA_MCP_AUTH_TOKEN
  - CORS support and DNS rebinding protections configured for remote hosting
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any

from mcp.server.mcpserver import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import uvicorn

from eduvia_mcp.tools import register_tools


class AuthMiddleware(BaseHTTPMiddleware):
    """Optional bearer token authentication for remote HTTP transport."""

    async def dispatch(self, request, call_next):
        if request.url.path == "/health":
            return await call_next(request)

        token = os.environ.get("EDUVIA_MCP_AUTH_TOKEN", "").strip()
        if token:
            auth_header = request.headers.get("Authorization", "")
            if auth_header != f"Bearer {token}":
                return JSONResponse({"error": "Unauthorized"}, status_code=401)
        return await call_next(request)


def create_server() -> MCPServer:
    """Create and configure the Eduvia MCPServer instance with all tools and health route."""
    server = MCPServer("eduvia")

    # Health check route for Cloud Run container probes
    @server.custom_route("/health", methods=["GET"])
    async def health_check(request: Any) -> JSONResponse:
        return JSONResponse({"status": "ok", "service": "eduvia-mcp"})

    register_tools(server)
    return server


def create_streamable_http_app(server: MCPServer | None = None):
    """Build the Starlette ASGI application for Streamable HTTP hosting on /mcp."""
    if server is None:
        server = create_server()

    transport_sec = TransportSecuritySettings(enable_dns_rebinding_protection=False)
    app = server.streamable_http_app(
        streamable_http_path="/mcp",
        transport_security=transport_sec,
    )

    # Add CORS and optional auth middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(AuthMiddleware)

    return app


def run_stdio() -> None:
    """Run MCP server over standard input/output (local developer mode)."""
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    server = create_server()
    server.run(transport="stdio")


def run_streamable_http(host: str = "0.0.0.0", port: int = 8080) -> None:
    """Run MCP server over Streamable HTTP on host:port for Cloud Run deployment."""
    server = create_server()
    app = create_streamable_http_app(server)
    uvicorn.run(app, host=host, port=port, log_level="info")


def main() -> None:
    """Entrypoint supporting both local stdio and remote Streamable HTTP."""
    parser = argparse.ArgumentParser(description="Eduvia MCP Server")
    parser.add_argument(
        "--remote",
        "--http",
        action="store_true",
        help="Run as remote Streamable HTTP server on 0.0.0.0:${PORT:-8080}",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to listen on in remote mode (defaults to $PORT or 8080)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host interface to bind in remote mode (default 0.0.0.0)",
    )

    args, unknown = parser.parse_known_args()

    # Determine transport from CLI flags or environment variables
    env_transport = os.environ.get("EDUVIA_MCP_TRANSPORT", "").lower()
    is_remote = args.remote or env_transport in ("http", "streamable-http", "remote") or ("PORT" in os.environ and not sys.stdin.isatty())

    if is_remote:
        port = args.port or int(os.environ.get("PORT", "8080"))
        run_streamable_http(host=args.host, port=port)
    else:
        run_stdio()


if __name__ == "__main__":
    main()
