"""Tests for replan logic — tool failure triggers replan mid-loop."""

from app.agents.observer import Observation
from app.agents.evaluator import evaluate, build_replan_context


class TestReplan:
    def test_search_no_results_triggers_replan(self):
        """When search returns 0 results, evaluator should recommend replanning."""
        observations = [
            Observation(tool_name="search_properties", success=True, result_count=0, anomaly=True,
                       anomaly_detail="No results found"),
        ]
        ev = evaluate(observations, 1)
        assert ev.should_replan
        assert "broaden" in ev.replan_reason.lower() or "search" in ev.replan_reason.lower()

    def test_replan_context_suggests_broader_search(self):
        observations = [
            Observation(tool_name="search_properties", success=True, result_count=0, anomaly=True),
        ]
        ev = evaluate(observations, 1)
        ctx = build_replan_context(ev)
        assert "REPLANIFICACIÓN" in ctx or "Ampliar" in ctx or "ajustar" in ctx.lower()

    def test_multiple_failures(self):
        observations = [
            Observation(tool_name="search_properties", success=False, anomaly=True),
            Observation(tool_name="get_property_details", success=False, anomaly=True),
        ]
        ev = evaluate(observations, 2)
        assert ev.should_replan

    def test_partial_success_no_replan(self):
        """FAQ-only messages should succeed without replan."""
        observations = [
            Observation(tool_name="get_faq_answer", success=True),
        ]
        ev = evaluate(observations, 1)
        assert ev.success
        assert not ev.should_replan

    def test_details_failure_triggers_replan(self):
        observations = [
            Observation(tool_name="get_property_details", success=False, anomaly=True,
                       anomaly_detail="Property not found"),
        ]
        ev = evaluate(observations, 1)
        assert ev.should_replan

    def test_replan_for_too_many_results_does_not_trigger(self):
        """Lots of results is NOT a replan trigger (it's a good thing)."""
        observations = [
            Observation(tool_name="search_properties", success=True, result_count=15, result_ids=list(range(1, 16))),
        ]
        ev = evaluate(observations, 1)
        assert ev.success
