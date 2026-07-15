> ⚠️ **Deprecated — legacy AIUCE family.** This repo is being consolidated into **SONUV** / **AIOBR** / a unified history archive (2026). No new work is accepted. Current status: **[aiuce.com](https://aiuce.com)**. _Marked 2026-07-15._
>
> _本仓库属旧 AIUCE 体系，正整合进 SONUV / AIOBR / 统一历史归档，不再接受新改动；最新状态见 aiuce.com。_
> **Disposition**: **Migrate → SONUV / AIOBR**
> **处置**：可验证接口/测试将整合进 SONUV 或 AIOBR（运行时/治理能力）；本仓不再作为独立产品维护，源码迁移待目标仓就绪。


# AIUCE Tool Harness

[![Python](https://img.shields.io/badge/Python-2.7%20%7C%203.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/Framework-Tool%20Harness-orange.svg)]()

**Tool registration and invocation framework for AI agents.**

Tool registration, discovery, and sovereign execution framework for AI agents. Classifies tools across three domains (BODY/FLOW/INTEL), routes files intelligently, and enforces sovereignty checks before execution.

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

| Domain | Role | Examples |
|--------|------|----------|
| **BODY** | Execution | tool calls, file I/O, data processing |
| **FLOW** | Coordination | routing, scheduling, orchestration |
| **INTEL** | Reasoning | analysis, decision support, planning |

## License

MIT License — Copyright 2026 Bill Gao
