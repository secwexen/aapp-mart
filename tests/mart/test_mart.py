"""Tests for MART agent behavior, execution strategies, and coordination."""

from dataclasses import FrozenInstanceError

import pytest

from aapp_mart.mart.behavior import AgentBehaviorResult, AgentContext
from aapp_mart.mart.coordinator import CoordinationResult, MARTCoordinator
from aapp_mart.mart.state import AgentState
from aapp_mart.mart.strategy import SequentialStrategy, StrategyStep


class MockAgent:
    """Provide a controllable MART agent for testing."""

    def __init__(
        self,
        agent_id: str,
        state: AgentState = AgentState.READY,
        result: AgentBehaviorResult | None = None,
        error: Exception | None = None,
    ) -> None:
        """Initialize the mock agent."""
        self._agent_id = agent_id
        self._state = state
        self._result = result
        self._error = error
        self.executed_contexts: list[AgentContext] = []

    @property
    def agent_id(self) -> str:
        """Return the agent identifier."""
        return self._agent_id

    @property
    def state(self) -> AgentState:
        """Return the current agent state."""
        return self._state

    def execute(self, context: AgentContext) -> AgentBehaviorResult:
        """Execute the mock agent behavior."""
        self.executed_contexts.append(context)

        if self._error is not None:
            raise self._error

        if self._result is not None:
            return self._result

        return AgentBehaviorResult(
            agent_id=self.agent_id,
            state=AgentState.COMPLETED,
            output={"status": "completed"},
        )


def create_context(
    agent_id: str = "agent-001",
    scenario_id: str = "scenario-001",
    target: str = "test-target",
) -> AgentContext:
    """Create a valid agent context."""
    return AgentContext(
        agent_id=agent_id,
        scenario_id=scenario_id,
        target=target,
        parameters={"environment": "test"},
    )


def create_result(
    agent_id: str = "agent-001",
    state: AgentState = AgentState.COMPLETED,
) -> AgentBehaviorResult:
    """Create a valid agent behavior result."""
    return AgentBehaviorResult(
        agent_id=agent_id,
        state=state,
        output={"status": state.value},
        metadata={"source": "test"},
    )


def create_strategy(
    *steps: StrategyStep,
) -> SequentialStrategy:
    """Create a sequential execution strategy."""
    return SequentialStrategy(steps=tuple(steps))


def create_strategy_step(
    agent_id: str = "agent-001",
    order: int = 0,
) -> StrategyStep:
    """Create a valid strategy step."""
    return StrategyStep(
        agent_id=agent_id,
        context=create_context(agent_id=agent_id),
        order=order,
    )


# ---------------------------------------------------------------------------
# AgentContext tests
# ---------------------------------------------------------------------------


def test_agent_context_creation() -> None:
    """Verify successful agent context creation."""
    context = create_context()

    assert context.agent_id == "agent-001"
    assert context.scenario_id == "scenario-001"
    assert context.target == "test-target"
    assert context.parameters["environment"] == "test"


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("agent_id", "", "Agent ID cannot be empty."),
        ("agent_id", "   ", "Agent ID cannot be empty."),
        ("scenario_id", "", "Scenario ID cannot be empty."),
        ("scenario_id", "   ", "Scenario ID cannot be empty."),
        ("target", "", "Target cannot be empty."),
        ("target", "   ", "Target cannot be empty."),
    ],
)
def test_agent_context_rejects_empty_required_fields(
    field: str,
    value: str,
    message: str,
) -> None:
    """Verify that required context fields cannot be empty."""
    agent_id = "agent-001"
    scenario_id = "scenario-001"
    target = "test-target"

    if field == "agent_id":
        agent_id = value
    elif field == "scenario_id":
        scenario_id = value
    else:
        target = value

    with pytest.raises(ValueError, match=message):
        AgentContext(
            agent_id=agent_id,
            scenario_id=scenario_id,
            target=target,
        )


def test_agent_context_parameters_are_read_only() -> None:
    """Verify that context parameters cannot be modified."""
    context = create_context()

    with pytest.raises(TypeError):
        context.parameters["environment"] = "production"  # type: ignore[index]


def test_agent_context_is_frozen() -> None:
    """Verify that context fields cannot be reassigned."""
    context = create_context()

    with pytest.raises(FrozenInstanceError):
        context.target = "another-target"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# AgentBehaviorResult tests
# ---------------------------------------------------------------------------


def test_agent_behavior_result_creation() -> None:
    """Verify successful agent result creation."""
    result = create_result()

    assert result.agent_id == "agent-001"
    assert result.state == AgentState.COMPLETED
    assert result.output["status"] == "completed"
    assert result.metadata["source"] == "test"


@pytest.mark.parametrize("agent_id", ["", "   "])
def test_agent_behavior_result_rejects_empty_agent_id(
    agent_id: str,
) -> None:
    """Verify that an empty agent ID is rejected."""
    with pytest.raises(ValueError, match="Agent ID cannot be empty."):
        create_result(agent_id=agent_id)


