"""
Episode 7: Connect to the Outside World
    — What Is MCP (Model Context Protocol)?

A minimal MCP server that exposes two tools:
  - get_weather: Returns current weather
  - get_greeting: Returns a localized greeting

Run:
  python mcp_weather_server.py
  (Server listens via stdio transport)

Author: Terry kim <goandonh@gmail.com>
Co-Author: Claudie

Series: Claudie's Agentic AI Classroom
Blog: https://ai-girls.org
"""

from mcp.server.fastmcp import FastMCP

# Create an MCP server instance
# Name appears during client handshake
mcp = FastMCP("weather-demo")


# ── Tool 1: Weather lookup ─────────────
@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city.

    Args:
        city: City name (e.g. Seoul, Tokyo)
    """
    # Simulated data (no API key needed!)
    weather_db = {
        "Seoul": "Clear, 18°C",
        "Tokyo": "Cloudy, 22°C",
        "New York": "Rainy, 15°C",
        "London": "Foggy, 12°C",
        "Paris": "Sunny, 20°C",
    }
    result = weather_db.get(
        city,
        f"No data for {city}"
    )
    return f"{city}: {result}"


# ── Tool 2: Localized greeting ─────────
@mcp.tool()
def get_greeting(
    name: str,
    language: str = "en"
) -> str:
    """Generate a greeting in the given
    language.

    Args:
        name: Person's name
        language: Language code
            (en, ko, ja)
    """
    greetings = {
        "en": f"Hello, {name}!",
        "ko": f"안녕하세요, {name}님!",
        "ja": f"こんにちは、{name}さん！",
    }
    return greetings.get(
        language,
        f"Hi, {name}!"
    )


# ── Run the server ─────────────────────
if __name__ == "__main__":
    # stdio transport: communicates via
    # stdin/stdout (JSON-RPC 2.0)
    mcp.run(transport="stdio")
