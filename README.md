# AIUCE Tool Harness

Tool registration and invocation framework for AI agents.

## Features

- **ToolSpec Protocol** — Declarative tool metadata with domain classification (BODY/FLOW/INTEL)
- **IPIPQClassifier** — File classification by extension and keyword matching (15 categories)
- **SmartFileRouter** — Keyword-driven file routing with priority-based rule chaining
- **ToolHarnessRegistry** — Central registry with optional sovereignty checks and audit logging
- **Dual-track output** — JSON for AI consumption, Markdown for human readability

## Installation

```bash
pip install aiuce-tool-harness
```

## Quick Start

```python
from aiuce_tool_harness import (
    ToolHarnessRegistry, ToolSpec, ToolDomain,
    IPIPQClassifier, SmartFileRouter,
)

# File classification
result = IPIPQClassifier.classify_file("/downloads/medical_report.pdf")
print(result["json"]["category"])  # "medical"
print(result["markdown"])          # "**medical_report.pdf** → `DATA/Medical/`"

# Smart file routing
router = SmartFileRouter()
route = router.classify("contract with client")
print(route["target"])  # "WORK/Business/"

# Tool registry
registry = ToolHarnessRegistry()
spec = ToolSpec(
    id="my-tool", name="My Tool",
    domain=ToolDomain.INTEL, layer="L9",
    description="Does something useful", cmd_template="run --input {path}",
)
registry.register(spec, handler=lambda p: {
    "json": {"result": "ok"}, "markdown": "✅ Done"
})
result = registry.invoke("my-tool", {"path": "/data/file.csv"})
```

## Architecture

```
┌──────────────────────┐
│  ToolHarnessRegistry │  ← Central registry
│  ├─ register(spec)   │
│  ├─ invoke(id, params)│
│  └─ list_tools()     │
├──────────────────────┤
│  IPIPQClassifier     │  ← File type classification
│  ├─ extension match  │
│  └─ keyword match    │
├──────────────────────┤
│  SmartFileRouter     │  ← Keyword-driven routing
│  ├─ rule chaining    │
│  └─ priority scoring │
└──────────────────────┘
```

## Three-Domain System

Every tool is classified into one of three domains:

- **BODY** — Execution: operations, tool calls, file processing
- **FLOW** — Flow: routing, scheduling, coordination
- **INTEL** — Intelligence: analysis, reasoning, decision support

## License

MIT License — Copyright 2026 Bill Gao
