"""
ToolHarnessRegistry — tool registration and invocation system.

Design:
- Tools register with a ToolSpec declaration
- Every invocation is audited (optional audit logger)
- Dual-track output: JSON for AI, Markdown for humans
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import uuid

from .types import ToolSpec, ToolInvocation, ToolDomain


class ToolHarnessRegistry:
    """
    Central registry for AI agent tools.

    Tools declare their specification (ToolSpec) on registration.
    Every invocation produces a ToolInvocation record with audit trail.
    """

    def __init__(self, audit_logger=None, sovereignty_checker=None):
        self._tools: Dict[str, ToolSpec] = {}
        self._handlers: Dict[str, Callable] = {}
        self._invocations: List[ToolInvocation] = []
        self.audit_logger = audit_logger
        self.sovereignty_checker = sovereignty_checker

    def register(
        self,
        spec: ToolSpec,
        handler: Optional[Callable] = None,
    ) -> None:
        """
        Register a tool with its specification and optional handler.

        Args:
            spec: Tool specification defining the tool's capabilities.
            handler: Optional callable to invoke the tool. If None,
                     the tool is registered for documentation only.
        """
        if self.sovereignty_checker:
            check = self.sovereignty_checker(spec.description)
            if getattr(check, "vetoed", False):
                raise ValueError(
                    f"Tool '{spec.name}' rejected by sovereignty check: "
                    f"{getattr(check, 'reason', 'unknown')}"
                )

        self._tools[spec.id] = spec
        if handler is not None:
            self._handlers[spec.id] = handler

    def invoke(
        self,
        tool_id: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Invoke a registered tool.

        Returns:
            Dict with 'json' (for AI) and 'markdown' (for humans) keys.
        """
        if tool_id not in self._tools:
            return {
                "json": {"error": f"Tool '{tool_id}' not registered"},
                "markdown": f"⚠️ Tool `{tool_id}` not found in registry.",
            }

        spec = self._tools[tool_id]
        params = params or {}
        invocation = ToolInvocation(
            invocation_id=str(uuid.uuid4())[:8],
            tool_id=tool_id,
            params=params,
            status="running",
            started_at=datetime.now().isoformat(),
            sovereignty_passed=True,
        )

        try:
            handler = self._handlers.get(tool_id)
            if handler is None:
                result = self._format_output(spec, params)
            else:
                result = handler(params)
                if not isinstance(result, dict) or "json" not in result:
                    result = self._format_output(spec, params, result)

            invocation.status = "success"
            invocation.output = result.get("markdown", "")
            invocation.completed_at = datetime.now().isoformat()

            if self.audit_logger:
                self.audit_logger.log({
                    "tool_id": tool_id,
                    "status": "success",
                    "domain": spec.domain.value,
                    "timestamp": invocation.completed_at,
                })

            return result

        except Exception as e:
            invocation.status = "failed"
            invocation.error = str(e)
            invocation.completed_at = datetime.now().isoformat()

            return {
                "json": {"error": str(e), "tool_id": tool_id},
                "markdown": f"⚠️ Tool `{spec.name}` failed: {e}",
            }
        finally:
            self._invocations.append(invocation)

    def _format_output(
        self,
        spec: ToolSpec,
        params: Dict[str, Any],
        raw_result: Any = None,
    ) -> Dict[str, Any]:
        """Format tool output in dual-track format."""
        json_output = {
            "tool": spec.name,
            "domain": spec.domain.value,
            "params": params,
        }
        if raw_result is not None:
            json_output["result"] = raw_result

        md_output = (
            f"### 🛠️ {spec.name}\n\n"
            f"**Domain:** {spec.domain.value}\n\n"
            f"{spec.description}\n"
        )

        return {"json": json_output, "markdown": md_output}

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all registered tools."""
        return [
            {
                "id": spec.id,
                "name": spec.name,
                "domain": spec.domain.value,
                "description": spec.description,
            }
            for spec in self._tools.values()
        ]

    def get_tool(self, tool_id: str) -> Optional[ToolSpec]:
        """Get a tool spec by ID."""
        return self._tools.get(tool_id)

    def get_invocation_history(
        self,
        tool_id: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Get recent invocation records."""
        records = self._invocations
        if tool_id:
            records = [r for r in records if r.tool_id == tool_id]
        return [
            {
                "invocation_id": r.invocation_id,
                "tool_id": r.tool_id,
                "status": r.status,
                "started_at": r.started_at,
                "error": r.error,
            }
            for r in records[-limit:]
        ]