def test_agent_behavior_result_output_is_read_only() -> None:
    """Verify that result output cannot be modified."""
    result = create_result()

    with pytest.raises(TypeError):
        result.output["status"] = "failed"  # type: ignore[index]


def test_agent_behavior_result_metadata_is_read_only() -> None:
    """Verify that result metadata cannot be modified."""
    result = create_result()

    with pytest.raises(TypeError):
        result.metadata["source"] = "modified"  # type: ignore[index]


# ---------------------------------------------------------------------------
# StrategyStep tests
# ---------------------------------------------------------------------------


def test_strategy_step_creation() -> None:
    """Verify successful strategy step creation."""
    step = create_strategy_step()

    assert step.agent_id == "agent-001"
    assert step.context.agent_id == step.agent_id
    assert step.order == 0


@pytest.mark.parametrize("agent_id", ["", "   "])
def test_strategy_step_rejects_empty_agent_id(
    agent_id: str,
) -> None:
    """Verify that an empty strategy agent ID is rejected."""
    with pytest.raises(ValueError, match="Agent ID cannot be empty."):
        StrategyStep(
            agent_id=agent_id,
            context=create_context(),
            order=0,
        )


def test_strategy_step_rejects_mismatched_agent_id() -> None:
    """Verify that strategy and context agent IDs must match."""
    with pytest.raises(
        ValueError,
        match="Strategy agent ID must match context agent ID.",
    ):
        StrategyStep(
            agent_id="agent-002",
            context=create_context(agent_id="agent-001"),
            order=0,
        )


def test_strategy_step_rejects_negative_order() -> None:
    """Verify that negative execution order is rejected."""
    with pytest.raises(
        ValueError,
        match="Strategy order cannot be negative.",
    ):
        create_strategy_step(order=-1)


# ---------------------------------------------------------------------------
# SequentialStrategy tests
# ---------------------------------------------------------------------------


def test_sequential_strategy_returns_steps_in_defined_order() -> None:
    """Verify that configured steps retain their execution order."""
    first = create_strategy_step("agent-001", 0)
    second = create_strategy_step("agent-002", 1)

    strategy = create_strategy(first, second)

    assert strategy.get_steps() == (first, second)


def test_sequential_strategy_rejects_duplicate_orders() -> None:
    """Verify that duplicate strategy orders are rejected."""
    first = create_strategy_step("agent-001", 0)
    second = create_strategy_step("agent-002", 0)

    with pytest.raises(
        ValueError,
        match="Duplicate strategy step orders.",
    ):
        create_strategy(first, second)


def test_sequential_strategy_rejects_unordered_steps() -> None:
    """Verify that strategy steps must be pre-sorted."""
    first = create_strategy_step("agent-001", 1)
    second = create_strategy_step("agent-002", 0)

    with pytest.raises(
        ValueError,
        match="Strategy steps must be ordered by execution order.",
    ):
        create_strategy(first, second)


def test_sequential_strategy_accepts_empty_steps() -> None:
    """Verify that an empty strategy can be constructed."""
    strategy = SequentialStrategy(steps=())

    assert not strategy.get_steps()


# ---------------------------------------------------------------------------
# MARTCoordinator initialization tests
# ---------------------------------------------------------------------------


def test_coordinator_rejects_empty_agent_registry() -> None:
    """Verify that at least one agent must be registered."""
    with pytest.raises(
        ValueError,
        match="At least one agent must be registered.",
    ):
        MARTCoordinator(
            agents={},
            strategy=SequentialStrategy(steps=()),
        )


def test_coordinator_rejects_empty_registered_agent_id() -> None:
    """Verify that registered agent IDs cannot be empty."""
    agent = MockAgent(agent_id="")

    with pytest.raises(ValueError, match="Agent ID cannot be empty."):
        MARTCoordinator(
            agents={"": agent},
            strategy=SequentialStrategy(steps=()),
        )


def test_coordinator_rejects_mismatched_registered_agent_id() -> None:
    """Verify that registry keys must match agent IDs."""
    agent = MockAgent(agent_id="agent-001")

    with pytest.raises(
        ValueError,
        match="Registered agent ID does not match its key.",
    ):
        MARTCoordinator(
            agents={"agent-002": agent},
            strategy=SequentialStrategy(steps=()),
        )


# ---------------------------------------------------------------------------
# MARTCoordinator execution tests
# ---------------------------------------------------------------------------


def test_coordinator_executes_agents_in_strategy_order() -> None:
    """Verify that agents execute in the configured strategy order."""
    first_agent = MockAgent("agent-001")
    second_agent = MockAgent("agent-002")

    first_step = create_strategy_step("agent-001", 0)
    second_step = create_strategy_step("agent-002", 1)

    coordinator = MARTCoordinator(
        agents={
            "agent-001": first_agent,
            "agent-002": second_agent,
        },
        strategy=create_strategy(first_step, second_step),
    )

    result = coordinator.execute()

    assert len(result.results) == 2
    assert result.results[0].agent_id == "agent-001"
    assert result.results[1].agent_id == "agent-002"
    assert first_agent.executed_contexts == [first_step.context]
    assert second_agent.executed_contexts == [second_step.context]


