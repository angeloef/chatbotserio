"""Tests for the agent schemas (no LLM required)."""

import pytest
from pydantic import ValidationError
from app.agents.schemas import (
    AgentResponse,
    ChatRequest,
    ChatResponse,
    StructuredToolCall,
    ToolCall,
)


class TestSchemas:
    def test_chat_request_valid(self):
        req = ChatRequest(message="hola", session_id="test-1")
        assert req.message == "hola"
        assert req.session_id == "test-1"

    def test_chat_request_empty_message_rejected(self):
        with pytest.raises(ValidationError):
            ChatRequest(message="", session_id="test-1")

    def test_chat_response_serializes(self):
        resp = ChatResponse(response="Hola!", tools_called=["echo"], confidence=0.95)
        data = resp.model_dump()
        assert data["response"] == "Hola!"
        assert data["tools_called"] == ["echo"]
        assert data["confidence"] == 0.95

    def test_agent_response_defaults(self):
        resp = AgentResponse(response="ok")
        assert resp.tools_called == []
        assert resp.raw_tool_results == []
        assert resp.confidence == 1.0

    def test_agent_response_confidence_bounds(self):
        with pytest.raises(ValidationError):
            AgentResponse(response="x", confidence=1.5)

        with pytest.raises(ValidationError):
            AgentResponse(response="x", confidence=-0.1)

    def test_tool_call_schema(self):
        tc = ToolCall(name="echo", arguments={"text": "hola"})
        assert tc.name == "echo"
        assert tc.arguments == {"text": "hola"}

    def test_structured_tool_call_schema(self):
        stc = StructuredToolCall(
            id="call_123",
            name="get_time",
            arguments={},
        )
        assert stc.id == "call_123"
        assert stc.name == "get_time"
