"""Tests for hidden CoT thinking — must NEVER reach the user."""

import pytest
from app.agents.thinking import think, summarize_thinking

# Thinking is an LLM call — these tests verify the non-LLM parts
# and that the module structure is correct.


class TestThinkingModule:
    def test_summarize_extracts_first_line(self):
        thinking = """El usuario quiere buscar un departamento.
Necesito usar search_properties con filtros de alquiler.
Luego mostraré los resultados."""
        summary = summarize_thinking(thinking)
        assert "quiere buscar" in summary.lower() or "departamento" in summary.lower()

    def test_summarize_empty(self):
        assert summarize_thinking("") == "(no thinking)"

    def test_summarize_strips_formatting(self):
        thinking = "## Análisis\n- Punto 1: buscar\n- Punto 2: filtrar"
        summary = summarize_thinking(thinking)
        # Should not have markdown formatting in first line
        assert not summary.startswith("##")
        assert not summary.startswith("-")

    def test_think_returns_string(self):
        """Verify that think() is properly defined as an async function returning str."""
        import inspect
        assert inspect.iscoroutinefunction(think)
        # Signature check
        sig = inspect.signature(think)
        assert "message" in sig.parameters
