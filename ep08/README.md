# Episode 8: Build Agents with SDK

**Claude Agent SDK** — Assemble agents like building blocks.

## Files

| File | Description |
|------|-------------|
| `hello_agent.py` | Simplest agent — just `query()` + a prompt |
| `tool_agent.py` | Agent with built-in tools (Read, Glob, Grep, Bash) |
| `handoff_agent.py` | Subagents — delegate tasks to specialist agents |

## How to Run

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
```

### 1. Hello Agent (simplest possible)

```bash
python hello_agent.py
```

Just `query(prompt="...")` — that's it. Compare to Ep5's 50+ line manual agent loop!

### 2. Tool Agent (built-in tools)

```bash
python tool_agent.py
```

List tool names as strings in `allowed_tools` — no JSON schema, no tool dispatch. The SDK runs the Think→Act→Observe loop for you.

### 3. Subagent (multi-agent sneak peek)

```bash
python handoff_agent.py
```

Define specialist agents with `AgentDefinition`, then let the main agent delegate using the `Agent` tool. A preview of Ep9's multi-agent systems!

## Key Concepts

- **`query()`**: The main entry point — runs the full agent loop as an async generator
- **`ClaudeAgentOptions`**: Configure tools, system prompt, max turns, MCP servers, etc.
- **Built-in tools**: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
- **`AgentDefinition`**: Define subagents with their own instructions and tool sets
- **Sessions**: Resume conversations with `resume=session_id`

## Ep5 vs Ep8 Comparison

| Aspect | Ep5 (Raw API) | Ep8 (Agent SDK) |
|--------|---------------|-----------------|
| Agent loop | Manual while-loop | `query()` handles it |
| Tool definition | JSON schema dict | String names or AgentDefinition |
| Tool execution | Manual dispatch | Built-in, automatic |
| Error handling | DIY | Built-in |
| Multi-agent | Not supported | Subagents via AgentDefinition |
| Lines of code | ~80 | ~10 |

## Blog Posts

- [KO] Coming soon
- [EN] Coming soon
- [JA] Coming soon
