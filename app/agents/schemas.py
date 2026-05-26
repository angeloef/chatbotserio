"""Agent response and tool call schemas."""

from typing import Any

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """A tool invocation requested by the agent."""

    name: str = Field(..., description="Tool name to invoke")
    arguments: dict[str, Any] = Field(default_factory=dict, description="Tool arguments")


class StructuredToolCall(BaseModel):
    """A structured tool call from the LLM (OpenAI format)."""

    id: str = Field(..., description="Tool call ID")
    name: str = Field(..., description="Function name")
    arguments: dict[str, Any] = Field(default_factory=dict, description="Parsed arguments")


class AgentResponse(BaseModel):
    """Structured response from the agent after processing a message."""

    response: str = Field(..., description="Text response to the user")
    tools_called: list[str] = Field(default_factory=list, description="Names of tools invoked")
    raw_tool_results: list[dict[str, Any]] = Field(
        default_factory=list, description="Raw results from tool executions"
    )
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Agent confidence (0-1)")
    messages: list["MessageChunk"] = Field(default_factory=list, description="Sequential message bubbles for multistep responses")


class MessageChunk(BaseModel):
    """A single message bubble in a multi-message response sequence."""
    text: str = Field(..., description="Text content for this message bubble")
    tool_used: str | None = Field(default=None, description="Tool that produced this chunk, e.g. 'get_property_details'")
    chunk_type: str = Field(default="tool_result", description="'tool_result' | 'closing'")


class ChatRequest(BaseModel):
    """Incoming chat request."""

    message: str = Field(..., min_length=1, description="User message")
    session_id: str = Field(..., description="Session identifier for multi-turn context")
    phone: str = Field(default="", description="User phone for cross-session memory")


class ChatResponse(BaseModel):
    """Response from the /chat endpoint."""

    response: str = Field(..., description="Text response to the user")
    tools_called: list[str] = Field(default_factory=list)
    confidence: float = Field(default=1.0)
    messages: list[MessageChunk] = Field(default_factory=list, description="Additional sequential message bubbles")
