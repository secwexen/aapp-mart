"""Integration tests for the AAPP-MART core execution engine."""

from typing import Any, Mapping
from uuid import UUID

import pytest

from aapp_mart.aapp.models import PredictionMode
from aapp_mart.aapp.prediction import Prediction
from aapp_mart.aapp.predictor import Predictor
from aapp_mart.engine.contracts import (
    ComponentName,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
    PredictionRequest,
    PredictionResult,
    SimulationRequest,
    new_contract_metadata,
)
from aapp_mart.engine.exceptions import ComponentNotRegisteredError, ExecutionError
from aapp_mart.engine.orchestration import AAPPMartOrchestrator
from aapp_mart.engine.pipeline import ExecutionPipeline
from aapp_mart.events import Event, EventPublisher, EventType
from aapp_mart.simulation.registry import SimulationScenarioRegistry
from aapp_mart.simulation.scenario import SimulationScenario
from aapp_mart.simulation.simulator import Simulator
from aapp_mart.simulation.step import SimulationStep


class SuccessfulComponent:
    """Test component that always returns a successful result."""

    # pylint: disable=too-few-public-methods

    component_name = ComponentName.AAPP

    def execute(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        """Return a successful execution result."""

        return ExecutionResult(
            execution_id=request.execution_id,
            component=self.component_name,
            status=ExecutionStatus.SUCCEEDED,
            output={"message": "Execution completed successfully"},
            metadata=request.metadata,
        )


class FailingComponent:
    """Test component that raises an execution exception."""

    # pylint: disable=too-few-public-methods

    component_name = ComponentName.MART

    def execute(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        """Simulate an execution failure."""

        raise RuntimeError("Simulated component failure")


class MismatchedComponent:
    """Component that returns a result with an incorrect execution ID."""

    # pylint: disable=too-few-public-methods

    component_name = ComponentName.AAPP

    def execute(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        """Return a result with a different execution ID."""

        return ExecutionResult(
            execution_id=UUID(int=request.execution_id.int ^ 1),
            component=self.component_name,
            status=ExecutionStatus.SUCCEEDED,
            output={"message": "Execution completed"},
            metadata=request.metadata,
        )


class PendingComponent:
    """Test component that returns a non-terminal execution status."""

    # pylint: disable=too-few-public-methods

    component_name = ComponentName.AAPP

    def execute(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        """Return an invalid pending result."""

        return ExecutionResult(
            execution_id=request.execution_id,
            component=self.component_name,
            status=ExecutionStatus.PENDING,
        )


class CancelledComponent:
    """Test component that returns a cancelled execution result."""

    # pylint: disable=too-few-public-methods

    component_name = ComponentName.AAPP

    def execute(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        """Return a cancelled execution result."""

        return ExecutionResult(
            execution_id=request.execution_id,
            component=self.component_name,
            status=ExecutionStatus.CANCELLED,
            output={"reason": "Execution cancelled"},
            metadata=request.metadata,
        )


def create_request(
    component: ComponentName = ComponentName.AAPP,
) -> ExecutionRequest:
    """Create a valid execution request for testing."""

    return ExecutionRequest(
        component=component,
        operation="test_execution",
        payload={"target": "test-target"},
        metadata=new_contract_metadata(
            correlation_id="test-correlation-id",
        ),
    )


@pytest.fixture(name="pipeline")
def _pipeline_fixture() -> ExecutionPipeline:
    """Provide a fresh execution pipeline."""

    return ExecutionPipeline()


# ---------------------------------------------------------------------------
# Component registration
# ---------------------------------------------------------------------------


def test_register_component(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify that a component can be registered."""

    pipeline.register_component(SuccessfulComponent())

    assert ComponentName.AAPP in pipeline.registered_components


def test_register_duplicate_component_fails(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify duplicate registration is rejected."""

    pipeline.register_component(SuccessfulComponent())

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        pipeline.register_component(SuccessfulComponent())


def test_replace_registered_component(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify explicit component replacement works."""

    pipeline.register_component(SuccessfulComponent())

    pipeline.register_component(
        SuccessfulComponent(),
        replace_existing=True,
    )

    assert ComponentName.AAPP in pipeline.registered_components


def test_unregister_component(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify a registered component can be removed."""

    pipeline.register_component(SuccessfulComponent())

    removed = pipeline.unregister_component(
        ComponentName.AAPP,
    )

    assert removed is True
    assert ComponentName.AAPP not in pipeline.registered_components


def test_unregister_missing_component(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify removing an unknown component returns false."""

    removed = pipeline.unregister_component(
        ComponentName.AAPP,
    )

    assert removed is False


# ---------------------------------------------------------------------------
# Execution pipeline
# ---------------------------------------------------------------------------


def test_submit_successful_execution(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify the pipeline executes a registered component."""

    pipeline.register_component(SuccessfulComponent())

    request = create_request()
    result = pipeline.submit(request)

    assert result.execution_id == request.execution_id
    assert result.component is ComponentName.AAPP
    assert result.status is ExecutionStatus.SUCCEEDED
    assert result.output["message"] == "Execution completed successfully"


def test_submit_unregistered_component(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify submitting an unknown component raises an error."""

    request = create_request(ComponentName.MART)

    with pytest.raises(ComponentNotRegisteredError):
        pipeline.submit(request)


def test_component_exception_returns_failed_result(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify component exceptions are normalized."""

    pipeline.register_component(FailingComponent())

    request = create_request(ComponentName.MART)
    result = pipeline.submit(request)

    assert result.status is ExecutionStatus.FAILED
    assert result.execution_id == request.execution_id
    assert result.error is not None
    assert result.error["type"] == "RuntimeError"
    assert result.error["message"] == "Simulated component failure"


def test_mismatched_execution_id_returns_failed_result(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify mismatched execution IDs are rejected."""

    pipeline.register_component(MismatchedComponent())

    request = create_request()
    result = pipeline.submit(request)

    assert result.status is ExecutionStatus.FAILED
    assert result.execution_id == request.execution_id
    assert result.error is not None
    assert "mismatched execution ID" in result.error["message"]


def test_non_terminal_result_returns_failed_result(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify components cannot return unfinished execution results."""

    pipeline.register_component(PendingComponent())

    request = create_request()
    result = pipeline.submit(request)

    assert result.status is ExecutionStatus.FAILED
    assert result.error is not None
    assert "non-terminal" in result.error["message"]


def test_duplicate_execution_id_is_rejected(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify an execution ID cannot be submitted twice."""

    pipeline.register_component(SuccessfulComponent())

    request = create_request()
    first_result = pipeline.submit(request)

    assert first_result.status is ExecutionStatus.SUCCEEDED

    with pytest.raises(
        ExecutionError,
        match="already been submitted",
    ):
        pipeline.submit(request)


# ---------------------------------------------------------------------------
# Execution state
# ---------------------------------------------------------------------------


def test_execution_state_after_success(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify the lifecycle reaches the succeeded state."""

    pipeline.register_component(SuccessfulComponent())

    request = create_request()
    pipeline.submit(request)

    assert pipeline.get_state(request.execution_id) is ExecutionStatus.SUCCEEDED


def test_execution_state_history(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify execution lifecycle transitions are recorded."""

    pipeline.register_component(SuccessfulComponent())

    request = create_request()
    pipeline.submit(request)

    history = pipeline.get_state_history(request.execution_id)

    assert len(history) == 2
    assert history[0].previous is ExecutionStatus.PENDING
    assert history[0].current is ExecutionStatus.RUNNING
    assert history[1].previous is ExecutionStatus.RUNNING
    assert history[1].current is ExecutionStatus.SUCCEEDED


def test_failed_execution_state(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify failed executions reach the failed state."""

    pipeline.register_component(FailingComponent())

    request = create_request(ComponentName.MART)
    pipeline.submit(request)

    assert pipeline.get_state(request.execution_id) is ExecutionStatus.FAILED


# ---------------------------------------------------------------------------
# Engine Events integration
# ---------------------------------------------------------------------------


def test_pipeline_publishes_successful_lifecycle_events(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify successful execution lifecycle events."""

    received: list[Event] = []
    observed_states: list[ExecutionStatus] = []
    request = create_request()

    def record_event(event: Event) -> None:
        """Record events and observe the submission state."""

        received.append(event)

        if event.event_type == EventType.EXECUTION_SUBMITTED:
            observed_states.append(pipeline.get_state(request.execution_id))

    pipeline.event_publisher.subscribe(record_event)
    pipeline.register_component(SuccessfulComponent())

    result = pipeline.submit(request)

    assert result.status is ExecutionStatus.SUCCEEDED

    assert [event.event_type for event in received] == [
        EventType.EXECUTION_SUBMITTED,
        EventType.EXECUTION_STARTED,
        EventType.EXECUTION_SUCCEEDED,
    ]

    assert observed_states == [ExecutionStatus.PENDING]
    assert all(event.correlation_id == request.metadata.correlation_id for event in received)
    assert all(event.payload["execution_id"] == str(request.execution_id) for event in received)


def test_pipeline_publishes_failed_lifecycle_events(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify failed execution lifecycle events."""

    received: list[Event] = []
    request = create_request(ComponentName.MART)

    pipeline.event_publisher.subscribe(received.append)
    pipeline.register_component(FailingComponent())

    result = pipeline.submit(request)

    assert result.status is ExecutionStatus.FAILED

    assert [event.event_type for event in received] == [
        EventType.EXECUTION_SUBMITTED,
        EventType.EXECUTION_STARTED,
        EventType.EXECUTION_FAILED,
    ]

    assert received[-1].correlation_id == request.metadata.correlation_id


def test_pipeline_publishes_cancelled_lifecycle_events(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify cancelled execution lifecycle events."""

    received: list[Event] = []
    request = create_request()

    pipeline.event_publisher.subscribe(received.append)
    pipeline.register_component(CancelledComponent())

    result = pipeline.submit(request)

    assert result.status is ExecutionStatus.CANCELLED

    assert [event.event_type for event in received] == [
        EventType.EXECUTION_SUBMITTED,
        EventType.EXECUTION_STARTED,
        EventType.EXECUTION_CANCELLED,
    ]

    assert pipeline.get_state(request.execution_id) is ExecutionStatus.CANCELLED


def test_subscriber_failure_does_not_interrupt_pipeline() -> None:
    """Verify subscriber failures do not interrupt execution."""

    publisher = EventPublisher()
    received: list[Event] = []

    def failing_subscriber(_event: Event) -> None:
        """Simulate a failing event subscriber."""

        raise RuntimeError("Observer unavailable")

    publisher.subscribe(failing_subscriber)
    publisher.subscribe(received.append)

    pipeline = ExecutionPipeline(event_publisher=publisher)
    pipeline.register_component(SuccessfulComponent())

    result = pipeline.submit(create_request())

    assert result.status is ExecutionStatus.SUCCEEDED
    assert len(received) == 3

    assert [event.event_type for event in received] == [
        EventType.EXECUTION_SUBMITTED,
        EventType.EXECUTION_STARTED,
        EventType.EXECUTION_SUCCEEDED,
    ]


# ---------------------------------------------------------------------------
# AAPP - ENGINE integration
# ---------------------------------------------------------------------------


class MockAAPPBackend:
    """Provide controlled prediction results for ENGINE integration tests."""

    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        """Initialize the backend and its seed recording."""

        self.received_seeds: list[int | None] = []

    def predict(
        self,
        request: PredictionRequest,
        mode: PredictionMode,
    ) -> PredictionResult:
        """Return a controlled prediction result."""

        self.received_seeds.append(request.seed)

        return PredictionResult(
            subject=request.subject,
            predicted_paths=(
                {
                    "path_id": "path-001",
                    "nodes": ("entry", "target"),
                    "mode": mode.value,
                },
            ),
            confidence=0.85,
            rationale="Mock AAPP prediction.",
            metadata=request.metadata,
        )


def create_aapp_request() -> ExecutionRequest:
    """Create a valid AAPP prediction execution request."""

    return ExecutionRequest(
        component=ComponentName.AAPP,
        operation="predict",
        payload={
            "subject": "server-01",
            "objective": "Identify potential attack paths.",
            "features": {
                "hostname": "server-01",
                "port": 443,
                "is_external": True,
            },
            "mode": PredictionMode.DETERMINISTIC.value,
        },
        metadata=new_contract_metadata(
            correlation_id="aapp-engine-integration",
        ),
    )


def test_register_aapp_prediction_component(
    pipeline: ExecutionPipeline,
) -> None:
    """Register the AAPP prediction component in ENGINE."""

    prediction = Prediction(
        predictor=Predictor(backend=MockAAPPBackend()),
    )

    pipeline.register_component(prediction)

    assert ComponentName.AAPP in pipeline.registered_components


def test_engine_executes_aapp_prediction(
    pipeline: ExecutionPipeline,
) -> None:
    """Execute an AAPP prediction through ENGINE."""

    prediction = Prediction(
        predictor=Predictor(backend=MockAAPPBackend()),
    )

    pipeline.register_component(prediction)

    request = create_aapp_request()
    result = pipeline.submit(request)

    assert result.execution_id == request.execution_id
    assert result.component is ComponentName.AAPP
    assert result.status is ExecutionStatus.SUCCEEDED
    assert result.output["subject"] == "server-01"
    assert result.output["confidence"] == 0.85
    assert result.error is None


def test_engine_handles_aapp_prediction_failure(
    pipeline: ExecutionPipeline,
) -> None:
    """Normalize AAPP prediction backend failures through ENGINE."""

    prediction = Prediction()
    pipeline.register_component(prediction)

    request = create_aapp_request()
    result = pipeline.submit(request)

    assert result.execution_id == request.execution_id
    assert result.component is ComponentName.AAPP
    assert result.status is ExecutionStatus.FAILED
    assert result.error is not None
    assert result.error["type"] == "PredictionBackendNotConfiguredError"
    assert pipeline.get_state(request.execution_id) is ExecutionStatus.FAILED


def test_engine_tracks_aapp_prediction_lifecycle(
    pipeline: ExecutionPipeline,
) -> None:
    """Track AAPP prediction execution lifecycle."""

    prediction = Prediction(
        predictor=Predictor(backend=MockAAPPBackend()),
    )

    received: list[Event] = []

    pipeline.event_publisher.subscribe(received.append)
    pipeline.register_component(prediction)

    request = create_aapp_request()
    result = pipeline.submit(request)

    assert result.status is ExecutionStatus.SUCCEEDED

    assert [event.event_type for event in received] == [
        EventType.EXECUTION_SUBMITTED,
        EventType.EXECUTION_STARTED,
        EventType.EXECUTION_SUCCEEDED,
    ]

    assert all(event.payload["execution_id"] == str(request.execution_id) for event in received)
    assert all(event.payload["component"] == ComponentName.AAPP.value for event in received)

    assert pipeline.get_state(request.execution_id) is ExecutionStatus.SUCCEEDED

    history = pipeline.get_state_history(request.execution_id)

    assert len(history) == 2
    assert history[0].current is ExecutionStatus.RUNNING
    assert history[1].current is ExecutionStatus.SUCCEEDED


# ---------------------------------------------------------------------------
# MART - ENGINE integration
# ---------------------------------------------------------------------------


class MockMARTStepExecutor:
    """Provide controlled simulation events for ENGINE integration tests."""

    # pylint: disable=too-few-public-methods

    def execute_step(
        self,
        scenario: SimulationScenario,
        step: SimulationStep,
        request: SimulationRequest,
        step_seed: int,
    ) -> Mapping[str, Any]:
        """Return a controlled simulation event."""

        return {
            "scenario_id": scenario.scenario_id,
            "step_id": step.step_id,
            "action": step.action,
            "target": request.target,
            "status": "completed",
            "seed": step_seed,
            "aapp_prediction": request.parameters.get("aapp_prediction"),
        }


def create_mart_scenario() -> SimulationScenario:
    """Create a MART scenario for ENGINE integration tests."""

    return SimulationScenario(
        scenario_id="scenario-001",
        name="MART Integration Scenario",
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


def create_mart_request() -> ExecutionRequest:
    """Create a valid MART simulation execution request."""

    return ExecutionRequest(
        component=ComponentName.MART,
        operation="simulate",
        payload={
            "scenario": "scenario-001",
            "target": "test-target",
            "parameters": {
                "environment": "test",
            },
            "seed": 17,
        },
        metadata=new_contract_metadata(
            correlation_id="mart-engine-integration",
        ),
    )


def create_mart_simulator() -> Simulator:
    """Create a MART simulator with a registered scenario."""

    registry = SimulationScenarioRegistry()
    registry.register(create_mart_scenario())

    return Simulator(
        registry=registry,
        step_executor=MockMARTStepExecutor(),
    )


def test_register_mart_simulation_component(
    pipeline: ExecutionPipeline,
) -> None:
    """Register the MART simulation component in ENGINE."""

    simulator = create_mart_simulator()
    pipeline.register_component(simulator)

    assert ComponentName.MART in pipeline.registered_components


def test_engine_executes_mart_simulation(
    pipeline: ExecutionPipeline,
) -> None:
    """Execute a MART simulation through ENGINE."""

    simulator = create_mart_simulator()
    pipeline.register_component(simulator)

    request = create_mart_request()
    result = pipeline.submit(request)

    assert result.execution_id == request.execution_id
    assert result.component is ComponentName.MART
    assert result.status is ExecutionStatus.SUCCEEDED
    assert result.output["scenario"] == "scenario-001"
    assert len(result.output["events"]) == 2
    assert result.output["summary"]["completed_steps"] == 2
    assert result.error is None


def test_engine_handles_mart_simulation_failure(
    pipeline: ExecutionPipeline,
) -> None:
    """Normalize MART simulation failures through ENGINE."""

    simulator = Simulator(
        registry=SimulationScenarioRegistry(),
        step_executor=MockMARTStepExecutor(),
    )

    pipeline.register_component(simulator)

    request = create_mart_request()
    result = pipeline.submit(request)

    assert result.execution_id == request.execution_id
    assert result.component is ComponentName.MART
    assert result.status is ExecutionStatus.FAILED
    assert result.error is not None
    assert result.error["type"] == "KeyError"
    assert pipeline.get_state(request.execution_id) is ExecutionStatus.FAILED


def test_engine_tracks_mart_simulation_lifecycle(
    pipeline: ExecutionPipeline,
) -> None:
    """Track MART simulation execution lifecycle."""

    received: list[Event] = []

    pipeline.event_publisher.subscribe(received.append)
    pipeline.register_component(create_mart_simulator())

    request = create_mart_request()
    result = pipeline.submit(request)

    assert result.status is ExecutionStatus.SUCCEEDED

    assert [event.event_type for event in received] == [
        EventType.EXECUTION_SUBMITTED,
        EventType.EXECUTION_STARTED,
        EventType.EXECUTION_SUCCEEDED,
    ]

    assert all(event.payload["execution_id"] == str(request.execution_id) for event in received)
    assert all(event.payload["component"] == ComponentName.MART.value for event in received)

    assert pipeline.get_state(request.execution_id) is ExecutionStatus.SUCCEEDED


# ---------------------------------------------------------------------------
# Combined AAPP - MART - ENGINE integration
# ---------------------------------------------------------------------------


def create_combined_request() -> ExecutionRequest:
    """Create a deterministic combined AAPP-MART execution request."""

    return ExecutionRequest(
        component=ComponentName.ENGINE,
        operation="predict_and_simulate",
        payload={
            "prediction": {
                "subject": "server-01",
                "objective": "Identify potential attack paths.",
                "features": {
                    "hostname": "server-01",
                    "port": 443,
                    "is_external": True,
                },
                "mode": PredictionMode.DETERMINISTIC.value,
            },
            "simulation": {
                "scenario": "scenario-001",
                "target": "test-target",
                "parameters": {
                    "environment": "test",
                },
            },
        },
        metadata=new_contract_metadata(
            correlation_id="aapp-mart-integration",
        ),
        deterministic=True,
        seed=42,
    )


def create_combined_pipeline(
    backend: MockAAPPBackend,
) -> ExecutionPipeline:
    """Create a fresh pipeline with the combined orchestrator."""

    prediction = Prediction(
        predictor=Predictor(backend=backend),
    )

    orchestrator = AAPPMartOrchestrator(
        prediction=prediction,
        simulator=create_mart_simulator(),
    )

    combined_pipeline = ExecutionPipeline()
    combined_pipeline.register_component(orchestrator)

    return combined_pipeline


def test_engine_executes_combined_aapp_mart_orchestration(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify AAPP prediction flows into MART through ENGINE."""

    prediction = Prediction(
        predictor=Predictor(backend=MockAAPPBackend()),
    )

    orchestrator = AAPPMartOrchestrator(
        prediction=prediction,
        simulator=create_mart_simulator(),
    )

    pipeline.register_component(orchestrator)

    request = create_combined_request()
    result = pipeline.submit(request)

    assert result.execution_id == request.execution_id
    assert result.component is ComponentName.ENGINE
    assert result.status is ExecutionStatus.SUCCEEDED
    assert result.error is None

    prediction_output = result.output["prediction"]
    simulation_output = result.output["simulation"]

    assert prediction_output["subject"] == "server-01"
    assert prediction_output["confidence"] == 0.85

    assert simulation_output["scenario"] == "scenario-001"
    assert len(simulation_output["events"]) == 2
    assert simulation_output["summary"]["completed_steps"] == 2

    first_event = simulation_output["events"][0]

    assert first_event["aapp_prediction"]["subject"] == "server-01"
    assert first_event["aapp_prediction"]["confidence"] == 0.85

    assert pipeline.get_state(request.execution_id) is ExecutionStatus.SUCCEEDED


def test_combined_orchestration_is_deterministic() -> None:
    """Verify identical seeds produce identical AAPP and MART outputs."""

    first_backend = MockAAPPBackend()
    second_backend = MockAAPPBackend()

    first_pipeline = create_combined_pipeline(first_backend)
    second_pipeline = create_combined_pipeline(second_backend)

    first_result = first_pipeline.submit(create_combined_request())
    second_result = second_pipeline.submit(create_combined_request())

    assert first_result.status is ExecutionStatus.SUCCEEDED
    assert second_result.status is ExecutionStatus.SUCCEEDED

    # AAPP must receive the same derived seed in both executions.
    assert first_backend.received_seeds == second_backend.received_seeds
    assert len(first_backend.received_seeds) == 1
    assert first_backend.received_seeds[0] is not None

    # Prediction output must be reproducible.
    assert first_result.output["prediction"] == second_result.output["prediction"]

    first_simulation = first_result.output["simulation"]
    second_simulation = second_result.output["simulation"]

    # MART events include step seeds, so this checks deterministic seed
    # propagation and event output across the complete orchestration.
    assert first_simulation["events"] == second_simulation["events"]
    assert first_simulation["summary"] == second_simulation["summary"]

    first_step_seeds = [event["seed"] for event in first_simulation["events"]]
    second_step_seeds = [event["seed"] for event in second_simulation["events"]]

    assert first_step_seeds == second_step_seeds
    assert len(first_step_seeds) == 2
