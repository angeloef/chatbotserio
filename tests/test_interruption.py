"""Tests for interruption handling and topic switching."""

import pytest
from app.agents.conversation_manager import (
    save_specialist_state,
    get_saved_state,
    clear_saved_state,
    detect_topic_switch,
    build_interruption_prompt,
    ConversationSnapshot,
)


class TestTopicSwitch:
    def test_same_specialist_no_switch(self):
        assert not detect_topic_switch("search", "search")

    def test_natural_transition_search_to_scheduling(self):
        assert not detect_topic_switch("search", "scheduling")

    def test_natural_transition_rapport_to_search(self):
        assert not detect_topic_switch("rapport", "search")

    def test_forced_switch_scheduling_to_negotiator(self):
        # Scheduling → Negotiator is NOT a natural transition
        assert detect_topic_switch("scheduling", "negotiator")

    def test_forced_switch_knowledge_to_scheduling(self):
        assert detect_topic_switch("knowledge", "scheduling")


class TestInterruptionPrompt:
    def test_builds_prompt(self):
        prompt = build_interruption_prompt("scheduling", "negotiator")
        assert "agendamiento" in prompt.lower()
        assert "negociación" in prompt.lower()
        assert "¿Seguimos" in prompt or "volver" in prompt.lower()


class TestSnapshotStore:
    def test_save_and_retrieve(self):
        clear_saved_state("snap-test")
        save_specialist_state("snap-test", "scheduling", {"step": "collecting_info"})

        snap = get_saved_state("snap-test")
        assert snap is not None
        assert snap.active_specialist == "scheduling"
        assert snap.specialist_state == {"step": "collecting_info"}

    def test_clear(self):
        save_specialist_state("snap-clear", "search", {})
        assert get_saved_state("snap-clear") is not None
        clear_saved_state("snap-clear")
        assert get_saved_state("snap-clear") is None

    def test_not_found(self):
        clear_saved_state("snap-nope")
        assert get_saved_state("snap-nope") is None
