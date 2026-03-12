"""
Episode 9: Multi-Agent Systems
    — Sequential Pipeline (2 Agents)

Two agents working in sequence:
Researcher finds information, then
Writer creates a blog post from it.

Like a relay race — each agent runs
their leg and passes the baton!

Run:
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY="your-key-here"
  python simple_pipeline.py

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
    # ── Define specialist agents ───────
    # Each agent has ONE job.
    # Researcher searches the web.
    # Writer turns research into prose.
    agents = {
        "researcher": AgentDefinition(
            description=(
                "Researches a topic and "
                "returns a briefing."
            ),
            prompt=(
                "You are a tech researcher."
                " Find key facts, recent "
                "trends, and concrete "
                "examples about the topic."
                " Return a structured "
                "briefing with bullet "
                "points."
            ),
            tools=[
                "WebSearch",
                "WebFetch",
            ],
        ),
        "writer": AgentDefinition(
            description=(
                "Writes blog posts from "
                "research briefings."
            ),
            prompt=(
                "You are a blog writer. "
                "Using the research "
                "provided, write an "
                "engaging blog post with "
                "clear sections and a "
                "friendly tone."
            ),
            tools=[],
        ),
    }

    # ── Sequential pipeline ────────────
    # The manager calls researcher FIRST,
    # then passes results to writer.
    # This is the sequential pattern:
    #   Agent A → Agent B → Done
    print("=== Sequential Pipeline ===")
    print("Researcher → Writer\n")

    async for msg in query(
        prompt=(
            "Create a short blog post "
            "about multi-agent AI "
            "systems. First research "
            "the topic, then write "
            "the post."
        ),
        options=ClaudeAgentOptions(
            system_prompt=(
                "You are a pipeline "
                "manager. Follow this "
                "exact order:\n"
                "1. Call researcher to "
                "gather facts\n"
                "2. Call writer to create "
                "a blog post from the "
                "research\n"
                "Return the final post."
            ),
            allowed_tools=["Agent"],
            agents=agents,
            max_turns=10,
        ),
    ):
        if hasattr(msg, "result"):
            print(msg.result)


if __name__ == "__main__":
    asyncio.run(main())


# ── How sequential pipelines work ──────
#
# 1. Manager receives the task
# 2. Calls researcher (Agent A)
#    → researcher searches the web
#    → returns a briefing
# 3. Calls writer (Agent B)
#    → writer gets the briefing
#    → returns a blog post
# 4. Manager returns the final result
#
# Key insight: Writer never searches.
# Researcher never writes. Each agent
# is focused on ONE thing.
#
# Real-world example:
#   The blog-agent that publishes
#   this series uses 10 agents
#   in a sequential pipeline!
