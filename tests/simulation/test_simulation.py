"""Tests for simulation scenarios and registry."""

import pytest

from aapp_mart.simulation.registry import SimulationScenarioRegistry
from aapp_mart.simulation.scenario import SimulationScenario


def create_scenario(
    scenario_id: str = "scenario-001",
    name: str = "Test Scenario",
) -> SimulationScenario:
    """Create a simulation scenario for testing."""
    return SimulationScenario(
        scenario_id=scenario_id,
        name=name,
        description="Test simulation scenario",
        parameters={"target": "test-target"},
    )


def test_register_scenario() -> None:
    """Test successful scenario registration."""
    registry = SimulationScenarioRegistry()
    scenario = create_scenario()

    registry.register(scenario)

    assert registry.contains("scenario-001")
    assert registry.get("scenario-001") is scenario


def test_register_duplicate_scenario_raises_error() -> None:
    """Test that duplicate scenario IDs are rejected."""
    registry = SimulationScenarioRegistry()

    registry.register(create_scenario())

    with pytest.raises(ValueError, match="Scenario already registered"):
        registry.register(create_scenario())


def test_get_unknown_scenario_raises_error() -> None:
    """Test lookup of an unregistered scenario."""
    registry = SimulationScenarioRegistry()

    with pytest.raises(KeyError, match="Scenario not found"):
        registry.get("unknown-scenario")


def test_contains_scenario() -> None:
    """Test scenario existence checks."""
    registry = SimulationScenarioRegistry()

    assert not registry.contains("scenario-001")

    registry.register(create_scenario())

    assert registry.contains("scenario-001")


def test_list_scenarios() -> None:
    """Test that scenarios are returned in registration order."""
    registry = SimulationScenarioRegistry()

    first = create_scenario("scenario-001", "First")
    second = create_scenario("scenario-002", "Second")

    registry.register(first)
    registry.register(second)

    scenarios = registry.list_scenarios()

    assert scenarios == (first, second)
    assert isinstance(scenarios, tuple)


def test_list_scenarios_returns_empty_tuple() -> None:
    """Test listing scenarios when registry is empty."""
    registry = SimulationScenarioRegistry()

    assert not registry.list_scenarios()
