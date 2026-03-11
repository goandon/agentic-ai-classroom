"""
Episode 8: Build Agents with SDK
    — Subagents (Multi-Agent Sneak Peek)

Define specialized sub-agents that the
main agent can delegate tasks to.
A taste of Ep9's multi-agent systems!

Run:
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY="your-key-here"
  python handoff_agent.py

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
)


async def main():
    # ── Define specialist sub-agents ──
    # Each agent has its own instructions
    # and tool set.
    agents = {
        "code-reviewer": AgentDefinition(
            description=(
                "Reviews code for quality, "
                "bugs, and best practices."
            ),
            prompt=(
                "You are an expert code "
                "reviewer. Analyze code "
                "quality, find potential "
                "bugs, and suggest "
                "improvements. Be concise."
            ),
            tools=[
                "Read",
                "Glob",
                "Grep",
            ],
        ),
        "test-runner": AgentDefinition(
            description=(
                "Runs tests and reports "
                "results with analysis."
            ),
            prompt=(
                "You are a test specialist. "
                "Run the project's tests "
                "and analyze the results. "
                "Report failures clearly."
            ),
            tools=[
                "Bash",
                "Read",
            ],
        ),
    }

    # ── Main orchestrator ─────────────
    # The main agent can delegate to
    # sub-agents using the "Agent" tool.
    # It decides WHEN and WHO to call!
    async for message in query(
        prompt=(
            "Review the Python files in "
            "this directory for code "
            "quality, then run any "
            "available tests."
        ),
        options=ClaudeAgentOptions(
            allowed_tools=[
                "Read",
                "Glob",
                "Agent",
            ],
            agents=agents,
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)


if __name__ == "__main__":
    asyncio.run(main())


# ── How subagents work ────────────────
#
# 1. Main agent receives the task
# 2. It sees "Agent" in its tools
# 3. It picks the right sub-agent
#    (code-reviewer or test-runner)
# 4. Sub-agent runs in isolated context
# 5. Results flow back to main agent
# 6. Main agent synthesizes everything
#
# Think of it like a team:
#   Manager (main) delegates to
#   Specialists (sub-agents)
