"""Simulation scenario registration and lookup."""

from aapp_mart.simulation.scenario import SimulationScenario


class SimulationScenarioRegistry:
    """Registry for simulation scenario definitions."""

    def __init__(self) -> None:
        self._scenarios: dict[str, SimulationScenario] = {}

    def register(self, scenario: SimulationScenario) -> None:
        """Register a simulation scenario."""
        if scenario.scenario_id in self._scenarios:
            raise ValueError(f"Scenario already registered: {scenario.scenario_id}")

        self._scenarios[scenario.scenario_id] = scenario

    def get(self, scenario_id: str) -> SimulationScenario:
        """Return a registered scenario by its identifier."""
        try:
            return self._scenarios[scenario_id]
        except KeyError as exc:
            raise KeyError(f"Scenario not found: {scenario_id}") from exc

    def contains(self, scenario_id: str) -> bool:
        """Check whether a scenario is registered."""
        return scenario_id in self._scenarios

    def list_scenarios(self) -> tuple[SimulationScenario, ...]:
        """Return registered scenarios in registration order."""
        return tuple(self._scenarios.values())
