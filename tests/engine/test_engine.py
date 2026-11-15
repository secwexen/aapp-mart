"""Integration tests for the AAPP-MART core execution engine."""

from uuid import UUID

import pytest

from aapp_mart.engine.contracts import (
    ComponentName,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
    new_contract_metadata,
)
from aapp_mart.engine.exceptions import ComponentNotRegisteredError, ExecutionError
from aapp_mart.engine.pipeline import ExecutionPipeline
from aapp_mart.events import Event, EventPublisher, EventType


class SuccessfulComponent:
    """Test component that always returns a successful result."""

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

    component_name = ComponentName.MART

    def execute(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        """Simulate an execution failure."""

        raise RuntimeError("Simulated component failure")


class MismatchedComponent:
    """Component that returns a result with an incorrect execution ID."""

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
    assert result.output["message"] == ("Execution completed successfully")


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

    status = pipeline.get_state(request.execution_id)

    assert status is ExecutionStatus.SUCCEEDED


def test_execution_state_history(
    pipeline: ExecutionPipeline,
) -> None:
    """Verify execution lifecycle transitions are recorded."""

    pipeline.register_component(SuccessfulComponent())

    request = create_request()

    pipeline.submit(request)

    history = pipeline.get_state_history(
        request.execution_id,
    )

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

    assert received[-1].correlation_id == (request.metadata.correlation_id)


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

    pipeline = ExecutionPipeline(
        event_publisher=publisher,
    )

    pipeline.register_component(SuccessfulComponent())

    result = pipeline.submit(create_request())

    assert result.status is ExecutionStatus.SUCCEEDED
    assert len(received) == 3

    assert [event.event_type for event in received] == [
        EventType.EXECUTION_SUBMITTED,
        EventType.EXECUTION_STARTED,
        EventType.EXECUTION_SUCCEEDED,
    ]
