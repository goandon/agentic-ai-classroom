"""
Episode 8: Build Agents with SDK
    — Agent with Built-in Tools

An agent that uses built-in tools (Read,
Glob, Grep, Bash). The SDK handles the
Think->Act->Observe cycle automatically!

Compare to Ep5's manual agent loop —
no JSON schema, no tool dispatch needed.

Run:
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY="your-key-here"
  python tool_agent.py

Author: Terry kim <goandonh@gmail.com>
Co-Author: Claudie

Series: Claudie's Agentic AI Classroom
Blog: https://ai-girls.org
"""

import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
)


# ── Example 1: File Explorer Agent ───
# Give the agent Read + Glob tools.
# It can now browse files by itself!
async def file_explorer():
    print("=== File Explorer Agent ===")
    async for message in query(
        prompt=(
            "List all Python files in the "
            "current directory and show "
            "the first 5 lines of each."
        ),
        options=ClaudeAgentOptions(
            allowed_tools=[
                "Read",
                "Glob",
            ],
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)


# ── Example 2: Code Analyst Agent ────
# Give the agent search tools (Grep)
# plus Bash for running commands.
async def code_analyst():
    print("=== Code Analyst Agent ===")
    async for message in query(
        prompt=(
            "Find all TODO comments in "
            "this project and create "
            "a prioritized summary."
        ),
        options=ClaudeAgentOptions(
            allowed_tools=[
                "Read",
                "Glob",
                "Grep",
                "Bash",
            ],
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)


# ── Ep5 (Raw API) vs Ep8 (SDK) ───────
#
# Ep5: Manual agent loop (50+ lines)
#   - Define tool JSON schema by hand
#   - Write while-loop for agent cycle
#   - Parse tool_use blocks manually
#   - Execute tools with if/elif chain
#   - Build tool_result messages
#   - Handle stop_reason yourself
#
# Ep8: SDK handles everything (5 lines)
#   - Just list tool names as strings
#   - query() runs the full loop
#   - Tools execute automatically
#   - Results stream back to you


if __name__ == "__main__":
    asyncio.run(file_explorer())
    # Uncomment for code analyst:
    # asyncio.run(code_analyst())
