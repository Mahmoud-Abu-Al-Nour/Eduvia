"""
Eduvia MCP — Server Setup & Entrypoint
Provides stdio transport for Antigravity/Codex interaction.
"""

from __future__ import annotations

import sys
from mcp.server.mcpserver import MCPServer
from eduvia_mcp.tools import register_tools


def create_server() -> MCPServer:
    """Create and configure the Eduvia MCPServer instance."""
    server = MCPServer("eduvia")
    register_tools(server)
    return server


def main() -> None:
    """Run the MCP server over standard input/output (stdio transport)."""
    # Ensure Windows console / pipes communicate strictly using UTF-8
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    server = create_server()
    # stdio transport communicates with the host over stdin/stdout
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
