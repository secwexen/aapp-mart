"""Tests for AAPP-MART runtime context and execution lifecycle."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid4

import pytest

from aapp_mart.engine.contracts import ComponentName, ExecutionRequest
from aapp_mart.engine.contracts import ExecutionResult as EngineExecutionResult
from aapp_mart.engine.contracts import ExecutionStatus, new_contract_metadata
from aapp_mart.engine.exceptions import ContractValidationError, ExecutionError
from aapp_mart.engine.pipeline import ExecutionPipeline
from aapp_mart.engine.state_machine import StateTransition
from aapp_mart.engine.utils import utc_now
from aapp_mart.events import Event, EventPublisher, EventType
from aapp_mart.runtime import ExecutionContext, ExecutionResult, RuntimeExecution

# Pytest fixture parameters intentionally reuse fixture names.
# pylint: disable=redefined-outer-name

RequestFactory = Callable[..., ExecutionRequest]


def _build_request(
    *,
    execution_id: UUID | None = None,
    component: ComponentName = ComponentName.ENGINE,
    deterministic: bool = True,
    seed: int | None = 37,
    timeout_seconds: float | None = None,
) -> ExecutionRequest:
    """Build a valid execution request."""

    return ExecutionRequest(
        component=component,
        operation="runtime-test",
        payload={"operation": "runtime-test"},
        metadata=new_contract_metadata(),
        execution_id=execution_id if execution_id is not None else uuid4(),
        timeout_seconds=timeout_seconds,
        deterministic=deterministic,
        seed=seed,
    )


@pytest.fixture
def request_factory() -> RequestFactory:
    """Provide the execution request factory."""

    return _build_request


@pytest.fixture
def request_obj(
    request_factory: RequestFactory,
) -> ExecutionRequest:
    """Provide a standard deterministic engine request."""

    return request_factory()


@pytest.fixture
def context(
    request_obj: ExecutionRequest,
) -> ExecutionContext:
    """Provide a context derived from a valid engine request."""

    return ExecutionContext.from_request(request_obj)


@pytest.fixture
def execution(
    request_obj: ExecutionRequest,
) -> RuntimeExecution:
    """Provide a pending runtime execution."""

    return RuntimeExecution(request_obj)


# ---------------------------------------------------------------------------
# ExecutionContext
# ---------------------------------------------------------------------------


def test_context_is_created_from_execution_request(
    request_obj: ExecutionRequest,
    context: ExecutionContext,
) -> None:
    """Verify context fields are derived from the request."""

    assert context.execution_id == request_obj.execution_id
    assert context.component == request_obj.component
    assert context.metadata == request_obj.metadata
    assert context.deterministic is request_obj.deterministic
    assert context.seed == request_obj.seed
    assert context.timeout_seconds == request_obj.timeout_seconds
    assert context.created_at.tzinfo is not None
    assert context.created_at.utcoffset() is not None


def test_context_has_no_deadline_without_timeout(
    request_factory: RequestFactory,
) -> None:
    """Verify requests without timeouts have no deadline."""

    context = ExecutionContext.from_request(request_factory(timeout_seconds=None))

    assert context.deadline is None
    assert context.is_expired is False


def test_context_deadline_is_derived_from_creation_time(
    request_factory: RequestFactory,
) -> None:
    """Verify the deadline is based on context creation time."""

    timeout_seconds = 12.5

    context = ExecutionContext.from_request(request_factory(timeout_seconds=timeout_seconds))

    assert context.deadline == (context.created_at + timedelta(seconds=timeout_seconds))
    assert context.is_expired is False


def test_context_rejects_naive_creation_timestamp(
    context: ExecutionContext,
) -> None:
    """Reject a context with a naive creation timestamp."""

    naive_timestamp = datetime(2026, 1, 1, 12, 0, 0)

    with pytest.raises((ValueError, ContractValidationError)):
        replace(context, created_at=naive_timestamp)


def test_context_detects_expired_deadline(
    request_factory: RequestFactory,
) -> None:
    """Verify an expired execution deadline is detected."""

    context = ExecutionContext.from_request(request_factory(timeout_seconds=1.0))

    expired_context = replace(
        context,
        created_at=utc_now() - timedelta(seconds=10),
    )

    assert expired_context.is_expired is True


def test_context_can_request_and_observe_cancellation(
    context: ExecutionContext,
) -> None:
    """Verify cancellation can be requested and observed."""

    assert context.is_cancelled is False

    context.request_cancellation()

    assert context.is_cancelled is True
    assert context.wait_for_cancellation(timeout=0) is True


def test_context_attributes_can_be_set_and_read(
    context: ExecutionContext,
) -> None:
    """Verify execution context attributes can be accessed."""

    context.set_attribute("trace_label", "unit-test")

    assert context.get_attribute("trace_label") == "unit-test"
    assert context.get_attribute("missing", default="fallback") == "fallback"


def test_context_attribute_snapshot_is_detached(
    context: ExecutionContext,
) -> None:
    """Verify attribute snapshots cannot modify the original context."""

    context.set_attribute("mode", "safe")

    snapshot: dict[str, Any] = dict(context.snapshot_attributes())
    snapshot["mode"] = "modified-copy"
    snapshot["new_key"] = True

    assert context.get_attribute("mode") == "safe"
    assert context.get_attribute("new_key") is None


def test_context_rejects_empty_attribute_key(
    context: ExecutionContext,
) -> None:
    """Reject empty context attribute keys."""

    with pytest.raises((ValueError, ContractValidationError)):
        context.set_attribute("", "invalid")


def test_context_derives_repeatable_component_seed(
    context: ExecutionContext,
) -> None:
    """Verify component seeds are repeatable."""

    first: int = context.derive_component_seed("runtime-worker")
    second: int = context.derive_component_seed("runtime-worker")

    assert isinstance(first, int)
    assert first == second


def test_context_component_seeds_are_component_specific(
    context: ExecutionContext,
) -> None:
    """Verify different components receive different seeds."""

    first: int = context.derive_component_seed("worker-a")
    second: int = context.derive_component_seed("worker-b")

    assert first != second


def test_non_deterministic_context_can_omit_seed(
    request_factory: RequestFactory,
) -> None:
    """Verify non-deterministic execution can omit its seed."""

    request = request_factory(
        deterministic=False,
        seed=None,
    )

    context = ExecutionContext.from_request(request)

    assert context.deterministic is False
    assert context.seed is None


# ---------------------------------------------------------------------------
# RuntimeExecution lifecycle
# ---------------------------------------------------------------------------


def test_execution_starts_in_pending_state(
    execution: RuntimeExecution,
) -> None:
    """Verify a new execution starts in the pending state."""

    assert execution.status is ExecutionStatus.PENDING
    assert execution.started_at is None
    assert execution.result is None
    assert execution.is_terminal is False


def test_execution_start_transitions_to_running(
    execution: RuntimeExecution,
) -> None:
    """Verify starting an execution transitions it to running."""

    execution.start()

    assert execution.status is ExecutionStatus.RUNNING
    assert execution.started_at is not None
    assert execution.started_at.tzinfo is not None


def test_execution_succeeds_and_returns_canonical_result(
    execution: RuntimeExecution,
    request_obj: ExecutionRequest,
) -> None:
    """Verify successful execution returns the canonical result."""

    output: dict[str, Any] = {
        "prediction": "simulated",
        "confidence": 0.91,
    }

    execution.start()

    result = execution.succeed(output)

    assert isinstance(result, ExecutionResult)
    assert result.status is ExecutionStatus.SUCCEEDED
    assert result.execution_id == request_obj.execution_id
    assert result.output == output
    assert execution.result is result
    assert execution.status is ExecutionStatus.SUCCEEDED
    assert execution.is_terminal is True


def test_execution_failure_produces_failed_result(
    execution: RuntimeExecution,
) -> None:
    """Verify execution failures produce failed results."""

    execution.start()

    result = execution.fail(RuntimeError("component failed"))

    assert isinstance(result, ExecutionResult)
    assert result.status is ExecutionStatus.FAILED
    assert result.error is not None
    assert "component failed" in str(result.error)
    assert execution.result is result
    assert execution.is_terminal is True


def test_pending_execution_can_be_cancelled(
    execution: RuntimeExecution,
) -> None:
    """Verify pending executions can be cancelled."""

    result = execution.cancel()

    assert isinstance(result, ExecutionResult)
    assert result.status is ExecutionStatus.CANCELLED
    assert execution.status is ExecutionStatus.CANCELLED
    assert execution.is_terminal is True


def test_running_execution_can_be_cancelled(
    request_obj: ExecutionRequest,
) -> None:
    """Verify running executions can be cancelled."""

    context = ExecutionContext.from_request(request_obj)
    execution = RuntimeExecution(request_obj, context=context)

    execution.start()

    result = execution.cancel()

    assert result.status is ExecutionStatus.CANCELLED
    assert context.is_cancelled is True
    assert execution.status is ExecutionStatus.CANCELLED


def test_execution_cannot_be_started_twice(
    execution: RuntimeExecution,
) -> None:
    """Reject starting an already running execution."""

    execution.start()

    with pytest.raises(ExecutionError):
        execution.start()


def test_execution_cannot_succeed_before_start(
    execution: RuntimeExecution,
) -> None:
    """Reject successful completion before execution starts."""

    with pytest.raises(ExecutionError):
        execution.succeed({"result": "invalid"})


def test_execution_cannot_fail_before_start(
    execution: RuntimeExecution,
) -> None:
    """Reject failure completion before execution starts."""

    with pytest.raises(ExecutionError):
        execution.fail(RuntimeError("too early"))


def test_terminal_execution_cannot_be_cancelled_again(
    execution: RuntimeExecution,
) -> None:
    """Reject cancellation after a terminal state."""

    execution.start()
    execution.succeed({"done": True})

    with pytest.raises(ExecutionError):
        execution.cancel()


def test_execution_result_is_cached(
    execution: RuntimeExecution,
) -> None:
    """Verify the final execution result is cached."""

    execution.start()
    first_result = execution.succeed({"value": 1})

    assert execution.result is first_result
    assert execution.result is execution.result


def test_execution_records_state_transitions(
    execution: RuntimeExecution,
) -> None:
    """Verify execution state transitions are recorded."""

    execution.start()
    execution.succeed({"completed": True})

    history: tuple[StateTransition, ...] = execution.history

    assert len(history) >= 2
    assert execution.status is ExecutionStatus.SUCCEEDED


def test_execution_rejects_context_with_different_execution_id(
    request_factory: RequestFactory,
) -> None:
    """Reject a context belonging to another execution."""

    request = request_factory()
    mismatched_request = request_factory()

    mismatched_context = ExecutionContext.from_request(mismatched_request)

    with pytest.raises((ValueError, ContractValidationError)):
        RuntimeExecution(request, context=mismatched_context)


def test_execution_with_cancelled_context_cannot_start(
    request_obj: ExecutionRequest,
) -> None:
    """Reject starting an execution with a cancelled context."""

    context = ExecutionContext.from_request(request_obj)
    context.request_cancellation()

    execution = RuntimeExecution(request_obj, context=context)

    with pytest.raises(ExecutionError, match="cancelled"):
        execution.start()


def test_execution_with_expired_context_cannot_start(
    request_factory: RequestFactory,
) -> None:
    """Reject starting an execution with an expired context."""

    request = request_factory(timeout_seconds=1.0)
    context = ExecutionContext.from_request(request)

    context = replace(
        context,
        created_at=utc_now() - timedelta(seconds=10),
    )

    execution = RuntimeExecution(request, context=context)

    with pytest.raises(ExecutionError):
        execution.start()


def test_runtime_result_and_status_are_engine_contracts() -> None:
    """Verify Runtime re-exports canonical Engine contracts."""

    assert ExecutionResult is EngineExecutionResult
    assert ExecutionStatus is not None
    assert ExecutionStatus.PENDING.value == "pending"
    assert ExecutionStatus.RUNNING.value == "running"
    assert ExecutionStatus.SUCCEEDED.value == "succeeded"
    assert ExecutionStatus.FAILED.value == "failed"
    assert ExecutionStatus.CANCELLED.value == "cancelled"


def test_utc_timestamp_fixture_is_timezone_aware() -> None:
    """Verify UTC timestamps are timezone-aware."""

    timestamp = utc_now()

    assert timestamp.tzinfo is not None
    assert timestamp.utcoffset() == timedelta(0)


def test_standard_utc_timezone_is_available() -> None:
    """Verify the standard UTC timezone is available."""

    assert datetime.now(timezone.utc).utcoffset() == timedelta(0)


# ---------------------------------------------------------------------------
# Runtime Events integration
# ---------------------------------------------------------------------------


def test_runtime_publishes_successful_lifecycle_events(
    request_obj: ExecutionRequest,
) -> None:
    """Verify submitted, started and succeeded runtime events."""

    publisher = EventPublisher()
    received: list[Event] = []

    publisher.subscribe(received.append)

    execution = RuntimeExecution(
        request_obj,
        event_publisher=publisher,
    )

    execution.start()
    result = execution.succeed({"result": "completed"})

    assert result.status is ExecutionStatus.SUCCEEDED

    assert [event.event_type for event in received] == [
        EventType.EXECUTION_SUBMITTED,
        EventType.EXECUTION_STARTED,
        EventType.EXECUTION_SUCCEEDED,
    ]

    assert all(event.correlation_id == request_obj.metadata.correlation_id for event in received)

    assert all(event.payload["execution_id"] == str(request_obj.execution_id) for event in received)

    assert all(event.source == "aapp_mart.runtime" for event in received)


def test_runtime_publishes_failed_lifecycle_events(
    request_factory: RequestFactory,
) -> None:
    """Verify failed runtime execution events."""

    publisher = EventPublisher()
    received: list[Event] = []

    publisher.subscribe(received.append)

    request = request_factory()

    execution = RuntimeExecution(
        request,
        event_publisher=publisher,
    )

    execution.start()
    result = execution.fail(RuntimeError("Runtime component failed"))

    assert result.status is ExecutionStatus.FAILED

    assert [event.event_type for event in received] == [
        EventType.EXECUTION_SUBMITTED,
        EventType.EXECUTION_STARTED,
        EventType.EXECUTION_FAILED,
    ]


def test_runtime_publishes_cancelled_lifecycle_events(
    request_factory: RequestFactory,
) -> None:
    """Verify pending cancellation publishes lifecycle events."""

    publisher = EventPublisher()
    received: list[Event] = []

    publisher.subscribe(received.append)

    execution = RuntimeExecution(
        request_factory(),
        event_publisher=publisher,
    )

    result = execution.cancel()

    assert result.status is ExecutionStatus.CANCELLED

    assert [event.event_type for event in received] == [
        EventType.EXECUTION_SUBMITTED,
        EventType.EXECUTION_CANCELLED,
    ]


def test_runtime_subscriber_failure_does_not_interrupt_execution(
    request_factory: RequestFactory,
) -> None:
    """Verify subscriber failures do not interrupt runtime execution."""

    publisher = EventPublisher()
    received: list[Event] = []

    def failing_subscriber(_event: Event) -> None:
        """Simulate a failing event subscriber."""

        raise RuntimeError("Observer unavailable")

    publisher.subscribe(failing_subscriber)
    publisher.subscribe(received.append)

    execution = RuntimeExecution(
        request_factory(),
        event_publisher=publisher,
    )

    execution.start()
    result = execution.succeed({"result": "completed"})

    assert result.status is ExecutionStatus.SUCCEEDED
    assert execution.status is ExecutionStatus.SUCCEEDED
    assert len(received) == 3


class SuccessfulEngineComponent:
    """Component used to verify shared Engine and Runtime event publishing."""

    component_name = ComponentName.AAPP

    def execute(
        self,
        request: ExecutionRequest,
    ) -> EngineExecutionResult:
        """Return a successful Engine execution result."""

        return EngineExecutionResult(
            execution_id=request.execution_id,
            component=self.component_name,
            status=ExecutionStatus.SUCCEEDED,
            output={"result": "engine-completed"},
            metadata=request.metadata,
        )


def test_engine_and_runtime_can_share_event_publisher(
    request_factory: RequestFactory,
) -> None:
    """Verify Engine and Runtime can use the same event publisher."""

    publisher = EventPublisher()
    received: list[Event] = []

    publisher.subscribe(received.append)

    pipeline = ExecutionPipeline(
        event_publisher=publisher,
    )

    pipeline.register_component(SuccessfulEngineComponent())

    engine_request = request_factory(
        component=ComponentName.AAPP,
    )

    engine_result = pipeline.submit(engine_request)

    runtime_request = request_factory(
        component=ComponentName.ENGINE,
    )

    runtime = RuntimeExecution(
        runtime_request,
        event_publisher=publisher,
    )

    runtime.start()
    runtime_result = runtime.succeed({"result": "runtime-completed"})

    assert pipeline.event_publisher is publisher
    assert runtime.event_publisher is publisher

    assert engine_result.status is ExecutionStatus.SUCCEEDED
    assert runtime_result.status is ExecutionStatus.SUCCEEDED

    assert len(received) == 6

    assert [event.event_type for event in received] == [
        EventType.EXECUTION_SUBMITTED,
        EventType.EXECUTION_STARTED,
        EventType.EXECUTION_SUCCEEDED,
        EventType.EXECUTION_SUBMITTED,
        EventType.EXECUTION_STARTED,
        EventType.EXECUTION_SUCCEEDED,
    ]

    assert all(event.source == "aapp_mart.engine" for event in received[:3])

    assert all(event.source == "aapp_mart.runtime" for event in received[3:])
