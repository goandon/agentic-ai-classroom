# Episode 7: Connect to the Outside World

**MCP (Model Context Protocol)** — The universal connector for AI agents.

## Files

| File | Description |
|------|-------------|
| `mcp_weather_server.py` | Minimal MCP server with 2 tools (weather + greeting) |
| `mcp_client_demo.py` | MCP client that connects, discovers, and calls tools |
| `no_mcp_compare.py` | Before-MCP: hardcoded tool approach (shows the problem MCP solves) |

## How to Run

```bash
pip install -r requirements.txt
```

### 1. Run the MCP client demo (auto-launches server)

```bash
python mcp_client_demo.py
```

This starts the MCP server as a subprocess and demonstrates:
- Connecting via stdio transport
- Discovering available tools
- Calling tools and getting results

### 2. Run the "old way" comparison

```bash
export ANTHROPIC_API_KEY="your-key-here"
python no_mcp_compare.py
```

This shows how tools worked before MCP — hardcoded in each app, no reuse.

## Key Concepts

- **MCP Server**: Exposes tools/resources via a standard protocol
- **MCP Client**: Connects to servers, discovers and calls tools
- **Transport**: How client and server communicate (stdio or HTTP)
- **Tool Discovery**: Client asks "what can you do?" at runtime
- **JSON-RPC 2.0**: The message format under the hood

## The USB-C Analogy

Think of MCP as **USB-C for AI**:
- Before USB-C: every device had a different charger (custom integrations)
- After USB-C: one cable works with everything (MCP standard protocol)

## Blog Posts

- [KO] Coming soon
- [EN] Coming soon
- [JA] Coming soon
