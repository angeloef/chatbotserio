"""Tests for Phase 5: belief state, guards, state transitioner, context aggregator."""

import pytest
from app.core.belief_state import (
    ConversationBeliefState,
    get_belief,
    save_belief,
    clear_session,
)
from app.core.guard_functions import (
    ALL_GUARDS,
    can_greet,
    can_search,
    can_search_with_partial,
    can_view_details,
    can_view_photos,
    can_schedule,
    can_ask_faq,
    can_confirm,
    needs_clarify_operation,
    needs_clarify_type,
    needs_clarify_zone,
    needs_clarify_budget,
    should_handoff,
)
from app.core.state_transitioner import update_belief
from app.core.context_aggregator import build_context_prompt


# ── Belief State Basics ───────────────────────────────────────


class TestBeliefState:
    def test_new_belief_empty(self):
        b = ConversationBeliefState(session_id="test")
        assert b.search_criteria_count == 0
        assert b.operation is None
        assert b.property_type is None
        assert b.zone is None
        assert b.budget_max is None
        assert b.selected_property_id is None
        assert b.active_intents == set()
        assert b.is_first_turn

    def test_search_criteria_count(self):
        b = ConversationBeliefState(session_id="test")
        assert b.search_criteria_count == 0
        b.operation = "alquiler"
        assert b.search_criteria_count == 1
        b.property_type = "departamento"
        assert b.search_criteria_count == 2
        b.zone = "Centro"
        assert b.search_criteria_count == 3
        b.budget_max = 100000
        assert b.search_criteria_count == 4

    def test_search_criteria_dict(self):
        b = ConversationBeliefState(
            session_id="test", operation="alquiler", zone="Centro", budget_max=85000
        )
        d = b.search_criteria
        assert d["operación"] == "alquiler"
        assert d["zona"] == "Centro"
        assert "presupuesto_máx" in d

    def test_has_selection(self):
        b = ConversationBeliefState(session_id="test")
        assert not b.has_selection
        b.selected_property_id = 5
        assert b.has_selection

    def test_session_store(self):
        clear_session("test-store")
        b = get_belief("test-store")
        assert b.session_id == "test-store"
        b.operation = "venta"
        save_belief(b)
        b2 = get_belief("test-store")
        assert b2.operation == "venta"


# ── State Transitioner ────────────────────────────────────────


class TestStateTransitioner:
    def test_extract_operation(self):
        b = ConversationBeliefState(session_id="t")
        update_belief(b, "busco alquilar departamento")
        assert b.operation == "alquiler"

    def test_extract_type(self):
        b = ConversationBeliefState(session_id="t")
        update_belief(b, "busco departamento en venta")
        assert b.property_type == "departamento"

    def test_extract_casa(self):
        b = ConversationBeliefState(session_id="t")
        update_belief(b, "quiero comprar una casa")
        assert b.property_type == "casa"
        assert b.operation == "venta"

    def test_extract_zone(self):
        b = ConversationBeliefState(session_id="t")
        update_belief(b, "busco en Centro")
        assert b.zone == "Centro"

    def test_extract_zone_unam(self):
        b = ConversationBeliefState(session_id="t")
        update_belief(b, "algo cerca de la universidad")
        assert b.zone == "UNAM"

    def test_extract_budget_mil(self):
        b = ConversationBeliefState(session_id="t")
        update_belief(b, "hasta 80 mil pesos")
        assert b.budget_max == 80_000

    def test_extract_budget_lucas(self):
        b = ConversationBeliefState(session_id="t")
        update_belief(b, "presupuesto de 100 lucas")
        assert b.budget_max == 100_000

    def test_extract_bedrooms(self):
        b = ConversationBeliefState(session_id="t")
        update_belief(b, "necesito 2 dormitorios")
        assert b.bedrooms_min == 2

    def test_extract_intents(self):
        b = ConversationBeliefState(session_id="t")
        update_belief(b, "quiero agendar una visita")
        assert "scheduling" in b.active_intents
        assert "searching" in b.active_intents  # "quiero" triggers searching too

    def test_extract_selection(self):
        b = ConversationBeliefState(session_id="t")
        update_belief(b, "mostrame el 3")
        assert b.selected_property_id == 3

    def test_turn_count_increments(self):
        b = ConversationBeliefState(session_id="t")
        assert b.turn_count == 0
        update_belief(b, "hola")
        assert b.turn_count == 1
        update_belief(b, "busco depto")
        assert b.turn_count == 2

    def test_first_mention_wins(self):
        """First extracted value for a field should persist."""
        b = ConversationBeliefState(session_id="t")
        update_belief(b, "busco departamento en Centro")  # type=departamento, zone=Centro
        assert b.property_type == "departamento"
        assert b.zone == "Centro"
        # Next message changes zone — should NOT overwrite
        update_belief(b, "mejor en UNAM")
        assert b.property_type == "departamento"  # unchanged
        assert b.zone == "Centro"  # first mention wins

    def test_multi_turn_accumulation(self):
        """Full 4-turn scenario from the roadmap."""
        b = ConversationBeliefState(session_id="multi")

        # Turn 1: type + operation + zone
        update_belief(b, "busco depto alquiler Oberá centro")
        assert b.operation == "alquiler"
        assert b.property_type == "departamento"
        assert b.zone == "Centro"
        assert b.search_criteria_count == 3

        # Turn 2: budget (accumulated)
        update_belief(b, "hasta 80 lucas")
        assert b.budget_max == 80_000
        assert b.search_criteria_count == 4
        assert can_search(b)

        # Turn 3: selection
        update_belief(b, "mostrame el 5")
        assert b.selected_property_id == 5
        assert can_view_details(b)

        # Turn 4: scheduling
        update_belief(b, "quiero agendar visita")
        assert "scheduling" in b.active_intents
        assert can_schedule(b)


