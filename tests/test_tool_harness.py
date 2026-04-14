"""Tests for aiuce-tool-harness."""

import pytest
from aiuce_tool_harness import (
    ToolSpec, ToolInvocation, ToolDomain,
    IPIPQClassifier, SmartFileRouter, ToolHarnessRegistry,
)


class TestIPIPQClassifier:
    def test_classify_image_by_extension(self):
        result = IPIPQClassifier.classify_file("/home/user/photo.jpg")
        assert result["json"]["category"] in ("image", "review")

    def test_classify_document_by_extension(self):
        result = IPIPQClassifier.classify_file("/home/user/report.pdf")
        assert result["json"]["category"] == "document"

    def test_classify_by_keyword(self):
        # "medical" keyword triggers medical category even for .pdf
        result = IPIPQClassifier.classify_file("/home/user/patient_medical_record.pdf")
        assert result["json"]["category"] == "medical"

    def test_classify_uncategorized(self):
        result = IPIPQClassifier.classify_file("/home/user/xyz.abc123")
        assert result["json"]["category"] == "uncategorized"

    def test_classify_code(self):
        result = IPIPQClassifier.classify_file("/home/user/main.py")
        assert result["json"]["category"] == "code"

    def test_dual_output_format(self):
        result = IPIPQClassifier.classify_file("/home/user/test.csv")
        assert "json" in result
        assert "markdown" in result


class TestSmartFileRouter:
    def test_routes_medical(self):
        router = SmartFileRouter()
        result = router.classify("medical report from hospital")
        assert "Medical" in result["target"]

    def test_routes_business(self):
        router = SmartFileRouter()
        result = router.classify("client contract and invoice")
        assert "Business" in result["target"]

    def test_default_inbox(self):
        router = SmartFileRouter()
        result = router.classify("random text with no keywords")
        assert result["target"] == "DATA/INBOX/"

    def test_priority_scoring(self):
        router = SmartFileRouter()
        result = router.classify("medical diagnosis health prescription")
        assert result["confidence"] > 0.5

    def test_custom_rules(self):
        custom = [{"keywords": ["secret"], "target": "VAULT/", "priority": 20}]
        router = SmartFileRouter(custom_rules=custom)
        result = router.classify("secret project plan")
        assert result["target"] == "VAULT/"


class TestToolHarnessRegistry:
    def test_register_and_list(self):
        reg = ToolHarnessRegistry()
        spec = ToolSpec(
            id="test-tool", name="Test Tool",
            domain=ToolDomain.BODY, layer="L9",
            description="A test tool", cmd_template="echo hello",
        )
        reg.register(spec)
        tools = reg.list_tools()
        assert len(tools) == 1
        assert tools[0]["name"] == "Test Tool"

    def test_invoke_unknown_tool(self):
        reg = ToolHarnessRegistry()
        result = reg.invoke("nonexistent")
        assert "error" in result["json"]

    def test_invoke_with_handler(self):
        reg = ToolHarnessRegistry()
        spec = ToolSpec(
            id="echo", name="Echo",
            domain=ToolDomain.INTEL, layer="L9",
            description="Echo back", cmd_template="echo",
        )
        reg.register(spec, handler=lambda p: {
            "json": {"echo": p}, "markdown": f"Echo: {p}"
        })
        result = reg.invoke("echo", {"msg": "hello"})
        assert result["json"]["echo"]["msg"] == "hello"

    def test_invoke_without_handler(self):
        reg = ToolHarnessRegistry()
        spec = ToolSpec(
            id="doc-only", name="Doc Only",
            domain=ToolDomain.FLOW, layer="L9",
            description="No handler", cmd_template="none",
        )
        reg.register(spec)
        result = reg.invoke("doc-only", {"key": "val"})
        assert "markdown" in result
        assert "Doc Only" in result["markdown"]

    def test_get_invocation_history(self):
        reg = ToolHarnessRegistry()
        spec = ToolSpec(
            id="hist", name="History Test",
            domain=ToolDomain.BODY, layer="L9",
            description="Test", cmd_template="test",
        )
        reg.register(spec)
        reg.invoke("hist")
        history = reg.get_invocation_history("hist")
        assert len(history) == 1
        assert history[0]["status"] == "success"
