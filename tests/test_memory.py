"""Tests for memory tiers — working, episodic, semantic, procedural."""

import pytest
import asyncio
from app.core.belief_state import ConversationBeliefState
from app.memory.working import (
    save_working_memory,
    load_working_memory,
    clear_working_memory,
)
from app.memory.episodic import (
    save_episode,
    get_episodes,
    get_last_episode,
    build_greeting_from_episodes,
)
from app.memory.semantic import get_zone_info, get_zone_comparison
from app.memory.procedural import record_skill_use, get_skill_stats


class TestWorkingMemory:
    @pytest.mark.asyncio
    async def test_save_and_load(self):
        belief = ConversationBeliefState(
            session_id="wm-test-1",
            operation="alquiler",
            property_type="departamento",
            zone="Centro",
            budget_max=100000,
            turn_count=3,
            active_intents={"searching"},
        )
        await save_working_memory(belief)

        loaded = await load_working_memory("wm-test-1")
        assert loaded is not None
        assert loaded.operation == "alquiler"
        assert loaded.zone == "Centro"
        assert loaded.turn_count == 3

        await clear_working_memory("wm-test-1")

    @pytest.mark.asyncio
    async def test_load_nonexistent(self):
        loaded = await load_working_memory("nonexistent-session")
        # Returns None for truly nonexistent sessions
        assert loaded is None or loaded.turn_count == 0

    @pytest.mark.asyncio
    async def test_serialization_roundtrip(self):
        belief = ConversationBeliefState(
            session_id="wm-test-2",
            operation="venta",
            selected_property_id=7,
            history=["hola", "busco casa"],
            active_intents={"searching", "scheduling"},
        )
        await save_working_memory(belief)
        loaded = await load_working_memory("wm-test-2")
        assert loaded.selected_property_id == 7
        assert "searching" in loaded.active_intents
        await clear_working_memory("wm-test-2")


class TestEpisodicMemory:
    @pytest.mark.asyncio
    async def test_save_and_retrieve_episode(self):
        await save_episode(
            phone="549111234",
            session_id="ep-test-1",
            summary="Buscó departamento en alquiler Centro hasta $80K",
            turn_count=4,
            search_criteria={"operación": "alquiler", "tipo": "departamento"},
            properties_viewed=[1, 3],
            last_tool="search_properties",
            intent_outcome="searched_with_results",
        )

        episodes = await get_episodes("549111234", limit=1)
        assert len(episodes) >= 1
        assert "Centro" in episodes[0]["summary"]

    @pytest.mark.asyncio
    async def test_last_episode(self):
        await save_episode(
            phone="549999888",
            session_id="ep-test-last",
            summary="Vio propiedad #5 en Barrio Schuster",
            turn_count=3,
            properties_viewed=[5],
            intent_outcome="viewed_property",
        )
        last = await get_last_episode("549999888")
        assert last is not None
        assert "Schuster" in last["summary"]

    @pytest.mark.asyncio
    async def test_greeting_from_episodes(self):
        await save_episode(
            phone="549555666",
            session_id="ep-greet",
            summary="Buscó departamento alquiler Centro $85000",
            turn_count=2,
            search_criteria={
                "operación": "alquiler",
                "tipo": "departamento",
                "zona": "Centro",
                "presupuesto_máx": "$80,000",
            },
            properties_viewed=[1],
        )
        greeting = await build_greeting_from_episodes("549555666")
        assert "departamento" in greeting.lower() or "Centro" in greeting
        assert "Bienvenido" in greeting

    @pytest.mark.asyncio
    async def test_no_greeting_for_new_user(self):
        greeting = await build_greeting_from_episodes("549000000")
        assert greeting == ""


class TestSemanticMemory:
    @pytest.mark.asyncio
    async def test_get_zone_info_centro(self):
        info = await get_zone_info("Centro")
        assert info is not None
        assert "amenities" in info
        assert info["avg_price_alquiler"] > 0

    @pytest.mark.asyncio
    async def test_get_zone_info_unam(self):
        info = await get_zone_info("UNAM")
        assert "cerca facultad" in info["amenities"] or "estudiantil" in " ".join(info["amenities"])

    @pytest.mark.asyncio
    async def test_zone_comparison(self):
        comp = await get_zone_comparison()
        assert "Centro" in comp
        assert "UNAM" in comp
        assert "Barrio Schuster" in comp
        assert "Ruta 14" in comp

    @pytest.mark.asyncio
    async def test_unknown_zone(self):
        info = await get_zone_info("Marte")
        assert info is None


class TestProceduralMemory:
    @pytest.mark.asyncio
    async def test_record_and_stats(self):
        await record_skill_use("549-proc", "search_properties", True, 200)
        await record_skill_use("549-proc", "get_property_details", True, 150)
        await record_skill_use("549-proc", "search_properties", False, 300)

        stats = await get_skill_stats("549-proc")
        assert "search_properties" in stats
        assert stats["search_properties"]["count"] >= 2
        assert stats["get_property_details"]["count"] >= 1

    @pytest.mark.asyncio
    async def test_no_stats_new_user(self):
        stats = await get_skill_stats("549-new")
        assert stats == {}