def test_coordinator_passes_configured_context_to_agent() -> None:
    """Verify that each agent receives its configured context."""
    agent = MockAgent("agent-001")
    context = create_context(
        agent_id="agent-001",
        target="192.0.2.10",
    )
    step = StrategyStep(
        agent_id="agent-001",
        context=context,
        order=0,
    )

    coordinator = MARTCoordinator(
        agents={"agent-001": agent},
        strategy=create_strategy(step),
    )

    coordinator.execute()

    assert agent.executed_contexts == [context]
    assert agent.executed_contexts[0].target == "192.0.2.10"


def test_coordinator_rejects_unregistered_agent() -> None:
    """Verify that strategy references to unknown agents are rejected."""
    step = create_strategy_step("agent-002", 0)

    coordinator = MARTCoordinator(
        agents={"agent-001": MockAgent("agent-001")},
        strategy=create_strategy(step),
    )

    with pytest.raises(
        ValueError,
        match="Agent 'agent-002' is not registered.",
    ):
        coordinator.execute()


def test_coordinator_rejects_disabled_agent() -> None:
    """Verify that disabled agents cannot execute."""
    agent = MockAgent(
        agent_id="agent-001",
        state=AgentState.DISABLED,
    )
    step = create_strategy_step("agent-001", 0)

    coordinator = MARTCoordinator(
        agents={"agent-001": agent},
        strategy=create_strategy(step),
    )

    with pytest.raises(
        ValueError,
        match="Agent 'agent-001' is disabled.",
    ):
        coordinator.execute()

    assert not agent.executed_contexts


def test_coordinator_rejects_mismatched_result_agent_id() -> None:
    """Verify that agent results must match the strategy agent ID."""
    agent = MockAgent(
        agent_id="agent-001",
        result=create_result(agent_id="agent-002"),
    )
    step = create_strategy_step("agent-001", 0)

    coordinator = MARTCoordinator(
        agents={"agent-001": agent},
        strategy=create_strategy(step),
    )

    with pytest.raises(
        ValueError,
        match="Agent result ID does not match strategy step.",
    ):
        coordinator.execute()


def test_coordinator_propagates_agent_execution_errors() -> None:
    """Verify that agent execution errors propagate to the caller."""
    agent = MockAgent(
        agent_id="agent-001",
        error=RuntimeError("Agent execution failed."),
    )
    step = create_strategy_step("agent-001", 0)

    coordinator = MARTCoordinator(
        agents={"agent-001": agent},
        strategy=create_strategy(step),
    )

    with pytest.raises(
        RuntimeError,
        match="Agent execution failed.",
    ):
        coordinator.execute()


def test_coordinator_stops_after_agent_failure() -> None:
    """Verify that later agents are not executed after a failure."""
    first_agent = MockAgent(
        agent_id="agent-001",
        error=RuntimeError("First agent failed."),
    )
    second_agent = MockAgent("agent-002")

    coordinator = MARTCoordinator(
        agents={
            "agent-001": first_agent,
            "agent-002": second_agent,
        },
        strategy=create_strategy(
            create_strategy_step("agent-001", 0),
            create_strategy_step("agent-002", 1),
        ),
    )

    with pytest.raises(RuntimeError, match="First agent failed."):
        coordinator.execute()

    assert len(first_agent.executed_contexts) == 1
    assert not second_agent.executed_contexts


# ---------------------------------------------------------------------------
# CoordinationResult tests
# ---------------------------------------------------------------------------


def test_coordination_result_succeeds_when_all_agents_complete() -> None:
    """Verify successful coordination when every agent completes."""
    result = CoordinationResult(
        results=(
            create_result("agent-001", AgentState.COMPLETED),
            create_result("agent-002", AgentState.COMPLETED),
        ),
    )

    assert result.succeeded is True


@pytest.mark.parametrize(
    "state",
    [
        AgentState.IDLE,
        AgentState.READY,
        AgentState.RUNNING,
        AgentState.FAILED,
        AgentState.DISABLED,
    ],
)
def test_coordination_result_fails_when_agent_is_not_completed(
    state: AgentState,
) -> None:
    """Verify that any non-completed agent makes coordination unsuccessful."""
    result = CoordinationResult(
        results=(
            create_result("agent-001", AgentState.COMPLETED),
            create_result("agent-002", state),
        ),
    )

    assert result.succeeded is False


def test_coordinator_returns_successful_coordination_result() -> None:
    """Verify that successful execution returns completed agent results."""
    agent = MockAgent("agent-001")
    step = create_strategy_step("agent-001", 0)

    coordinator = MARTCoordinator(
        agents={"agent-001": agent},
        strategy=create_strategy(step),
    )

    result = coordinator.execute()

    assert isinstance(result, CoordinationResult)
    assert result.succeeded is True
    assert result.results[0].state == AgentState.COMPLETED
