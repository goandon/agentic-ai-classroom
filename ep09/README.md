# Episode 9: Multi-Agent Systems

**Multi-Agent AI** — Build teams of specialized agents.

## Files

| File | Description |
|------|-------------|
| `simple_pipeline.py` | Sequential: Researcher → Writer pipeline |
| `parallel_agents.py` | Parallel: SEO + Image agents run simultaneously |
| `blog_team.py` | Orchestrator: Editor manages Researcher → Writer → Reviewer |

## How to Run

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
```

### 1. Sequential Pipeline (simplest)

```bash
python simple_pipeline.py
```

Two agents in a relay: Researcher gathers facts, then Writer turns them into a blog post. One finishes before the next starts.

### 2. Parallel Agents (simultaneous)

```bash
python parallel_agents.py
```

SEO Researcher and Image Director work at the same time on independent tasks. Same total work, less wall-clock time.

### 3. Blog Team Orchestrator (full team)

```bash
python blog_team.py
```

An Editor-in-Chief coordinates three specialists: Researcher → Writer → Reviewer. The editor manages but never does the actual work — that's the orchestrator pattern!

## Key Concepts

- **Sequential Pattern**: Agents work one after another (A → B → C)
- **Parallel Pattern**: Independent agents work simultaneously (A + B → merge)
- **Orchestrator Pattern**: A manager agent delegates to specialists
- **`AgentDefinition`**: Define each agent's role, instructions, and tools
- **Role isolation**: Each agent has its own prompt and limited tools — constraints improve quality

## 3 Patterns Compared

| Pattern | When to Use | Example |
|---------|-------------|---------|
| Sequential | Tasks depend on previous results | Research → Write |
| Parallel | Tasks are independent | SEO + Image |
| Orchestrator | Complex workflow needing judgment | Editor manages team |

## Real-World Connection

The blog-agent that publishes *Claudie's Agentic AI Classroom* uses a 10-agent pipeline — the same orchestrator pattern from `blog_team.py`, just at production scale!

## Blog Posts

- [KO] Coming soon
- [EN] Coming soon
- [JA] Coming soon
