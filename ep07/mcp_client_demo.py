"""
Episode 7: MCP Client Demo
    — Connecting to an MCP Server

Shows how an MCP client connects to a
server, discovers tools, and calls them.

Usage:
  python mcp_client_demo.py

This script launches mcp_weather_server.py
as a subprocess and communicates via stdio.

Author: Terry kim <goandonh@gmail.com>
Co-Author: Claudie

Series: Claudie's Agentic AI Classroom
Blog: https://ai-girls.org
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # ── 1. Define server to connect to ─
    server_path = str(
        Path(__file__).parent
        / "mcp_weather_server.py"
    )

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_path],
    )

    # ── 2. Connect to the server ───────
    print("Connecting to MCP server...")
    async with stdio_client(
        server_params
    ) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize handshake
            await session.initialize()
            print("Connected!\n")

            # ── 3. Discover tools ──────
            tools = await session.list_tools()
            print(
                f"Found {len(tools.tools)}"
                f" tools:"
            )
            for tool in tools.tools:
                print(
                    f"  - {tool.name}: "
                    f"{tool.description}"
                )
            print()

            # ── 4. Call tools ──────────
            # Call get_weather
            result = await session.call_tool(
                "get_weather",
                {"city": "Seoul"}
            )
            print(
                "[get_weather] "
                f"{result.content[0].text}"
            )

            result = await session.call_tool(
                "get_weather",
                {"city": "Tokyo"}
            )
            print(
                "[get_weather] "
                f"{result.content[0].text}"
            )

            # Call get_greeting
            result = await session.call_tool(
                "get_greeting",
                {"name": "Claudie",
                 "language": "ko"}
            )
            print(
                "[get_greeting] "
                f"{result.content[0].text}"
            )

            print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
