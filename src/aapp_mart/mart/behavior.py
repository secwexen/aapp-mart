"""MART agent behavior contracts."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Protocol

from aapp_mart.mart.state import AgentState


def _create_metadata() -> dict[str, Any]:
    """Create an empty metadata dictionary."""
    return {}


@dataclass(frozen=True, slots=True)
class AgentContext:
    """Provide context for an explicitly configured agent task."""

    agent_id: str
    scenario_id: str
    target: str
    parameters: Mapping[str, Any] = field(
        default_factory=_create_metadata,
    )

    def __post_init__(self) -> None:
        """Validate and protect agent context."""
        if not self.agent_id.strip():
            raise ValueError("Agent ID cannot be empty.")

        if not self.scenario_id.strip():
            raise ValueError("Scenario ID cannot be empty.")

        if not self.target.strip():
            raise ValueError("Target cannot be empty.")

        object.__setattr__(
            self,
            "parameters",
            MappingProxyType(dict(self.parameters)),
        )


@dataclass(frozen=True, slots=True)
class AgentBehaviorResult:
    """Represent the result of an agent behavior."""

    agent_id: str
    state: AgentState
    output: Mapping[str, Any] = field(
        default_factory=_create_metadata,
    )
    metadata: Mapping[str, Any] = field(
        default_factory=_create_metadata,
    )

    def __post_init__(self) -> None:
        """Validate and protect behavior result data."""
        if not self.agent_id.strip():
            raise ValueError("Agent ID cannot be empty.")

        object.__setattr__(
            self,
            "output",
            MappingProxyType(dict(self.output)),
        )
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )


class AgentBehavior(Protocol):
    """Define the contract implemented by MART agent behaviors."""

    @property
    def agent_id(self) -> str:
        """Return the agent identifier."""
        ...

    @property
    def state(self) -> AgentState:
        """Return the current agent state."""
        ...

    def execute(
        self,
        context: AgentContext,
    ) -> AgentBehaviorResult:
        """Execute an explicitly configured agent behavior."""
        ...
