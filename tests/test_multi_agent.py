"""Tests for coordinator intent classification and specialist routing."""

import pytest
from app.agents.coordinator import classify_intent, SPECIALISTS, INTENT_PATTERNS


class TestIntentClassification:
    def test_search_intent_busco(self):
        assert classify_intent("busco departamento en alquiler") == "search"

    def test_search_intent_mostrame(self):
        assert classify_intent("mostrame el 3") == "search"

    def test_search_intent_fotos(self):
        assert classify_intent("fotos del 5") == "search"

    def test_scheduling_intent_agendar(self):
        assert classify_intent("quiero agendar una visita") == "scheduling"

    def test_scheduling_intent_coordinar(self):
        assert classify_intent("cuándo puedo coordinar") == "scheduling"

    def test_scheduling_intent_with_day(self):
        assert classify_intent("el martes a las 11") == "scheduling"

    def test_knowledge_intent_requisitos(self):
        assert classify_intent("qué requisitos necesito") == "knowledge"

    def test_knowledge_intent_zonas(self):
        assert classify_intent("zonas en Oberá") == "knowledge"

    def test_knowledge_intent_garantia(self):
        assert classify_intent("qué garantía piden") == "knowledge"

    def test_negotiator_intent_caro(self):
        assert classify_intent("es muy caro") == "negotiator"

    def test_negotiator_intent_presupuesto(self):
        assert classify_intent("se me va de presupuesto") == "negotiator"

    def test_rapport_intent_hola(self):
        assert classify_intent("hola") == "rapport"

    def test_rapport_intent_gracias(self):
        assert classify_intent("gracias") == "rapport"

    def test_rapport_intent_chau(self):
        assert classify_intent("chau") == "rapport"

    def test_default_fallback(self):
        # Something not matching any pattern defaults to search
        assert classify_intent("xyzzy") == "search"


class TestSpecialists:
    def test_all_five_specialists(self):
        assert len(SPECIALISTS) == 5

    def test_search_has_tools(self):
        s = SPECIALISTS["search"]
        assert "search_properties" in s.tool_names
        assert "get_property_details" in s.tool_names

    def test_scheduling_has_schedule_tool(self):
        s = SPECIALISTS["scheduling"]
        assert "schedule_visit" in s.tool_names

    def test_rapport_has_no_tools(self):
        s = SPECIALISTS["rapport"]
        assert s.tool_names == []

    def test_knowledge_has_faq(self):
        s = SPECIALISTS["knowledge"]
        assert "get_faq_answer" in s.tool_names

    def test_negotiator_has_search(self):
        s = SPECIALISTS["negotiator"]
        assert "search_properties" in s.tool_names


class TestIntentPatterns:
    def test_all_patterns_valid_regex(self):
        import re
        for intent, pattern in INTENT_PATTERNS:
            re.compile(pattern)  # Should not raise
