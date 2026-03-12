"""
Episode 10: Build Your Own AI Agent
    — Stage 2: Basic Personal Assistant

Connect the MCP tools from Stage 1 with
built-in tools (WebSearch, Read, Write)
to create a working assistant.

No personality yet, no safety — just raw
capability. Like EP5's agent loop, but
the SDK handles everything!

Run:
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY="your-key-here"
  python simple_assistant.py

Author: Terry kim <goandonh@gmail.com>
Co-Author: Claudie

Series: Claudie's Agentic AI Classroom
Blog: https://ai-girls.org
"""

import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    MCPServerStdio,
    ResultMessage,
)


async def main():
    # ── Connect tools ─────────────────
    # MCP server = custom tools (EP7)
    # Built-in tools = WebSearch, Read,
    #   Write (EP8)
    options = ClaudeAgentOptions(
        allowed_tools=[
            # Built-in tools
            "WebSearch", "Read", "Write",
            # MCP tools (server__tool format)
            "mcp__assistant__save_memo",
            "mcp__assistant__search_memos",
            "mcp__assistant__list_memos",
            "mcp__assistant__add_schedule",
            "mcp__assistant__get_schedule",
            "mcp__assistant__get_weather",
        ],
        mcp_servers={
            "assistant": MCPServerStdio(
                command="python",
                args=["tools_server.py"],
            )
        },
        max_turns=10,
    )

    print("=== Basic Personal Assistant ===")
    print("(No personality, no safety)\n")

    # ── Run the assistant ─────────────
    # One query() call — the SDK handles
    # the entire agent loop (EP5) for us!
    async for msg in query(
        prompt=(
            "Save a memo titled 'Meeting' "
            "with content 'Team sync at 3pm "
            "tomorrow'. Then check the "
            "weather in Seoul."
        ),
        options=options,
    ):
        if isinstance(msg, ResultMessage):
            if msg.subtype == "success":
                print(msg.result)


if __name__ == "__main__":
    asyncio.run(main())


# ── What just happened? ──────────────
#
# 1. SDK spawned tools_server.py as
#    a subprocess (MCPServerStdio)
# 2. Agent discovered 6 MCP tools +
#    3 built-in tools
# 3. Agent decided which tools to call
#    (save_memo, get_weather)
# 4. SDK ran the agent loop (EP5)
#    automatically
#
# Total code: ~40 lines (vs 50+ in EP5
# for a MUCH simpler agent!)
#
# But notice: no personality, no safety
# guardrails. Stage 3 fixes that.
