# Episode 10: Build Your Own AI Agent — Capstone Lab

Build a personal AI assistant from scratch, combining everything from Episodes 1–9!

## Files

| File | Stage | What You'll Learn |
|------|-------|-------------------|
| `tools_server.py` | 1. Build the tools | MCP server with FastMCP (EP7) |
| `simple_assistant.py` | 2. Connect tools | SDK + MCP integration (EP5, EP8) |
| `smart_assistant.py` | 3. Add personality | System prompts (EP6) + Hooks (NEW) |
| `team_assistant.py` | 4. Build a team | Multi-agent orchestrator (EP9) |
| `persistent_assistant.py` | 5. Add memory | Sessions for conversation continuity (NEW) |

## How to Run

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"

# Run each stage in order:
python simple_assistant.py    # Stage 2
python smart_assistant.py     # Stage 3
python team_assistant.py      # Stage 4
python persistent_assistant.py # Stage 5
```

Note: `tools_server.py` (Stage 1) runs automatically — the SDK spawns it as a subprocess via `MCPServerStdio`.

## Key Concepts

- **MCP Server**: Custom tools via FastMCP (`@mcp.tool()` decorator)
- **Claude Agent SDK**: `query()`, `ClaudeAgentOptions`, `AgentDefinition`
- **Hooks** (NEW): `PreToolUse` blocks dangerous operations, `PostToolUse` logs activity
- **Sessions** (NEW): `ResultMessage.session_id` + `resume` parameter for conversation memory
- **Multi-Agent**: Orchestrator delegates to specialist agents (Scheduler, Researcher, Assistant)

## Blog Post

- KO: Coming soon
- EN: Coming soon
- JA: Coming soon
