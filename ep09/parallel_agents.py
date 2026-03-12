"""
Episode 9: Multi-Agent Systems
    — Parallel Agents (2 Agents)

Two agents working simultaneously:
SEO Researcher analyzes keywords while
Image Director plans visuals.

Like two chefs prepping different
dishes at the same time!

Run:
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY="your-key-here"
  python parallel_agents.py

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
    # ── Define independent agents ──────
    # These two agents do NOT depend
    # on each other's results.
    # Perfect for parallel execution!
    agents = {
        "seo-researcher": AgentDefinition(
            description=(
                "Analyzes SEO keywords "
                "and search trends."
            ),
            prompt=(
                "You are an SEO "
                "specialist. Analyze "
                "search trends for the "
                "given topic. Return: "
                "top 5 keywords, search "
                "volume hints, and a "
                "suggested blog title."
            ),
            tools=["WebSearch"],
        ),
        "image-director": AgentDefinition(
            description=(
                "Plans visual content "
                "for blog posts."
            ),
            prompt=(
                "You are an art director."
                " Plan the visual content"
                " for a blog post: "
                "featured image concept, "
                "2 diagram ideas, and "
                "color palette suggestion."
            ),
            tools=[],
        ),
    }

    # ── Parallel execution ─────────────
    # The manager calls BOTH agents.
    # Since their tasks are independent,
    # they can run at the same time.
    # This is the parallel pattern:
    #   Agent A ──┐
    #             ├→ Merge results
    #   Agent B ──┘
    print("=== Parallel Agents ===")
    print("SEO + Image (simultaneous)\n")

    async for msg in query(
        prompt=(
            "For a blog post about "
            "'multi-agent AI systems': "
            "1) Research SEO keywords "
            "2) Plan the images. "
            "These tasks are "
            "independent."
        ),
        options=ClaudeAgentOptions(
            system_prompt=(
                "You manage parallel "
                "tasks. Call BOTH "
                "seo-researcher AND "
                "image-director — they "
                "don't depend on each "
                "other, so dispatch them "
                "together. Combine their "
                "results into a unified "
                "content brief."
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


# ── How parallel execution works ───────
#
# 1. Manager receives the task
# 2. Calls seo-researcher AND
#    image-director at the same time
# 3. Both agents work independently:
#    - SEO agent searches for keywords
#    - Image agent plans visuals
# 4. Manager collects both results
# 5. Merges into a unified brief
#
# Key insight: Parallel only works
# when tasks are INDEPENDENT.
# If Agent B needs Agent A's output,
# use sequential instead.
#
# Time saved:
#   Sequential: time(A) + time(B)
#   Parallel:   max(time(A), time(B))
