"""Tests for runtime execution lifecycle management."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from typing import cast
from unittest.mock import Mock
from uuid import uuid4

import pytest

from aapp_mart.engine.contracts import (
    ComponentName,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
    new_contract_metadata,
)
from aapp_mart.engine.exceptions import ExecutionError
from aapp_mart.events import EventPublisher
from aapp_mart.runtime.context import ExecutionContext
from aapp_mart.runtime.execution import RuntimeExecution


def _make_request(
    timeout_seconds: float | None = None,
) -> ExecutionRequest:
    """Create a valid execution request."""
    return ExecutionRequest(
        component=ComponentName.AAPP,
        operation="test_operation",
        payload={"target": "staging.example.test"},
        metadata=new_contract_metadata(),
        timeout_seconds=timeout_seconds,
    )


def _make_publisher() -> tuple[Mock, EventPublisher]:
    """Create a mock event publisher."""
    publisher_mock = Mock(spec=EventPublisher)
    publisher = cast(EventPublisher, publisher_mock)
    return publisher_mock, publisher


def _make_runtime(
    request: ExecutionRequest | None = None,
    *,
    publish_submitted: bool = True,
) -> tuple[RuntimeExecution, Mock]:
    """Create a runtime execution with a mock publisher."""
    publisher_mock, publisher = _make_publisher()

    runtime = RuntimeExecution(
        request or _make_request(),
        event_publisher=publisher,
        publish_submitted=publish_submitted,
    )

    return runtime, publisher_mock


def test_initializes_pending_execution() -> None:
    """Initialize an execution in the pending state."""
    runtime, _ = _make_runtime()

    assert runtime.status is ExecutionStatus.PENDING
    assert runtime.started_at is None
    assert runtime.result is None
    assert not runtime.history
    assert runtime.is_terminal is False


def test_publishes_submitted_event_on_initialization() -> None:
    """Publish the submission event during initialization."""
    runtime, publisher_mock = _make_runtime()

    assert runtime.status is ExecutionStatus.PENDING
    publisher_mock.publish.assert_called_once()


def test_can_disable_submitted_event_on_initialization() -> None:
    """Allow deferred publication of the submission event."""
    runtime, publisher_mock = _make_runtime(
        publish_submitted=False,
    )

    publisher_mock.publish.assert_not_called()

    assert runtime.status is ExecutionStatus.PENDING


def test_publishes_submitted_event_only_once() -> None:
    """Prevent duplicate submission event publication."""
    runtime, publisher_mock = _make_runtime()

    runtime.publish_submitted()
    runtime.publish_submitted()

    publisher_mock.publish.assert_called_once()


def test_rejects_submitted_event_after_execution_starts() -> None:
    """Reject submission publication after the pending state."""
    runtime, _ = _make_runtime(publish_submitted=False)
    runtime.start()

    with pytest.raises(ExecutionError):
        runtime.publish_submitted()


def test_starts_pending_execution() -> None:
    """Transition a pending execution into the running state."""
    runtime, publisher_mock = _make_runtime()

    runtime.start()

    assert runtime.status is ExecutionStatus.RUNNING
    assert runtime.started_at is not None
    assert runtime.history[-1].previous is ExecutionStatus.PENDING
    assert runtime.history[-1].current is ExecutionStatus.RUNNING
    assert publisher_mock.publish.call_count == 2


def test_rejects_starting_execution_twice() -> None:
    """Prevent an execution from starting more than once."""
    runtime, _ = _make_runtime()
    runtime.start()

    with pytest.raises(ExecutionError):
        runtime.start()


def test_rejects_start_when_context_is_cancelled() -> None:
    """Prevent starting an execution with a cancellation request."""
    request = _make_request()
    context = ExecutionContext.from_request(request)
    context.request_cancellation()

    publisher_mock, publisher = _make_publisher()
    runtime = RuntimeExecution(
        request,
        context,
        event_publisher=publisher,
    )

    with pytest.raises(ExecutionError):
        runtime.start()

    assert runtime.status is ExecutionStatus.PENDING
    publisher_mock.publish.assert_called_once()


def test_rejects_start_when_deadline_has_expired() -> None:
    """Prevent starting an execution after its deadline."""
    request = _make_request(timeout_seconds=1.0)
    context = replace(
        ExecutionContext.from_request(request),
        created_at=datetime.now(timezone.utc) - timedelta(seconds=5),
    )

    runtime = RuntimeExecution(
        request,
        context,
        publish_submitted=False,
    )

    with pytest.raises(ExecutionError):
        runtime.start()

    assert runtime.status is ExecutionStatus.PENDING


def test_succeeds_with_output() -> None:
    """Complete a running execution successfully."""
    runtime, _ = _make_runtime()
    runtime.start()

    result = runtime.succeed(
        {"prediction": "test-result"},
    )

    assert result.status is ExecutionStatus.SUCCEEDED
    assert result.output == {"prediction": "test-result"}
    assert result.error is None
    assert result.started_at == runtime.started_at
    assert result.completed_at.tzinfo is not None
    assert result.metadata == runtime.request.metadata
    assert runtime.result == result
    assert runtime.status is ExecutionStatus.SUCCEEDED
    assert runtime.is_terminal is True


def test_succeeds_without_output() -> None:
    """Allow successful execution without an output payload."""
    runtime, _ = _make_runtime()
    runtime.start()

    result = runtime.succeed()

    assert result.status is ExecutionStatus.SUCCEEDED
    assert result.output == {}


def test_rejects_success_before_start() -> None:
    """Prevent successful completion of a pending execution."""
    runtime, _ = _make_runtime()

    with pytest.raises(ExecutionError):
        runtime.succeed()


def test_rejects_success_after_terminal_state() -> None:
    """Prevent successful completion after execution has terminated."""
    runtime, _ = _make_runtime()
    runtime.start()
    runtime.succeed()

    with pytest.raises(ExecutionError):
        runtime.succeed()


def test_fails_running_execution() -> None:
    """Complete a running execution with normalized error details."""
    runtime, _ = _make_runtime()
    runtime.start()

    result = runtime.fail(RuntimeError("execution failed"))

    assert result.status is ExecutionStatus.FAILED
    assert result.error == {
        "type": "RuntimeError",
        "message": "execution failed",
    }
    assert result.started_at == runtime.started_at
    assert runtime.result == result
    assert runtime.status is ExecutionStatus.FAILED
    assert runtime.is_terminal is True


def test_fails_execution_before_start() -> None:
    """Fail a pending execution without setting a start timestamp."""
    runtime, _ = _make_runtime()

    result = runtime.fail_before_start(
        RuntimeError("startup failed"),
    )

    assert result.status is ExecutionStatus.FAILED
    assert result.started_at is None
    assert result.error == {
        "type": "RuntimeError",
        "message": "startup failed",
    }
    assert runtime.result == result
    assert runtime.is_terminal is True


def test_rejects_fail_before_start_after_start() -> None:
    """Prevent pre-start failure after execution has started."""
    runtime, _ = _make_runtime()
    runtime.start()

    with pytest.raises(ExecutionError):
        runtime.fail_before_start(RuntimeError("failure"))


def test_cancels_pending_execution() -> None:
    """Cancel a pending execution."""
    runtime, _ = _make_runtime()

    result = runtime.cancel()

    assert result.status is ExecutionStatus.CANCELLED
    assert result.output == {"reason": "Execution cancelled"}
    assert runtime.context.is_cancelled is True
    assert runtime.result == result
    assert runtime.is_terminal is True


def test_cancels_running_execution() -> None:
    """Cancel a running execution."""
    runtime, _ = _make_runtime()
    runtime.start()

    result = runtime.cancel()

    assert result.status is ExecutionStatus.CANCELLED
    assert result.started_at == runtime.started_at
    assert runtime.context.is_cancelled is True
    assert runtime.status is ExecutionStatus.CANCELLED


def test_rejects_cancelling_terminal_execution() -> None:
    """Prevent cancellation after execution has terminated."""
    runtime, _ = _make_runtime()
    runtime.start()
    runtime.succeed()

    with pytest.raises(ExecutionError):
        runtime.cancel()


def test_completes_with_component_success_result() -> None:
    """Accept a valid successful component result."""
    runtime, _ = _make_runtime()
    runtime.start()

    component_result = ExecutionResult(
        execution_id=runtime.request.execution_id,
        component=runtime.request.component,
        status=ExecutionStatus.SUCCEEDED,
        output={"result": "component-output"},
    )

    result = runtime.complete(component_result)

    assert result.status is ExecutionStatus.SUCCEEDED
    assert result.output == {"result": "component-output"}
    assert result.started_at == runtime.started_at
    assert result.metadata == runtime.request.metadata
    assert runtime.result == result


def test_completes_with_component_failure_result() -> None:
    """Accept a valid failed component result."""
    runtime, _ = _make_runtime()
    runtime.start()

    component_result = ExecutionResult(
        execution_id=runtime.request.execution_id,
        component=runtime.request.component,
        status=ExecutionStatus.FAILED,
        error={
            "type": "RuntimeError",
            "message": "component failed",
        },
    )

    result = runtime.complete(component_result)

    assert result.status is ExecutionStatus.FAILED
    assert result.error == component_result.error
    assert result.started_at == runtime.started_at
    assert runtime.is_terminal is True


def test_completes_with_component_cancelled_result() -> None:
    """Accept a valid cancelled component result."""
    runtime, _ = _make_runtime()
    runtime.start()

    component_result = ExecutionResult(
        execution_id=runtime.request.execution_id,
        component=runtime.request.component,
        status=ExecutionStatus.CANCELLED,
    )

    result = runtime.complete(component_result)

    assert result.status is ExecutionStatus.CANCELLED
    assert result.started_at == runtime.started_at
    assert runtime.is_terminal is True


def test_rejects_component_result_with_wrong_execution_id() -> None:
    """Reject a component result for another execution."""
    runtime, _ = _make_runtime()
    runtime.start()

    component_result = ExecutionResult(
        execution_id=uuid4(),
        component=runtime.request.component,
        status=ExecutionStatus.SUCCEEDED,
    )

    with pytest.raises(ValueError, match="mismatched execution ID"):
        runtime.complete(component_result)


def test_rejects_component_result_with_wrong_component() -> None:
    """Reject a component result from another component."""
    runtime, _ = _make_runtime()
    runtime.start()

    component_result = ExecutionResult(
        execution_id=runtime.request.execution_id,
        component=ComponentName.MART,
        status=ExecutionStatus.SUCCEEDED,
    )

    with pytest.raises(ValueError, match="mismatched component"):
        runtime.complete(component_result)


@pytest.mark.parametrize(
    "status",
    [
        ExecutionStatus.PENDING,
        ExecutionStatus.RUNNING,
    ],
)
def test_rejects_non_terminal_component_result(
    status: ExecutionStatus,
) -> None:
    """Reject component results with non-terminal statuses."""
    runtime, _ = _make_runtime()
    runtime.start()

    component_result = ExecutionResult(
        execution_id=runtime.request.execution_id,
        component=runtime.request.component,
        status=status,
    )

    with pytest.raises(ValueError, match="non-terminal"):
        runtime.complete(component_result)


def test_rejects_component_result_before_runtime_starts() -> None:
    """Prevent component completion before runtime execution starts."""
    runtime, _ = _make_runtime()

    component_result = ExecutionResult(
        execution_id=runtime.request.execution_id,
        component=runtime.request.component,
        status=ExecutionStatus.SUCCEEDED,
    )

    with pytest.raises(ExecutionError):
        runtime.complete(component_result)


def test_uses_component_result_metadata_when_available() -> None:
    """Preserve metadata supplied by the component result."""
    runtime, _ = _make_runtime()
    runtime.start()

    component_metadata = new_contract_metadata(
        correlation_id="component-correlation",
    )

    component_result = ExecutionResult(
        execution_id=runtime.request.execution_id,
        component=runtime.request.component,
        status=ExecutionStatus.SUCCEEDED,
        metadata=component_metadata,
    )

    result = runtime.complete(component_result)

    assert result.metadata == component_metadata


def test_ignores_event_publisher_failure_during_lifecycle() -> None:
    """Prevent event delivery errors from interrupting execution."""
    publisher_mock, publisher = _make_publisher()
    publisher_mock.publish.side_effect = RuntimeError("event failure")

    runtime = RuntimeExecution(
        _make_request(),
        event_publisher=publisher,
    )

    runtime.start()
    result = runtime.succeed({"result": "ok"})

    assert result.status is ExecutionStatus.SUCCEEDED
    assert runtime.status is ExecutionStatus.SUCCEEDED


def test_exposes_event_publisher() -> None:
    """Expose the publisher associated with the runtime."""
    publisher_mock, publisher = _make_publisher()

    runtime = RuntimeExecution(
        _make_request(),
        event_publisher=publisher,
    )

    assert runtime.event_publisher is publisher
    publisher_mock.publish.assert_called_once()


def test_rejects_context_with_mismatched_execution_id() -> None:
    """Reject a context belonging to another execution."""
    request = _make_request()
    context = replace(
        ExecutionContext.from_request(request),
        execution_id=uuid4(),
    )

    with pytest.raises(
        ValueError,
        match="execution ID does not match",
    ):
        RuntimeExecution(
            request,
            context,
            publish_submitted=False,
        )


def test_rejects_context_with_mismatched_component() -> None:
    """Reject a context belonging to another component."""
    request = _make_request()
    context = replace(
        ExecutionContext.from_request(request),
        component=ComponentName.MART,
    )

    with pytest.raises(
        ValueError,
        match="component does not match",
    ):
        RuntimeExecution(
            request,
            context,
            publish_submitted=False,
        )
