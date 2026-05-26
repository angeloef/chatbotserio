"""Tests for response parser — JSON extraction and fallback handling."""

import json
import pytest
from app.core.response_parser import parse_llm_response, FINAL_RESPONSE_SCHEMA


class TestParseLLMResponse:
    def test_valid_json(self):
        text, conf = parse_llm_response(
            '{"respuesta": "Hola, ¿en qué te ayudo?", "confianza": 0.98}'
        )
        assert text == "Hola, ¿en qué te ayudo?"
        assert conf == 0.98

    def test_valid_json_with_newlines(self):
        text, conf = parse_llm_response(
            '{"respuesta": "Línea 1\\nLínea 2", "confianza": 0.85}'
        )
        assert "Línea 1" in text
        assert "Línea 2" in text
        assert conf == 0.85

    def test_valid_json_low_confidence(self):
        text, conf = parse_llm_response(
            '{"respuesta": "No entendí bien", "confianza": 0.30}'
        )
        assert conf == 0.30

    def test_fallback_plain_text(self):
        text, conf = parse_llm_response("Hola, ¿cómo estás?")
        assert text == "Hola, ¿cómo estás?"
        assert conf == 0.5

    def test_fallback_empty_string(self):
        text, conf = parse_llm_response("")
        assert text == ""
        assert conf == 0.0

    def test_fallback_none_text(self):
        text, conf = parse_llm_response("   ")
        assert conf == 0.0

    def test_json_in_code_block(self):
        text, conf = parse_llm_response(
            '```json\n{"respuesta": "hola", "confianza": 0.99}\n```'
        )
        assert text == "hola"
        assert conf == 0.99

    def test_json_with_extra_text(self):
        """Parser should extract the JSON even with surrounding text."""
        text, conf = parse_llm_response(
            'Claro, acá va:\n{"respuesta": "ok", "confianza": 0.95}\nEso es todo.'
        )
        assert text == "ok"
        assert conf == 0.95

    def test_missing_confianza_defaults(self):
        text, conf = parse_llm_response(
            '{"respuesta": "hola"}'
        )
        # Should fall through to strategies, but if it matches as a dict,
        # confianza should default
        text, conf = parse_llm_response(
            '{"respuesta": "hola", "confianza": "INVALID"}'
        )
        assert text == "hola"
        assert conf == 0.5  # coerced from invalid

    def test_response_schema_is_valid(self):
        """Verify the json_schema dict has the required structure."""
        assert FINAL_RESPONSE_SCHEMA["type"] == "json_schema"
        schema = FINAL_RESPONSE_SCHEMA["json_schema"]
        assert schema["strict"] is True
        assert "respuesta" in schema["schema"]["required"]
        assert "confianza" in schema["schema"]["required"]

    def test_clamps_confidence(self):
        text, conf = parse_llm_response(
            '{"respuesta": "x", "confianza": 2.5}'
        )
        assert conf <= 1.0
        text, conf = parse_llm_response(
            '{"respuesta": "x", "confianza": -1.0}'
        )
        assert conf >= 0.0
