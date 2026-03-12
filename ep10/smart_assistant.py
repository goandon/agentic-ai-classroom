"""
Episode 10: Build Your Own AI Agent
    — Stage 3: Smart Assistant (Hooks)

Add personality (system prompt, EP6) and
safety monitoring (Hooks — NEW!).

Hooks intercept tool calls:
  - PreToolUse: Block dangerous operations
  - PostToolUse: Log everything

Like hiring a security guard for
your assistant!

Run:
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY="your-key-here"
  python smart_assistant.py

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


# ── Hook 1: Safety guard ─────────────
# Runs BEFORE a tool executes.
# Can block dangerous operations.

async def safety_guard(
    input_data, tool_use_id, context
):
    """Block writes to system paths."""
    tool = input_data["tool_name"]
    tool_input = input_data["tool_input"]

    if tool in ("Write", "Edit"):
        path = tool_input.get(
            "file_path", ""
        )
        blocked = [
            "/etc/", "/usr/",
            "C:\\Windows", "C:\\Program",
        ]
        if any(p in path for p in blocked):
            print(
                f"[BLOCKED] {tool} → {path}"
            )
            return {
                "hookSpecificOutput": {
                    "hookEventName":
                        input_data[
                            "hook_event_name"
                        ],
                    "permissionDecision":
                        "deny",
                    "permissionDecisionReason":
                        "System path blocked",
                }
            }
    return {}  # Allow


# ── Hook 2: Activity logger ──────────
# Runs AFTER a tool executes.
# Logs every tool call for monitoring.

async def activity_logger(
    input_data, tool_use_id, context
):
    """Log all tool usage."""
    tool = input_data["tool_name"]
    print(f"  [LOG] Tool used: {tool}")
    return {}


async def main():
    # ── Personality (EP6) ─────────────
    system_prompt = (
        "You are a friendly, helpful "
        "personal AI assistant. Your name "
        "is 'Buddy'.\n\n"
        "Rules:\n"
        "- Use warm, casual tone\n"
        "- Suggest related actions\n"
        "- Confirm before modifying files\n"
        "- If asked what you can do, "
        "list your tools"
    )

    # ── Hooks (NEW!) ─────────────────
    # PreToolUse: safety_guard blocks
    #   dangerous file writes
    # PostToolUse: activity_logger logs
    #   every tool call
    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
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
            "PreToolUse": [
                HookMatcher(
                    matcher="Write|Edit",
                    hooks=[safety_guard],
                ),
            ],
            "PostToolUse": [
                HookMatcher(
                    hooks=[activity_logger],
                ),
            ],
        },
        max_turns=10,
    )

    print("=== Smart Assistant (Buddy) ===")
    print("With personality + safety\n")

    async for msg in query(
        prompt=(
            "Hi Buddy! Save a memo about "
            "my grocery list: milk, eggs, "
            "bread. Then check the weather "
            "in Tokyo."
        ),
        options=options,
    ):
        if isinstance(msg, ResultMessage):
            if msg.subtype == "success":
                print(f"\n{msg.result}")


if __name__ == "__main__":
    asyncio.run(main())


# ── What Hooks do ────────────────────
#
# Without Hooks:
#   Agent calls Write("/etc/passwd")
#   → File gets modified! Danger!
#
# With PreToolUse Hook:
#   Agent calls Write("/etc/passwd")
#   → Hook fires BEFORE execution
#   → Returns "deny"
#   → Tool call BLOCKED. Safe!
#
# PostToolUse Hook:
#   Agent calls any tool
#   → Tool executes normally
#   → Hook fires AFTER execution
#   → Logs the tool name
#   → Great for monitoring
#
# Think of Hooks as a security system:
# PreToolUse  = the front door lock
# PostToolUse = the security camera
