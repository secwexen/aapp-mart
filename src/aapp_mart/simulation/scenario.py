"""Simulation scenario definitions."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from aapp_mart.simulation.step import SimulationStep


def _create_parameters() -> dict[str, Any]:
    """Create an empty scenario parameters dictionary."""
    return {}


@dataclass(frozen=True, slots=True)
class SimulationScenario:
    """Immutable definition of a simulation scenario."""

    scenario_id: str
    name: str
    description: str = ""
    parameters: Mapping[str, Any] = field(default_factory=_create_parameters)
    steps: tuple[SimulationStep, ...] = ()

    def __post_init__(self) -> None:
        if not self.scenario_id.strip():
            raise ValueError("scenario_id must not be empty")

        if not self.name.strip():
            raise ValueError("name must not be empty")

        object.__setattr__(
            self,
            "parameters",
            MappingProxyType(dict(self.parameters)),
        )

        steps = tuple(self.steps)

        step_ids = [step.step_id for step in steps]

        if len(step_ids) != len(set(step_ids)):
            raise ValueError("Duplicate simulation step IDs.")

        object.__setattr__(self, "steps", steps)
