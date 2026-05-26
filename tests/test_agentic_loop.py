"""Tests for agentic loop components — thinking, planner, observer, evaluator."""

import pytest
from app.agents.planner import build_plan, PlanStep, ExecutionPlan
from app.agents.observer import observe, build_observation_report, Observation
from app.agents.evaluator import evaluate, build_replan_context, _build_success_summary


class TestPlanner:
    def test_build_search_plan(self):
        thinking = "El usuario quiere buscar departamentos en alquiler. Necesito usar search_properties para encontrar opciones."
        plan = build_plan(thinking, ["search_properties", "get_property_details"])
        assert len(plan.steps) == 1
        assert plan.steps[0].tool_name == "search_properties"

    def test_build_search_then_details(self):
        thinking = "Primero busco propiedades con search_properties. Luego muestro detalles con get_property_details si el usuario pide."
        plan = build_plan(thinking, ["search_properties", "get_property_details", "get_property_images"])
        assert len(plan.steps) >= 1
        names = [s.tool_name for s in plan.steps]
        assert "search_properties" in names

    def test_plan_with_dependencies(self):
        thinking = "Buscar propiedades, luego mostrar detalles y fotos."
        plan = build_plan(thinking, ["search_properties", "get_property_details", "get_property_images"])
        for step in plan.steps:
            if step.tool_name == "get_property_details":
                assert step.depends_on == "search_properties"

    def test_empty_plan_for_no_tools(self):
        thinking = "Solo un saludo, no necesito herramientas."
        plan = build_plan(thinking, [])
        assert len(plan.steps) == 0

    def test_plan_has_fallback(self):
        plan = build_plan("buscar propiedades", ["search_properties"])
        assert plan.fallback

    def test_max_three_steps(self):
        thinking = "buscar search detalles detail fotos photo image faq agendar schedule"
        plan = build_plan(thinking, [
            "search_properties", "get_property_details", "get_property_images",
            "get_faq_answer", "schedule_visit",
        ])
        assert len(plan.steps) <= 3


class TestObserver:
    def test_observe_search_with_results(self):
        obs = observe("search_properties", "Encontré 5 propiedades:\n[1] Depto A\n[2] Depto B\n[3] Depto C")
        assert obs.success
        assert obs.result_count == 5
        assert obs.result_ids == [1, 2, 3]

    def test_observe_search_no_results(self):
        obs = observe("search_properties", "No encontré propiedades para alquiler en Centro.")
        assert obs.success  # Tool didn't error
        assert obs.anomaly  # But empty results is anomalous
        assert "No results" in obs.anomaly_detail or "no encontré" in obs.anomaly_detail.lower()

    def test_observe_error(self):
        obs = observe("get_property_details", "Error: herramienta 'xyz' no encontrada")
        assert not obs.success
        assert obs.anomaly

    def test_observe_faq(self):
        obs = observe("get_faq_answer", "Para alquilar necesitás:\n• DNI\n• Recibo de sueldo")
        assert obs.success
        assert obs.result_count == 0  # FAQ doesn't have counts

    def test_build_observation_report(self):
        observations = [
            Observation(tool_name="search_properties", success=True, result_count=3, result_ids=[1, 2, 3]),
            Observation(tool_name="get_property_details", success=True),
        ]
        report = build_observation_report(observations)
        assert "search_properties" in report
        assert "3 resultados" in report

    def test_empty_observation_report(self):
        report = build_observation_report([])
        assert "No tool calls" in report


class TestEvaluator:
    def test_evaluate_success(self):
        observations = [
            Observation(tool_name="search_properties", success=True, result_count=3, result_ids=[1, 3, 5]),
        ]
        ev = evaluate(observations, 1)
        assert ev.success
        assert not ev.should_replan

    def test_evaluate_search_no_results(self):
        observations = [
            Observation(tool_name="search_properties", success=True, result_count=0, anomaly=True),
        ]
        ev = evaluate(observations, 1)
        assert not ev.success
        assert ev.should_replan
        assert ev.replan_reason == "search_no_results"

    def test_evaluate_tool_failure(self):
        observations = [
            Observation(tool_name="search_properties", success=False, anomaly=True),
        ]
        ev = evaluate(observations, 1)
        assert not ev.success
        assert ev.should_replan

    def test_evaluate_empty_observations(self):
        ev = evaluate([], 0)
        assert ev.success

    def test_replan_context(self):
        ev = evaluate([
            Observation(tool_name="search_properties", success=True, result_count=0, anomaly=True),
        ], 1)
        ctx = build_replan_context(ev)
        assert "REPLANIFICACIÓN" in ctx or "broaden" in ctx.lower() or "ajustar" in ctx.lower()

    def test_success_summary(self):
        summary = _build_success_summary([
            Observation(tool_name="search_properties", success=True, result_count=5),
            Observation(tool_name="get_property_details", success=True),
        ])
        assert "search_properties" in summary
        assert "5" in summary
