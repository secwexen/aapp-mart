"""MART agent coordination."""

from dataclasses import dataclass
from typing import Mapping

from aapp_mart.mart.behavior import AgentBehavior, AgentBehaviorResult, AgentContext
from aapp_mart.mart.strategy import ExecutionStrategy


@dataclass(frozen=True, slots=True)
class CoordinationResult:
    """Represent the results of a coordinated execution."""

    results: tuple[AgentBehaviorResult, ...]

    @property
    def succeeded(self) -> bool:
        """Return whether all agent executions completed."""
        return all(result.state.value == "completed" for result in self.results)


class MARTCoordinator:
    """Coordinate registered agents using an execution strategy."""

    def __init__(
        self,
        agents: Mapping[str, AgentBehavior],
        strategy: ExecutionStrategy,
    ) -> None:
        """Initialize the coordinator."""
        if not agents:
            raise ValueError("At least one agent must be registered.")

        for agent_id, agent in agents.items():
            if not agent_id.strip():
                raise ValueError("Agent ID cannot be empty.")

            if agent.agent_id != agent_id:
                raise ValueError("Registered agent ID does not match its key.")

        self._agents = dict(agents)
        self._strategy = strategy

    def execute(self) -> CoordinationResult:
        """Execute configured agent tasks sequentially."""
        results: list[AgentBehaviorResult] = []

        for step in self._strategy.get_steps():
            agent = self._agents.get(step.agent_id)

            if agent is None:
                raise ValueError(f"Agent '{step.agent_id}' is not registered.")

            if agent.state.value == "disabled":
                raise ValueError(f"Agent '{step.agent_id}' is disabled.")

            context: AgentContext = step.context
            result = agent.execute(context)

            if result.agent_id != step.agent_id:
                raise ValueError("Agent result ID does not match strategy step.")

            results.append(result)

        return CoordinationResult(results=tuple(results))
