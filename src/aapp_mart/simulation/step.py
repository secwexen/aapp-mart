"""Simulation step definitions."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


def _create_parameters() -> dict[str, Any]:
    """Create an empty parameters dictionary."""
    return {}


@dataclass(frozen=True, slots=True)
class SimulationStep:
    """Represent a single step in a simulation scenario."""

    step_id: str
    name: str
    description: str = ""
    action: str = ""
    parameters: Mapping[str, Any] = field(
        default_factory=_create_parameters,
    )

    def __post_init__(self) -> None:
        """Validate and protect simulation step data."""
        if not self.step_id.strip():
            raise ValueError("Step ID cannot be empty.")

        if not self.name.strip():
            raise ValueError("Step name cannot be empty.")

        object.__setattr__(
            self,
            "parameters",
            MappingProxyType(dict(self.parameters)),
        )