# ── Guard Functions ───────────────────────────────────────────


class TestGuards:
    def test_can_greet_always(self):
        assert can_greet(ConversationBeliefState(session_id="t"))

    def test_can_search_full_criteria(self):
        b = ConversationBeliefState(
            session_id="t",
            operation="alquiler",
            property_type="departamento",
            zone="Centro",
            budget_max=100000,
        )
        assert can_search(b)

    def test_can_search_with_intent(self):
        b = ConversationBeliefState(session_id="t", active_intents={"searching"})
        assert can_search(b)
        assert can_search_with_partial(b)

    def test_cannot_search_empty(self):
        b = ConversationBeliefState(session_id="t")
        assert not can_search(b)

    def test_can_view_details_with_selection(self):
        b = ConversationBeliefState(session_id="t", selected_property_id=3)
        assert can_view_details(b)

    def test_cannot_view_details_no_selection(self):
        assert not can_view_details(ConversationBeliefState(session_id="t"))

    def test_can_schedule_full(self):
        b = ConversationBeliefState(
            session_id="t",
            selected_property_id=3,
            active_intents={"scheduling"},
        )
        assert can_schedule(b)

    def test_cannot_schedule_no_selection(self):
        b = ConversationBeliefState(
            session_id="t", active_intents={"scheduling"}
        )
        assert not can_schedule(b)

    def test_needs_clarify_operation(self):
        b = ConversationBeliefState(
            session_id="t", active_intents={"searching"}
        )
        assert needs_clarify_operation(b)

    def test_no_clarify_when_operation_set(self):
        b = ConversationBeliefState(
            session_id="t",
            operation="alquiler",
            active_intents={"searching"},
        )
        assert not needs_clarify_operation(b)

    def test_should_handoff_after_many_turns(self):
        b = ConversationBeliefState(session_id="t", turn_count=6)
        assert should_handoff(b)

    def test_no_handoff_with_criteria(self):
        b = ConversationBeliefState(
            session_id="t", turn_count=6, operation="alquiler"
        )
        assert not should_handoff(b)

    def test_all_guards_registered(self):
        assert len(ALL_GUARDS) == 13
        for name, guard in ALL_GUARDS.items():
            assert callable(guard), f"{name} is not callable"


# ── Context Aggregator ────────────────────────────────────────


class TestContextAggregator:
    def test_empty_on_first_turn(self):
        b = ConversationBeliefState(session_id="t", turn_count=1)
        assert build_context_prompt(b) == ""

    def test_includes_criteria(self):
        b = ConversationBeliefState(
            session_id="t",
            turn_count=2,
            operation="alquiler",
            property_type="departamento",
            zone="Centro",
            budget_max=100000,
            active_intents={"searching"},
        )
        prompt = build_context_prompt(b)
        assert "Criterios de búsqueda" in prompt
        assert "alquiler" in prompt
        assert "departamento" in prompt
        assert "Centro" in prompt
        assert "100,000" in prompt

    def test_suggests_search_when_ready(self):
        b = ConversationBeliefState(
            session_id="t",
            turn_count=3,
            operation="alquiler",
            property_type="departamento",
            zone="Centro",
            budget_max=100000,
            active_intents={"searching"},
        )
        prompt = build_context_prompt(b)
        # Guard-based guidance was moved to system prompt (Phase 10 fix).
        # Context aggregator now only reports what's accumulated —
        # all 4 criteria filled + searching intent means the system
        # prompt will handle suggesting the search.
        assert "Criterios completados: 4/4" in prompt
        assert "searching" in prompt

    def test_suggests_clarify_operation(self):
        b = ConversationBeliefState(
            session_id="t",
            turn_count=2,
            property_type="departamento",
            zone="Centro",
            active_intents={"searching"},
        )
        prompt = build_context_prompt(b)
        assert "alquiler" in prompt.lower() or "venta" in prompt.lower()

    def test_includes_selection(self):
        b = ConversationBeliefState(
            session_id="t", turn_count=3, selected_property_id=7
        )
        prompt = build_context_prompt(b)
        assert "ID 7" in prompt or "propiedad" in prompt
