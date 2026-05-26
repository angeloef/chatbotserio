"""Tests for real estate tools — search, details, images, FAQ."""

import pytest
import asyncio
from app.tools.search_properties import search_properties, _describe_filters
from app.tools.get_property_details import get_property_details
from app.tools.get_property_images import get_property_images
from app.tools.get_faq_answer import get_faq_answer, FAQ_ENTRIES
from app.tools.registry import TOOL_REGISTRY, get_tools_schema
from app.agents.schemas import StructuredToolCall


class TestFAQ:
    def test_faq_requisitos(self):
        result = asyncio.run(get_faq_answer("requisitos"))
        assert "DNI" in result
        assert "garantía" in result.lower()

    def test_faq_garantia(self):
        result = asyncio.run(get_faq_answer("garantía"))
        assert "propietaria" in result.lower()

    def test_faq_zonas(self):
        result = asyncio.run(get_faq_answer("zonas"))
        assert "Centro" in result
        assert "UNAM" in result

    def test_faq_fuzzy_match(self):
        result = asyncio.run(get_faq_answer("qué necesito para alquilar"))
        assert "DNI" in result or "requisitos" in result.lower()

    def test_faq_empty_returns_topics(self):
        result = asyncio.run(get_faq_answer(""))
        assert "requisitos" in result.lower()

    def test_faq_unknown_topic(self):
        result = asyncio.run(get_faq_answer("machine learning"))
        assert "no tengo" in result.lower() or "No tengo" in result

    def test_faq_all_entries_exist(self):
        assert len(FAQ_ENTRIES) >= 10


class TestDescribeFilters:
    def test_all_filters(self):
        result = _describe_filters("alquiler", "departamento", "Centro", 100000, 2)
        assert "alquiler" in result
        assert "departamento" in result
        assert "Centro" in result
        assert "100,000" in result
        assert "2+" in result

    def test_no_filters(self):
        assert _describe_filters() == ""

    def test_partial_filters(self):
        result = _describe_filters(operation="alquiler", zona="UNAM")
        assert "alquiler" in result
        assert "UNAM" in result
        assert "departamento" not in result


class TestToolsRegistry:
    def test_all_six_tools_registered(self):
        assert len(TOOL_REGISTRY) == 7  # echo, get_time, search, details, images, faq, schedule_visit

    def test_search_schema_exists(self):
        schema = get_tools_schema()
        names = [s["function"]["name"] for s in schema]
        assert "search_properties" in names
        assert "get_property_details" in names
        assert "get_property_images" in names
        assert "get_faq_answer" in names

    def test_search_schema_has_required_params(self):
        schema = get_tools_schema()
        s = next(s for s in schema if s["function"]["name"] == "search_properties")
        # All params are optional in search_properties
        props = s["function"]["parameters"]["properties"]
        assert "operation" in props
        assert "tipo" in props
        assert "zona" in props
        assert "presupuesto_max" in props
        assert "dormitorios" in props


class TestToolExecution:
    @pytest.mark.asyncio
    async def test_execute_faq(self):
        from app.tools.registry import execute_tool
        tc = StructuredToolCall(id="1", name="get_faq_answer", arguments={"pregunta": "requisitos"})
        result = await execute_tool(tc)
        assert "DNI" in result

    def test_execute_faq_sync_echo_still_works(self):
        from app.tools.registry import execute_tool
        import asyncio
        tc = StructuredToolCall(id="1", name="echo", arguments={"text": "hola"})
        result = asyncio.run(execute_tool(tc))
        assert "Eco: hola" in result
