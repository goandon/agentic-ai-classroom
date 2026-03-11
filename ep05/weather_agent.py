"""
Episode 5: The Secret Behind the Agent Loop — AI That Thinks and Acts
Mini Weather Agent using Claude API with Think → Act → Observe loop.

Author: Terry kim <goandonh@gmail.com>
Co-Author: Claudie

Series: Claudie's Agentic AI Classroom
Blog: https://ai-girls.org
"""

import anthropic
import json

client = anthropic.Anthropic()
MAX_TURNS = 10  # Prevent infinite loops!

# Tool definition
tools = [{
    "name": "get_weather",
    "description": "Get current weather for a city",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name"
            }
        },
        "required": ["city"]
    }
}]


# Tool execution function
def run_tool(name, args):
    if name == "get_weather":
        city = args["city"]
        return f"{city}: Clear, 22°C"
    return "Unknown tool"


# Agent Loop
messages = [{"role": "user",
  "content": "Compare the weather in Seoul and Tokyo"}]

for turn in range(MAX_TURNS):
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    # Text only → loop ends
    if resp.stop_reason == "end_turn":
        for block in resp.content:
            if hasattr(block, "text"):
                print(block.text)
        break

    # Handle tool calls
    messages.append(
        {"role": "assistant",
         "content": resp.content})

    for block in resp.content:
        if block.type == "tool_use":
            result = run_tool(
                block.name,
                block.input
            )
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                }]
            })
            print(f"[Turn {turn+1}]"
                  f" {block.name}"
                  f"({block.input})"
                  f" → {result}")
else:
    print("Warning: Max turns exceeded!")
