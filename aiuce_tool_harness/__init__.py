"""
AIUCE Tool Harness — tool registration and invocation framework.

Provides:
- ToolSpec / ToolInvocation: type definitions for tool metadata
- IPIPQClassifier: file classification by extension and keyword
- SmartFileRouter: keyword-driven file routing with rule chaining
- ToolHarnessRegistry: central tool registry with dual-track output
"""

from .types import ToolSpec, ToolInvocation, ToolDomain
from .classifier import IPIPQClassifier
from .router import SmartFileRouter
from .registry import ToolHarnessRegistry

__all__ = [
    "ToolSpec",
    "ToolInvocation",
    "ToolDomain",
    "IPIPQClassifier",
    "SmartFileRouter",
    "ToolHarnessRegistry",
]
__version__ = "0.1.0"
