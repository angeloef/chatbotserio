"""Tests for escalation module — confidence thresholds and clarification messages."""

import pytest
from app.agents.escalation import (
    EscalationLevel,
    assess_confidence,
    build_clarification_message,
    THRESHOLD_EXECUTE,
    THRESHOLD_VERIFY,
    THRESHOLD_CLARIFY,
)


class TestAssessConfidence:
    def test_execute_high_confidence(self):
        level, conf = assess_confidence(0.98)
        assert level == EscalationLevel.EXECUTE
        assert conf == 0.98

    def test_execute_boundary(self):
        level, conf = assess_confidence(0.95)
        assert level == EscalationLevel.EXECUTE

    def test_verify_mid_high(self):
        level, conf = assess_confidence(0.85)
        assert level == EscalationLevel.VERIFY

    def test_verify_boundary(self):
        level, conf = assess_confidence(0.70)
        assert level == EscalationLevel.VERIFY

    def test_verify_just_below_execute(self):
        level, conf = assess_confidence(0.949)
        assert level == EscalationLevel.VERIFY

    def test_clarify_mid(self):
        level, conf = assess_confidence(0.60)
        assert level == EscalationLevel.CLARIFY

    def test_clarify_boundary(self):
        level, conf = assess_confidence(0.50)
        assert level == EscalationLevel.CLARIFY

    def test_handoff_low(self):
        level, conf = assess_confidence(0.30)
        assert level == EscalationLevel.HANDOFF

    def test_handoff_very_low(self):
        level, conf = assess_confidence(0.01)
        assert level == EscalationLevel.HANDOFF

    def test_clamps_above_1(self):
        level, conf = assess_confidence(1.5)
        assert level == EscalationLevel.EXECUTE
        assert conf == 1.0

    def test_clamps_below_0(self):
        level, conf = assess_confidence(-0.5)
        assert level == EscalationLevel.HANDOFF
        assert conf == 0.0


class TestBuildClarificationMessage:
    def test_execute_passes_through(self):
        result = build_clarification_message(EscalationLevel.EXECUTE, "Hola, ¿en qué te ayudo?")
        assert result == "Hola, ¿en qué te ayudo?"

    def test_verify_appends_confirmation(self):
        result = build_clarification_message(EscalationLevel.VERIFY, "Busco departamentos en Centro.")
        assert "¿Entendí bien?" in result
        assert "Busco departamentos en Centro." in result

    def test_verify_no_double_question(self):
        result = build_clarification_message(EscalationLevel.VERIFY, "¿Querés buscar en Centro?")
        assert result == "¿Querés buscar en Centro?"

    def test_clarify_asks_for_details(self):
        result = build_clarification_message(EscalationLevel.CLARIFY, "original text")
        assert "más detalles" in result or "detalles" in result
        # Should mention examples
        assert "alquilar" in result.lower() or "comprar" in result.lower()

    def test_handoff_graceful(self):
        result = build_clarification_message(EscalationLevel.HANDOFF, "original text")
        assert "no estoy seguro" in result.lower() or "Disculpá" in result
        # Should offer alternatives
        assert "Buscar" in result or "Requisitos" in result or "Zonas" in result

    def test_all_levels_return_strings(self):
        for level in EscalationLevel:
            result = build_clarification_message(level, "test")
            assert isinstance(result, str)
            assert len(result) > 0
