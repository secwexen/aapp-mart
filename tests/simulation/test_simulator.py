"""Tests for the simulation execution module."""

from typing import Any, Mapping

import pytest

from aapp_mart.engine.contracts import SimulationRequest, new_contract_metadata
from aapp_mart.engine.utils import derive_seed
from aapp_mart.simulation.registry import SimulationScenarioRegistry
from aapp_mart.simulation.scenario import SimulationScenario
from aapp_mart.simulation.simulator import Simulator
from aapp_mart.simulation.state import SimulationState
from aapp_mart.simulation.step import SimulationStep


class RecordingStepExecutor:  # pylint: disable=too-few-public-methods
    """Record executed steps and return actual execution events."""

    def __init__(self) -> None:
        self.executed_steps: list[str] = []
        self.received_requests: list[SimulationRequest] = []
        self.received_seeds: list[int] = []

    def execute_step(
        self,
        scenario: SimulationScenario,
        step: SimulationStep,
        request: SimulationRequest,
        step_seed: int,
    ) -> Mapping[str, Any]:
        """Execute a step and return its recorded event."""
        self.executed_steps.append(step.step_id)
        self.received_requests.append(request)
        self.received_seeds.append(step_seed)

        return {
            "scenario_id": scenario.scenario_id,
            "step_id": step.step_id,
            "action": step.action,
            "target": request.target,
            "status": "completed",
            "seed": step_seed,
        }


def create_scenario() -> SimulationScenario:
    """Create a scenario containing explicitly defined steps."""
    return SimulationScenario(
        scenario_id="scenario-001",
        name="Test Scenario",
        description="Simulator execution test",
        parameters={"environment": "test"},
        steps=(
            SimulationStep(
                step_id="step-001",
                name="Discovery",
                action="discovery",
            ),
            SimulationStep(
                step_id="step-002",
                name="Validation",
                action="validation",
            ),
        ),
    )


def create_request(seed: int = 17) -> SimulationRequest:
    """Create a simulation request."""
    return SimulationRequest(
        scenario="scenario-001",
        target="test-target",
        parameters={"environment": "test"},
        metadata=new_contract_metadata("correlation-001"),
        seed=seed,
    )


def create_simulator(
    scenario: SimulationScenario,
    executor: RecordingStepExecutor,
) -> Simulator:
    """Create a simulator with a registered scenario."""
    registry = SimulationScenarioRegistry()
    registry.register(scenario)

    return Simulator(
        registry=registry,
        step_executor=executor,
    )


def test_simulator_resolves_registered_scenario() -> None:
    """Verify that the simulator resolves a scenario from the registry."""
    scenario = create_scenario()
    executor = RecordingStepExecutor()
    simulator = create_simulator(scenario, executor)

    result = simulator.simulate(create_request())

    assert result.scenario == scenario.scenario_id


def test_simulator_executes_steps_in_defined_order() -> None:
    """Verify that scenario steps execute in their declared order."""
    scenario = create_scenario()
    executor = RecordingStepExecutor()
    simulator = create_simulator(scenario, executor)

    simulator.simulate(create_request())

    assert executor.executed_steps == [
        "step-001",
        "step-002",
    ]


def test_simulator_collects_actual_execution_events() -> None:
    """Verify that actual executor outputs appear in the result."""
    scenario = create_scenario()
    executor = RecordingStepExecutor()
    simulator = create_simulator(scenario, executor)

    result = simulator.simulate(create_request())

    assert list(result.events) == [
        {
            "scenario_id": "scenario-001",
            "step_id": "step-001",
            "action": "discovery",
            "target": "test-target",
            "status": "completed",
            "seed": derive_seed(17, "scenario-001:step-001"),
        },
        {
            "scenario_id": "scenario-001",
            "step_id": "step-002",
            "action": "validation",
            "target": "test-target",
            "status": "completed",
            "seed": derive_seed(17, "scenario-001:step-002"),
        },
    ]


