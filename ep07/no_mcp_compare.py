"""
Episode 7: Why MCP? — The Problem It Solves

WITHOUT MCP: Each AI app must write custom
integration code for every service.

  App A ──custom code──▶ Weather API
  App A ──custom code──▶ Database
  App B ──custom code──▶ Weather API (again!)
  App B ──custom code──▶ Database (again!)

WITH MCP: One standard protocol for all.

  App A ──MCP──▶ Weather MCP Server
  App A ──MCP──▶ Database MCP Server
  App B ──MCP──▶ Weather MCP Server (reuse!)
  App B ──MCP──▶ Database MCP Server (reuse!)

This file shows the "old way" — hardcoded
API calls that every app must duplicate.

Author: Terry kim <goandonh@gmail.com>
Co-Author: Claudie

Series: Claudie's Agentic AI Classroom
Blog: https://ai-girls.org
"""

import anthropic
import json

client = anthropic.Anthropic()

# ── The old way: hardcoded tool logic ──
# Every AI app must define its own tools
# AND its own execution logic.
# If you want to reuse this in another
# app, you must copy-paste everything!

tools = [{
    "name": "get_weather",
    "description":
        "Get weather for a city",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name"
            }
        },
        "required": ["city"]
    }
}]

# Hardcoded execution — tightly coupled
# to THIS specific app
WEATHER_DB = {
    "Seoul": "Clear, 18°C",
    "Tokyo": "Cloudy, 22°C",
}


def run_tool(name, args):
    """Each app must implement this."""
    if name == "get_weather":
        city = args["city"]
        return WEATHER_DB.get(
            city, "No data"
        )
    return "Unknown tool"


# ── Run with Claude ────────────────────
messages = [
    {"role": "user",
     "content": "What's the weather "
                "in Seoul?"}
]

resp = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=512,
    tools=tools,
    messages=messages
)

# Handle tool calls manually
for block in resp.content:
    if block.type == "tool_use":
        result = run_tool(
            block.name, block.input
        )
        print(
            f"Tool: {block.name}"
            f"({block.input})"
        )
        print(f"Result: {result}")

# ── The problem ────────────────────────
# 1. Tools are hardcoded in EACH app
# 2. No standard discovery mechanism
# 3. No reuse across different AI apps
# 4. Adding a new service = change code
#    in EVERY app that needs it
#
# MCP solves this with a STANDARD protocol
# → See mcp_weather_server.py for the
#   MCP approach!
