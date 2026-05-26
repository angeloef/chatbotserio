"""Tests for MCP JSON-RPC 2.0 server."""

import json
import pytest
from app.skills.mcp_server import handle_mcp_request, handle_mcp_request_raw


class TestMCPInitialize:
    def test_initialize(self):
        response = handle_mcp_request({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2024-11-05"},
        })
        result = response.result
        assert result["protocolVersion"] == "2024-11-05"
        assert "tools" in result["capabilities"]
        assert result["serverInfo"]["name"] == "ChatbotSerio"

    def test_initialize_has_id(self):
        response = handle_mcp_request({
            "jsonrpc": "2.0",
            "id": 42,
            "method": "initialize",
            "params": {},
        })
        assert response.id == 42


class TestMCPToolsList:
    def test_tools_list(self):
        response = handle_mcp_request({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
        })
        tools = response.result["tools"]
        assert len(tools) == 6
        names = [t["name"] for t in tools]
        assert "search_properties" in names
        assert "get_property_details" in names
        assert "schedule_visit" in names

    def test_tools_list_has_schema(self):
        response = handle_mcp_request({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/list",
        })
        for tool in response.result["tools"]:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool


class TestMCPToolsCall:
    def test_call_faq(self):
        response = handle_mcp_request({
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "get_faq_answer",
                "arguments": {"pregunta": "requisitos"},
            },
        })
        content = response.result["content"]
        assert len(content) == 1
        assert content[0]["type"] == "text"
        assert "DNI" in content[0]["text"]

    def test_call_schedule(self):
        response = handle_mcp_request({
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "schedule_visit",
                "arguments": {
                    "property_id": "5",
                    "nombre": "Juan",
                    "telefono": "3755-123456",
                    "dia": "martes",
                    "horario": "11:00",
                },
            },
        })
        content = response.result["content"]
        assert "Juan" in content[0]["text"]
        assert "5" in content[0]["text"]

    def test_call_unknown_tool(self):
        response = handle_mcp_request({
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "nonexistent_tool",
                "arguments": {},
            },
        })
        assert "Error" in response.result["content"][0]["text"]


class TestMCPErrors:
    def test_unknown_method(self):
        response = handle_mcp_request({
            "jsonrpc": "2.0",
            "id": 7,
            "method": "nonexistent",
        })
        assert response.error is not None
        assert response.error["code"] == -32601

    def test_parse_error(self):
        result = handle_mcp_request_raw("not valid json")
        data = json.loads(result)
        assert data["error"]["code"] == -32700

    def test_valid_json_rpc(self):
        result = handle_mcp_request_raw(
            '{"jsonrpc":"2.0","id":8,"method":"initialize","params":{}}'
        )
        data = json.loads(result)
        assert data["id"] == 8
        assert "result" in data


class TestMCPResponseFormat:
    def test_response_has_jsonrpc(self):
        response = handle_mcp_request({
            "jsonrpc": "2.0",
            "id": 9,
            "method": "tools/list",
        })
        d = response.to_dict()
        assert d["jsonrpc"] == "2.0"

    def test_error_has_no_result(self):
        response = handle_mcp_request({
            "jsonrpc": "2.0",
            "id": 10,
            "method": "nonexistent",
        })
        d = response.to_dict()
        assert "result" not in d
        assert "error" in d
