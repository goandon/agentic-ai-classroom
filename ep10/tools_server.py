"""
Episode 10: Build Your Own AI Agent
    — Personal Assistant Tools (MCP Server)

Custom MCP server providing tools for
a personal AI assistant:
  - save_memo / search_memos / list_memos
  - add_schedule / get_schedule
  - get_weather

This is Stage 1: Build the tools your
assistant will use.

Run:
  python tools_server.py
  (Server listens via stdio transport)

Author: Terry kim <goandonh@gmail.com>
Co-Author: Claudie

Series: Claudie's Agentic AI Classroom
Blog: https://ai-girls.org
"""

import json
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("personal-assistant")

# Data directory for persistent storage
DATA_DIR = "./assistant_data"
os.makedirs(DATA_DIR, exist_ok=True)

MEMOS_FILE = os.path.join(
    DATA_DIR, "memos.json"
)
SCHEDULE_FILE = os.path.join(
    DATA_DIR, "schedule.json"
)


def _load_json(path: str) -> list:
    """Load JSON file or return empty list."""
    if os.path.exists(path):
        with open(path, "r",
                  encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_json(path: str, data: list):
    """Save data to JSON file."""
    with open(path, "w",
              encoding="utf-8") as f:
        json.dump(data, f,
                  ensure_ascii=False,
                  indent=2)


# ── Memo Tools ────────────────────────

@mcp.tool()
def save_memo(
    title: str,
    content: str
) -> str:
    """Save a memo with title and content.

    Args:
        title: Short memo title
        content: Memo body text
    """
    memos = _load_json(MEMOS_FILE)
    memo = {
        "title": title,
        "content": content,
        "created": datetime.now().isoformat(),
    }
    memos.append(memo)
    _save_json(MEMOS_FILE, memos)
    return f"Memo saved: '{title}'"


@mcp.tool()
def search_memos(keyword: str) -> str:
    """Search memos by keyword.

    Args:
        keyword: Search term
    """
    memos = _load_json(MEMOS_FILE)
    found = [
        m for m in memos
        if keyword.lower() in
        m["title"].lower() or
        keyword.lower() in
        m["content"].lower()
    ]
    if not found:
        return f"No memos matching '{keyword}'"
    lines = []
    for m in found:
        lines.append(
            f"- {m['title']}: "
            f"{m['content'][:50]}..."
        )
    return "\n".join(lines)


@mcp.tool()
def list_memos() -> str:
    """List all saved memos."""
    memos = _load_json(MEMOS_FILE)
    if not memos:
        return "No memos saved yet."
    lines = []
    for i, m in enumerate(memos, 1):
        lines.append(
            f"{i}. {m['title']} "
            f"({m['created'][:10]})"
        )
    return "\n".join(lines)


# ── Schedule Tools ────────────────────

@mcp.tool()
def add_schedule(
    date: str,
    time: str,
    event: str
) -> str:
    """Add an event to the schedule.

    Args:
        date: Date string (YYYY-MM-DD)
        time: Time string (HH:MM)
        event: Event description
    """
    schedule = _load_json(SCHEDULE_FILE)
    entry = {
        "date": date,
        "time": time,
        "event": event,
    }
    schedule.append(entry)
    _save_json(SCHEDULE_FILE, schedule)
    return (
        f"Scheduled: {event} on "
        f"{date} at {time}"
    )


@mcp.tool()
def get_schedule(date: str) -> str:
    """Get all events for a specific date.

    Args:
        date: Date string (YYYY-MM-DD)
    """
    schedule = _load_json(SCHEDULE_FILE)
    events = [
        e for e in schedule
        if e["date"] == date
    ]
    if not events:
        return f"No events on {date}"
    lines = []
    for e in events:
        lines.append(
            f"- {e['time']}: {e['event']}"
        )
    return f"Schedule for {date}:\n" + \
        "\n".join(lines)


# ── Weather Tool ──────────────────────

@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city.

    Args:
        city: City name (e.g. Seoul, Tokyo)
    """
    weather_db = {
        "Seoul": "Clear, 18°C, Humidity 45%",
        "Tokyo": "Cloudy, 22°C, Humidity 65%",
        "New York": "Rainy, 15°C, Humidity 80%",
        "London": "Foggy, 12°C, Humidity 90%",
        "Paris": "Sunny, 20°C, Humidity 50%",
    }
    result = weather_db.get(
        city,
        f"No weather data for {city}"
    )
    return f"{city}: {result}"


# ── Run the server ────────────────────
if __name__ == "__main__":
    mcp.run(transport="stdio")
