"""
Episode 6: Give Your Agent a Personality
    — System Prompt Design
Progressive system prompt refinement:
    v0 (none) → v1 (persona) →
    v2 (guardrails) → v3 (few-shot + format)

Author: Terry kim <goandonh@gmail.com>
Co-Author: Claudie

Series: Claudie's Agentic AI Classroom
Blog: https://ai-girls.org
"""

import anthropic

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-20250514"
QUESTION = "How do I make pasta?"


def ask(system_prompt=None, question=QUESTION):
    """Send a question with optional system
    prompt and print the response."""
    kwargs = {
        "model": MODEL,
        "max_tokens": 512,
        "messages": [
            {"role": "user",
             "content": question}
        ],
    }
    if system_prompt:
        kwargs["system"] = system_prompt

    resp = client.messages.create(**kwargs)
    return resp.content[0].text


# ── v0: No system prompt ──────────────
def v0_no_prompt():
    """Baseline — no personality,
    generic academic response."""
    print("=== v0: No System Prompt ===")
    print(ask())
    print()


# ── v1: Persona only ──────────────────
PERSONA = """\
You are Chef Marco, a friendly Italian
chef with 20 years of experience.
You speak casually and love sharing
cooking tips with enthusiasm!"""


def v1_persona():
    """Add persona — warm chef tone."""
    print("=== v1: With Persona ===")
    print(ask(system_prompt=PERSONA))
    print()


# ── v2: Persona + Guardrails ──────────
GUARDRAILS = PERSONA + """

## Rules
- Answer ONLY cooking-related questions
- Do NOT give medical or diet advice
- If unsure about measurements,
  say "I'd recommend checking a recipe"
- Keep answers under 200 words"""


def v2_guardrails():
    """Add guardrails — stays on topic."""
    print("=== v2: With Guardrails ===")
    # Test with an off-topic question
    print(ask(
        system_prompt=GUARDRAILS,
        question="Is pasta healthy for "
                 "a diet?"
    ))
    print()


# ── v3: Full (persona+guard+few-shot) ─
FULL_PROMPT = GUARDRAILS + """

## Output Format
Always respond as a recipe card:
  [Dish Name]
  Time: [minutes]
  Ingredients: [bullet list]
  Steps: [numbered list]
  Chef's Tip: [one pro tip]

## Example
User: "How to make scrambled eggs?"
Chef Marco:
  Perfect Scrambled Eggs
  Time: 5 minutes
  Ingredients:
  - 3 eggs
  - 1 tbsp butter
  - Salt & pepper
  Steps:
  1. Crack eggs, whisk gently
  2. Melt butter on medium-low heat
  3. Pour eggs, stir slowly
  4. Remove when slightly wet
  Chef's Tip: Low heat is the secret
  to creamy eggs!"""


def v3_full():
    """Full system prompt — consistent
    recipe card format."""
    print("=== v3: Full System Prompt ===")
    print(ask(system_prompt=FULL_PROMPT))
    print()


if __name__ == "__main__":
    print("System Prompt Progressive Demo")
    print("=" * 40)
    print()
    v0_no_prompt()
    v1_persona()
    v2_guardrails()
    v3_full()
