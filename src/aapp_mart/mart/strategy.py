"""MART execution strategy definitions."""

from dataclasses import dataclass
from typing import Protocol

from aapp_mart.mart.behavior import AgentContext


@dataclass(frozen=True, slots=True)
class StrategyStep:
    """Represent an explicitly configured agent task."""

    agent_id: str
    context: AgentContext
    order: int

    def __post_init__(self) -> None:
        """Validate strategy step configuration."""
        if not self.agent_id.strip():
            raise ValueError("Agent ID cannot be empty.")

        if self.agent_id != self.context.agent_id:
            raise ValueError("Strategy agent ID must match context agent ID.")

        if self.order < 0:
            raise ValueError("Strategy order cannot be negative.")


class ExecutionStrategy(Protocol):
    """Define the contract for MART execution strategies."""

    def get_steps(self) -> tuple[StrategyStep, ...]:
        """Return the configured strategy steps."""
        ...


@dataclass(frozen=True, slots=True)
class SequentialStrategy:
    """Execute explicitly configured tasks in sequential order."""

    steps: tuple[StrategyStep, ...]

    def __post_init__(self) -> None:
        """Validate strategy configuration."""
        orders = [step.order for step in self.steps]

        if len(orders) != len(set(orders)):
            raise ValueError("Duplicate strategy step orders.")

        if tuple(sorted(orders)) != tuple(orders):
            raise ValueError("Strategy steps must be ordered by execution order.")

    def get_steps(self) -> tuple[StrategyStep, ...]:
        """Return configured steps in execution order."""
        return self.steps
