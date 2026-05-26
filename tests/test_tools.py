"""Tests for the tool registry and individual tools."""

import pytest
from app.tools.registry import TOOL_REGISTRY, execute_tool, get_tools_schema
from app.tools.echo_tool import echo
from app.tools.time_tool import get_time
from app.agents.schemas import StructuredToolCall


class TestEchoTool:
    def test_echo_with_text(self):
        result = echo("hola mundo")
        assert result == "Eco: hola mundo"

    def test_echo_empty_uses_default(self):
        result = echo("")
        assert "No especificaste" in result

    def test_echo_registered(self):
        assert "echo" in TOOL_REGISTRY


class TestTimeTool:
    def test_get_time_returns_string(self):
        result = get_time()
        assert isinstance(result, str)
        assert len(result) > 10

    def test_get_time_has_art_timezone(self):
        result = get_time()
        assert "(ART)" in result

    def test_get_time_registered(self):
        assert "get_time" in TOOL_REGISTRY


class TestToolRegistry:
    def test_schema_has_all_tools(self):
        schema = get_tools_schema()
        assert len(schema) == 7
        names = [s["function"]["name"] for s in schema]
        assert "echo" in names
        assert "get_time" in names
        assert "search_properties" in names

    @pytest.mark.asyncio
    async def test_execute_echo(self):
        tc = StructuredToolCall(id="1", name="echo", arguments={"text": "test"})
        result = await execute_tool(tc)
        assert "Eco: test" in result

    @pytest.mark.asyncio
    async def test_execute_get_time(self):
        tc = StructuredToolCall(id="1", name="get_time", arguments={})
        result = await execute_tool(tc)
        assert "(ART)" in result
        assert len(result) > 10

    @pytest.mark.asyncio
    async def test_execute_unknown_tool(self):
        tc = StructuredToolCall(id="1", name="nonexistent", arguments={})
        result = await execute_tool(tc)
        assert "no encontrada" in result.lower() or "Error" in result

    @pytest.mark.asyncio
    async def test_execute_bad_arguments(self):
        tc = StructuredToolCall(id="1", name="echo", arguments={"wrong_param": 123})
        result = await execute_tool(tc)
        # Should get an error about invalid arguments
        assert "Error" in result or "argumentos" in result.lower()


class TestToolSchemas:
    def test_echo_schema_has_required_text(self):
        schema = get_tools_schema()
        echo_s = next(s for s in schema if s["function"]["name"] == "echo")
        assert "text" in echo_s["function"]["parameters"]["properties"]
        assert "text" in echo_s["function"]["parameters"]["required"]

    def test_time_schema_has_no_required_params(self):
        schema = get_tools_schema()
        time_s = next(s for s in schema if s["function"]["name"] == "get_time")
        params = time_s["function"]["parameters"]
        # No required fields for a parameterless tool
        assert params.get("required", []) == [] or "required" not in params
