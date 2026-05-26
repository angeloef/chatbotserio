"""Tests for UserPersona — cross-session preference accumulation."""

import pytest
from app.memory.user_model import (
    get_persona,
    update_persona,
    build_personalized_context,
)


class TestPersona:
    @pytest.mark.asyncio
    async def test_new_persona_defaults(self):
        persona = await get_persona("549-persona-new")
        assert persona["phone"] == "549-persona-new"
        assert persona["session_count"] == 0
        assert persona["preferred_zones"] == []

    @pytest.mark.asyncio
    async def test_update_preferences(self):
        # Session 1: search in Centro
        await update_persona("549-persona-1", {
            "session_count": 1,
            "operation": "alquiler",
            "zone": "Centro",
            "property_type": "departamento",
            "budget_max": 80000,
            "properties_viewed": [1],
        })

        persona = await get_persona("549-persona-1")
        assert persona["last_operation"] == "alquiler"
        assert persona["session_count"] >= 1
        zones = persona.get("preferred_zones", [])
        assert any(z.get("name") == "Centro" for z in zones)

    @pytest.mark.asyncio
    async def test_accumulate_across_sessions(self):
        # Session 2: search in UNAM
        await update_persona("549-persona-1", {
            "session_count": 1,
            "zone": "UNAM",
            "property_type": "casa",
        })

        persona = await get_persona("549-persona-1")
        assert persona["session_count"] >= 2
        types = persona.get("preferred_types", [])
        assert any(t.get("name") == "departamento" for t in types)
        assert any(t.get("name") == "casa" for t in types)

    @pytest.mark.asyncio
    async def test_objection_tracking(self):
        await update_persona("549-persona-obj", {
            "session_count": 1,
            "objection": "muy caro",
        })
        await update_persona("549-persona-obj", {
            "session_count": 1,
            "objection": "muy lejos",
        })

        persona = await get_persona("549-persona-obj")
        assert "muy caro" in persona.get("objections", [])
        assert "muy lejos" in persona.get("objections", [])

    @pytest.mark.asyncio
    async def test_budget_moving_average(self):
        await update_persona("549-persona-bud", {
            "session_count": 1,
            "budget_max": 80000,
        })
        await update_persona("549-persona-bud", {
            "session_count": 1,
            "budget_max": 100000,
        })

        persona = await get_persona("549-persona-bud")
        budget = persona.get("budget_range")
        assert budget is not None
        assert 80000 <= budget <= 100000  # Should be around 90000

    @pytest.mark.asyncio
    async def test_context_empty_for_new_user(self):
        ctx = await build_personalized_context("549-new-context")
        assert ctx == ""

    @pytest.mark.asyncio
    async def test_context_includes_preferences(self):
        await update_persona("549-ctx-1", {
            "session_count": 1,
            "operation": "alquiler",
            "zone": "Centro",
            "property_type": "departamento",
            "budget_max": 90000,
        })

        ctx = await build_personalized_context("549-ctx-1")
        assert "Centro" in ctx
        assert "alquiler" in ctx.lower()
