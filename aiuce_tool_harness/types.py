"""
Type definitions for the tool harness system.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid


class ToolDomain(Enum):
    """Tool domain classification from the three-domain system"""
    BODY = "body"      # Execution domain: operations, tool calls, file processing
    FLOW = "flow"      # Flow domain: routing, scheduling, coordination
    INTEL = "intel"    # Intelligence domain: analysis, reasoning, decision


@dataclass
class ToolSpec:
    """
    Tool specification - tool description protocol for registry.
    Every tool registered must declare its specification.
    """

    id: str
    name: str
    domain: ToolDomain
    layer: str  # L0-L10
    description: str
    cmd_template: str  # CLI command template
    constitutional_alignment: List[str] = field(default_factory=list)
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_mode: str = "dual"  # "json" | "markdown" | "dual"
    retry_on_failure: bool = True
    max_retries: int = 3
    timeout_seconds: int = 30
    tags: List[str] = field(default_factory=list)


@dataclass
class ToolInvocation:
    """Tool invocation record"""
    invocation_id: str
    tool_id: str
    params: Dict[str, Any]
    status: str  # pending | running | success | failed | timeout
    started_at: str
    completed_at: Optional[str] = None
    output: Optional[str] = None
    error: Optional[str] = None
    audit_id: Optional[str] = None
    sovereignty_passed: bool = True