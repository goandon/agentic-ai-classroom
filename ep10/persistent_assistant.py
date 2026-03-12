"""
Episode 10: Build Your Own AI Agent
    — Stage 5: Persistent Assistant
      (Sessions)

The final evolution: an assistant that
REMEMBERS across conversations!

Sessions (NEW!) let you capture a
session_id and resume later with full
context.

Run:
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY="your-key-here"
  python persistent_assistant.py

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
    HookMatcher,
    ResultMessage,
)


# Reuse the activity logger from Stage 3
async def activity_logger(
    input_data, tool_use_id, context
):
    """Log all tool usage."""
    tool = input_data["tool_name"]
    print(f"  [LOG] {tool}")
    return {}


def build_options():
    """Build shared options for all turns."""
    return ClaudeAgentOptions(
        system_prompt=(
            "You are Buddy, a friendly "
            "personal AI assistant with "
            "persistent memory. You "
            "remember previous "
            "conversations."
        ),
        allowed_tools=[
            "WebSearch", "Read", "Write",
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
        hooks={
            "PostToolUse": [
                HookMatcher(
                    hooks=[activity_logger],
                ),
            ],
        },
        max_turns=10,
    )


async def main():
    print("=== Persistent Assistant ===")
    print("Sessions = Memory!\n")

    # ── Turn 1: Save something ────────
    print("--- Turn 1: Save a memo ---")
    session_id = None

    async for msg in query(
        prompt=(
            "Save a memo titled "
            "'Project Ideas' with content "
            "'Build a recipe recommender "
            "using MCP tools'."
        ),
        options=build_options(),
    ):
        if isinstance(msg, ResultMessage):
            session_id = msg.session_id
            if msg.subtype == "success":
                print(msg.result)

    print(f"\nSession ID: {session_id}\n")

    # ── Turn 2: Ask WITH memory ───────
    print("--- Turn 2: With Memory ---")
    print("(Using resume=session_id)\n")

    async for msg in query(
        prompt="What memo did I just save?",
        options=ClaudeAgentOptions(
            **{
                **build_options().__dict__,
                "resume": session_id,
            }
        ),
    ):
        if isinstance(msg, ResultMessage):
            if msg.subtype == "success":
                print(msg.result)

    # ── Turn 2b: Ask WITHOUT memory ───
    print("\n--- Turn 2b: No Memory ---")
    print("(Fresh session, no resume)\n")

    async for msg in query(
        prompt="What memo did I just save?",
        options=build_options(),
    ):
        if isinstance(msg, ResultMessage):
            if msg.subtype == "success":
                print(msg.result)


if __name__ == "__main__":
    asyncio.run(main())


# ── How Sessions work ────────────────
#
# Without sessions:
#   Turn 1: "Save a memo about X"
#   Turn 2: "What did I save?"
#   → "I don't have any context"
#   (Each query() starts fresh!)
#
# With sessions:
#   Turn 1: "Save a memo about X"
#   → Capture session_id from
#     ResultMessage
#   Turn 2: query(resume=session_id)
#   → "You saved a memo about X!"
#   (Full context restored!)
#
# Think of session_id as a bookmark:
#   It marks WHERE you were in the
#   conversation so you can come back.
#
# Even easier? Use ClaudeSDKClient:
#   async with ClaudeSDKClient() as c:
#       await c.query("Save memo...")
#       await c.query("What did I save?")
#   # Automatic! No session_id needed.
#
# ── The 5-Stage Journey ──────────────
#
# Stage 1: tools_server.py
#   → Built the tools (EP7: MCP)
# Stage 2: simple_assistant.py
#   → Connected tools (EP5+EP8: SDK)
# Stage 3: smart_assistant.py
#   → Added personality + safety
#     (EP6: Prompt, NEW: Hooks)
# Stage 4: team_assistant.py
#   → Built a team (EP9: Multi-Agent)
# Stage 5: persistent_assistant.py
#   → Added memory (EP4+NEW: Sessions)
#
# You just built a REAL AI assistant
# using everything from EP1 to EP10!
