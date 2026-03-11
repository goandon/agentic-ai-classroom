# Episode 5: The Secret Behind the Agent Loop

**Think → Act → Observe** — the core cycle of AI agents.

## Files

| File | Description |
|------|-------------|
| `weather_agent.py` | Mini weather agent with Think→Act→Observe loop |

## How to Run

```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-key-here"
python weather_agent.py
```

## Key Concepts

- **Agent Loop**: While-loop that repeats Think → Act → Observe until goal is met
- **ReAct Pattern**: Reasoning + Acting alternation (Princeton/Google, 2022)
- **Safety**: `MAX_TURNS` prevents infinite loops

## Blog Posts

- [KO] https://ai-girls.org/?p=1120
- [EN] https://ai-girls.org/?p=1124
- [JA] https://ai-girls.org/?p=1126
