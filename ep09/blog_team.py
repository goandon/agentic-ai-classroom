"""
Episode 9: Multi-Agent Systems
    — Blog Team Orchestrator (3 Agents)

An editor-in-chief orchestrates a team:
Researcher → Writer → Reviewer.

The editor doesn't write or research —
it MANAGES. Like a real newsroom!

This mirrors the blog-agent pipeline
that publishes this very series.

Run:
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY="your-key-here"
  python blog_team.py

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
    # ── Define the team ────────────────
    # Three specialists, each with
    # a clear role and focused tools.
    agents = {
        "researcher": AgentDefinition(
            description=(
                "Researches topics using "
                "web search."
            ),
            prompt=(
                "You are a tech "
                "researcher. Search for "
                "recent info on the given "
                "topic. Return a "
                "structured briefing "
                "with:\n"
                "- Key facts (3-5)\n"
                "- Recent trends\n"
                "- One concrete example"
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
                "Write an engaging post "
                "using the research. "
                "Use clear sections, "
                "simple language, and "
                "a friendly tone. "
                "Target: 300-500 words."
            ),
            tools=[],
        ),
        "reviewer": AgentDefinition(
            description=(
                "Reviews drafts for "
                "quality and accuracy."
            ),
            prompt=(
                "You are a blog editor. "
                "Review the draft for:\n"
                "- Factual accuracy\n"
                "- Clarity and flow\n"
                "- Engagement level\n"
                "Provide specific, "
                "actionable feedback. "
                "Then rewrite the "
                "improved version."
            ),
            tools=[],
        ),
    }

    # ── Editor orchestrates ────────────
    # The editor-in-chief decides:
    #   WHO does what, in WHAT order.
    # It delegates, collects results,
    # and synthesizes the final output.
    #
    # This is the orchestrator pattern:
    #        ┌─ Researcher
    #  Editor├─ Writer
    #        └─ Reviewer
    print("=== Blog Team Orchestrator ===")
    print("Editor → Research → Write "
          "→ Review\n")

    async for msg in query(
        prompt=(
            "Create a blog post about "
            "'How AI agents work "
            "together as a team'. "
            "Research it, write it, "
            "then review and improve."
        ),
        options=ClaudeAgentOptions(
            system_prompt=(
                "You are an editor-in-"
                "chief managing a blog "
                "team. Your workflow:\n"
                "1. Call researcher to "
                "gather facts\n"
                "2. Call writer to draft "
                "the post using "
                "research\n"
                "3. Call reviewer to "
                "improve the draft\n"
                "Return the final "
                "polished blog post."
            ),
            allowed_tools=[
                "Agent",
            ],
            agents=agents,
            max_turns=15,
        ),
    ):
        if hasattr(msg, "result"):
            print(msg.result)


if __name__ == "__main__":
    asyncio.run(main())


# ── How the orchestrator works ─────────
#
# 1. Editor receives "write a blog post"
# 2. Editor calls researcher
#    → "Research AI agent teamwork"
#    → Researcher searches the web
#    → Returns structured briefing
# 3. Editor calls writer
#    → "Write a post using this research"
#    → Writer drafts the blog post
#    → Returns the draft
# 4. Editor calls reviewer
#    → "Review and improve this draft"
#    → Reviewer gives feedback + rewrite
#    → Returns improved version
# 5. Editor synthesizes final result
#
# Key insight: The editor NEVER writes,
# researches, or reviews. It only
# COORDINATES. That's the orchestrator.
#
# Real-world scale:
#   The blog-agent that publishes
#   "Claudie's Agentic AI Classroom"
#   uses 10 agents in its pipeline:
#   SEO → Research → Art Direction →
#   Writing → Editing → Supervision →
#   Publishing → Translation →
#   Polylang Ops
#
# Today's 3-agent team is the same
# concept — just smaller!
