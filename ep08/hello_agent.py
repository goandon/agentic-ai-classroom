"""
Episode 8: Build Agents with SDK
    — Claude Agent SDK Introduction

The simplest possible agent using
Claude Agent SDK. Just a few lines to
create a working agent with built-in tools!

Compare this to Ep5's manual agent loop
(50+ lines of boilerplate).

Run:
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY="your-key-here"
  python hello_agent.py

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


async def main():
    # The simplest agent — just a prompt!
    # No tool definitions, no agent loop,
    # no message handling needed.
    async for message in query(
        prompt="What is Agentic AI? "
               "Explain in 2 sentences.",
    ):
        # Each message is a streaming event
        # from the agent's execution
        if hasattr(message, "result"):
            print(message.result)


asyncio.run(main())


# ── With options ──────────────────────
# You can customize the agent's behavior
# with ClaudeAgentOptions.

async def with_options():
    options = ClaudeAgentOptions(
        system_prompt=(
            "You are a friendly AI teacher. "
            "Explain concepts simply using "
            "everyday analogies."
        ),
        max_turns=3,
    )

    async for message in query(
        prompt="What is an AI agent?",
        options=options,
    ):
        if hasattr(message, "result"):
            print(message.result)

# Uncomment to run with options:
# asyncio.run(with_options())
