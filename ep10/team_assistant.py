"""
Episode 10: Build Your Own AI Agent
    — Stage 4: Team Assistant (Multi-Agent)

Upgrade from a solo assistant to a team:
  - Scheduler: manages calendar
  - Researcher: finds information
  - Assistant: handles memos and files

An orchestrator delegates to the right
specialist — just like EP9!

Run:
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY="your-key-here"
  python team_assistant.py

Author: Terry kim <goandonh@gmail.com>
Co-Author: Claudie

Series: Claudie's Agentic AI Classroom
Blog: https://ai-girls.org
"""

import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AgentDefinition,
    MCPServerStdio,
    HookMatcher,
    ResultMessage,
)


# ── Reuse Hooks from Stage 3 ─────────

async def activity_logger(
    input_data, tool_use_id, context
):
    """Log all tool usage."""
    agent = input_data.get(
        "agent_type", "main"
    )
    tool = input_data["tool_name"]
    print(f"  [LOG] {agent}: {tool}")
    return {}


async def main():
    # ── Define the team (EP9) ─────────
    agents = {
        "scheduler": AgentDefinition(
            description=(
                "Manages calendar and "
                "schedules."
            ),
            prompt=(
                "You are a precise "
                "scheduling assistant. "
                "Add events, check "
                "schedules, and confirm "
                "all dates clearly."
            ),
            tools=[
                "mcp__assistant__"
                "add_schedule",
                "mcp__assistant__"
                "get_schedule",
            ],
        ),
        "researcher": AgentDefinition(
            description=(
                "Searches the web for "
                "information."
            ),
            prompt=(
                "You are a thorough "
                "research assistant. "
                "Search for recent, "
                "accurate information. "
                "Always cite sources."
            ),
            tools=[
                "WebSearch",
                "WebFetch",
            ],
        ),
        "assistant": AgentDefinition(
            description=(
                "Handles memos, files, "
                "and general tasks."
            ),
            prompt=(
                "You are a helpful "
                "personal assistant. "
                "Manage memos, read/write "
                "files, and handle "
                "general requests."
            ),
            tools=[
                "Read", "Write",
                "mcp__assistant__"
                "save_memo",
                "mcp__assistant__"
                "search_memos",
                "mcp__assistant__"
                "list_memos",
                "mcp__assistant__"
                "get_weather",
            ],
        ),
    }

    # ── Orchestrator ──────────────────
    options = ClaudeAgentOptions(
        system_prompt=(
            "You are a team manager "
            "coordinating 3 specialists:\n"
            "- scheduler: for calendar\n"
            "- researcher: for web search\n"
            "- assistant: for memos/files\n"
            "\n"
            "Route each request to the "
            "right specialist. You can "
            "chain them: researcher finds "
            "info, then assistant saves "
            "it as a memo."
        ),
        allowed_tools=["Agent"],
        agents=agents,
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
        max_turns=15,
    )

    print("=== Team Assistant ===")
    print("Scheduler + Researcher "
          "+ Assistant\n")

    async for msg in query(
        prompt=(
            "I need three things: "
            "1) Schedule a dentist "
            "appointment on 2026-03-20 "
            "at 14:00. "
            "2) Search for the best "
            "cafes in Seoul. "
            "3) Save the cafe list as "
            "a memo titled 'Seoul Cafes'."
        ),
        options=options,
    ):
        if isinstance(msg, ResultMessage):
            if msg.subtype == "success":
                print(f"\n{msg.result}")


if __name__ == "__main__":
    asyncio.run(main())


# ── Team Architecture ────────────────
#
#          ┌─ Scheduler (calendar)
#  Manager ├─ Researcher (web search)
#          └─ Assistant (memos/files)
#
# This is the Orchestrator pattern
# from EP9! The manager:
#   1. Receives the user request
#   2. Routes to the right specialist
#   3. Can chain: Researcher → Assistant
#   4. Synthesizes the final answer
#
# Compare to EP9's blog_team.py:
#   3 agents (Researcher, Writer, Reviewer)
# Here:
#   3 agents (Scheduler, Researcher,
#             Assistant)
#
# Same pattern, different specialists!