def test_simulator_passes_request_to_executor() -> None:
    """Verify that the original simulation request reaches every step."""
    scenario = create_scenario()
    executor = RecordingStepExecutor()
    simulator = create_simulator(scenario, executor)
    request = create_request()

    simulator.simulate(request)

    assert len(executor.received_requests) == 2
    assert all(received is request for received in executor.received_requests)
    assert all(received.target == "test-target" for received in executor.received_requests)
    assert all(received.parameters == {"environment": "test"} for received in executor.received_requests)


def test_simulator_derives_deterministic_step_seeds() -> None:
    """Verify that equivalent requests produce identical step seeds."""
    scenario = create_scenario()

    first_executor = RecordingStepExecutor()
    first_simulator = create_simulator(scenario, first_executor)
    first_simulator.simulate(create_request(seed=17))

    second_executor = RecordingStepExecutor()
    second_simulator = create_simulator(scenario, second_executor)
    second_simulator.simulate(create_request(seed=17))

    assert first_executor.received_seeds == second_executor.received_seeds


def test_simulator_derives_different_seeds_for_different_steps() -> None:
    """Verify that different step namespaces produce different seeds."""
    scenario = create_scenario()
    executor = RecordingStepExecutor()
    simulator = create_simulator(scenario, executor)

    simulator.simulate(create_request(seed=17))

    assert executor.received_seeds == [
        derive_seed(17, "scenario-001:step-001"),
        derive_seed(17, "scenario-001:step-002"),
    ]
    assert executor.received_seeds[0] != executor.received_seeds[1]


def test_simulator_uses_different_seed_for_different_base_seed() -> None:
    """Verify that changing the base seed changes step seeds."""
    scenario = create_scenario()

    first_executor = RecordingStepExecutor()
    first_simulator = create_simulator(scenario, first_executor)
    first_simulator.simulate(create_request(seed=17))

    second_executor = RecordingStepExecutor()
    second_simulator = create_simulator(scenario, second_executor)
    second_simulator.simulate(create_request(seed=99))

    assert first_executor.received_seeds != second_executor.received_seeds


def test_simulator_transitions_to_completed_state() -> None:
    """Verify that successful execution completes the simulator."""
    scenario = create_scenario()
    executor = RecordingStepExecutor()
    simulator = create_simulator(scenario, executor)

    simulator.simulate(create_request())

    assert simulator.state == SimulationState.COMPLETED


def test_simulator_transitions_to_failed_state() -> None:
    """Verify that executor failures update the simulator state."""

    class FailingStepExecutor:  # pylint: disable=too-few-public-methods
        """Raise an error when a simulation step executes."""

        def execute_step(
            self,
            scenario: SimulationScenario,
            step: SimulationStep,
            request: SimulationRequest,
            step_seed: int,
        ) -> Mapping[str, Any]:
            """Simulate an execution failure."""
            raise RuntimeError("Step execution failed.")

    scenario = create_scenario()
    registry = SimulationScenarioRegistry()
    registry.register(scenario)

    simulator = Simulator(
        registry=registry,
        step_executor=FailingStepExecutor(),
    )

    with pytest.raises(RuntimeError, match="Step execution failed."):
        simulator.simulate(create_request())

    assert simulator.state == SimulationState.FAILED


def test_simulator_executes_empty_scenario() -> None:
    """Verify that an empty scenario completes without executing steps."""
    scenario = SimulationScenario(
        scenario_id="scenario-empty",
        name="Empty Scenario",
    )
    executor = RecordingStepExecutor()
    simulator = create_simulator(scenario, executor)

    request = SimulationRequest(
        scenario="scenario-empty",
        target="test-target",
        parameters={},
        metadata=new_contract_metadata("correlation-empty"),
        seed=17,
    )

    result = simulator.simulate(request)

    assert result.events == ()
    assert result.summary["total_steps"] == 0
    assert result.summary["completed_steps"] == 0
    assert not executor.executed_steps
