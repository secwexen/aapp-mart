"""Tests for AAPP-MART runtime context and execution lifecycle.

The runtime package deliberately re-exports the canonical execution contracts
from ``aapp_mart.engine``. These tests therefore exercise the runtime facade
without defining a second result model.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from aapp_mart.engine.contracts import (
    ComponentName,
    ExecutionRequest,
    ExecutionStatus,
    new_contract_metadata,
)
from aapp_mart.engine.exceptions import ContractValidationError, ExecutionError
from aapp_mart.engine.utils import utc_now
from aapp_mart.runtime import (
    ExecutionContext,
    ExecutionResult,
    RuntimeExecution,
)


def _build_request(
    *,
    execution_id=None,
    component: ComponentName = ComponentName.ENGINE,
    deterministic: bool = True,
    seed: int | None = 37,
    timeout_seconds: float | None = None,
) -> ExecutionRequest:
    """Build a valid execution request using the canonical engine contract."""

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
def request_factory():
    """Return the request factory used by runtime tests."""
    return _build_request


@pytest.fixture
def request_obj(request_factory):
    """Provide a standard deterministic engine request."""
    return request_factory()


@pytest.fixture
def context(request_obj):
    """Provide a context derived from a valid engine request."""
    return ExecutionContext.from_request(request_obj)


@pytest.fixture
def execution(request_obj):
    """Provide a pending runtime execution."""
    return RuntimeExecution(request_obj)


# ---------------------------------------------------------------------------
# ExecutionContext
# ---------------------------------------------------------------------------


def test_context_is_created_from_execution_request(request_obj, context):
    assert context.execution_id == request_obj.execution_id
    assert context.component == request_obj.component
    assert context.metadata == request_obj.metadata
    assert context.deterministic is request_obj.deterministic
    assert context.seed == request_obj.seed
    assert context.timeout_seconds == request_obj.timeout_seconds
    assert context.created_at.tzinfo is not None
    assert context.created_at.utcoffset() is not None


def test_context_has_no_deadline_without_timeout(request_factory):
    context = ExecutionContext.from_request(
        request_factory(timeout_seconds=None)
    )
    assert context.deadline is None
    assert context.is_expired is False


def test_context_deadline_is_derived_from_creation_time(request_factory):
    timeout_seconds = 12.5
    context = ExecutionContext.from_request(
        request_factory(timeout_seconds=timeout_seconds)
    )

    assert context.deadline == context.created_at + timedelta(seconds=timeout_seconds)
    assert context.is_expired is False


def test_context_rejects_naive_creation_timestamp(context):
    naive_timestamp = datetime(2026, 1, 1, 12, 0, 0)

    with pytest.raises((ValueError, ContractValidationError)):
        replace(context, created_at=naive_timestamp)


def test_context_detects_expired_deadline(request_factory):
    context = ExecutionContext.from_request(
        request_factory(timeout_seconds=1.0)
    )
    expired_context = replace(
        context,
        created_at=utc_now() - timedelta(seconds=10),
    )

    assert expired_context.is_expired is True


def test_context_can_request_and_observe_cancellation(context):
    assert context.is_cancelled is False

    context.request_cancellation()

    assert context.is_cancelled is True
    assert context.wait_for_cancellation(timeout=0) is True


def test_context_attributes_can_be_set_and_read(context):
    context.set_attribute("trace_label", "unit-test")

    assert context.get_attribute("trace_label") == "unit-test"
    assert context.get_attribute("missing", default="fallback") == "fallback"


def test_context_attribute_snapshot_is_detached(context):
    context.set_attribute("mode", "safe")

    snapshot = context.snapshot_attributes()
    snapshot["mode"] = "modified-copy"
    snapshot["new_key"] = True

    assert context.get_attribute("mode") == "safe"
    assert context.get_attribute("new_key") is None


def test_context_rejects_empty_attribute_key(context):
    with pytest.raises((ValueError, ContractValidationError)):
        context.set_attribute("", "invalid")


def test_context_derives_repeatable_component_seed(context):
    first = context.derive_component_seed("runtime-worker")
    second = context.derive_component_seed("runtime-worker")

    assert isinstance(first, int)
    assert first == second


def test_context_component_seeds_are_component_specific(context):
    first = context.derive_component_seed("worker-a")
    second = context.derive_component_seed("worker-b")

    assert first != second


def test_non_deterministic_context_can_omit_seed(request_factory):
    request = request_factory(deterministic=False, seed=None)
    context = ExecutionContext.from_request(request)

    assert context.deterministic is False
    assert context.seed is None


# ---------------------------------------------------------------------------
# RuntimeExecution lifecycle
# ---------------------------------------------------------------------------


def test_execution_starts_in_pending_state(execution):
    assert execution.status is ExecutionStatus.PENDING
    assert execution.started_at is None
    assert execution.result is None
    assert execution.is_terminal is False


def test_execution_start_transitions_to_running(execution):
    execution.start()

    assert execution.status is ExecutionStatus.RUNNING
    assert execution.started_at is not None
    assert execution.started_at.tzinfo is not None


def test_execution_succeeds_and_returns_canonical_result(execution, request_obj):
    output = {"prediction": "simulated", "confidence": 0.91}
    execution.start()

    result = execution.succeed(output)

    assert isinstance(result, ExecutionResult)
    assert result.status is ExecutionStatus.SUCCEEDED
    assert result.execution_id == request_obj.execution_id
    assert result.output == output
    assert execution.result is result
    assert execution.status is ExecutionStatus.SUCCEEDED
    assert execution.is_terminal is True


def test_execution_failure_produces_failed_result(execution):
    execution.start()

    result = execution.fail(RuntimeError("component failed"))

    assert isinstance(result, ExecutionResult)
    assert result.status is ExecutionStatus.FAILED
    assert result.error is not None
    assert "component failed" in str(result.error)
    assert execution.result is result
    assert execution.is_terminal is True


def test_pending_execution_can_be_cancelled(execution):
    result = execution.cancel()

    assert isinstance(result, ExecutionResult)
    assert result.status is ExecutionStatus.CANCELLED
    assert execution.status is ExecutionStatus.CANCELLED
    assert execution.is_terminal is True


def test_running_execution_can_be_cancelled(request_obj):
    context = ExecutionContext.from_request(request_obj)
    execution = RuntimeExecution(request_obj, context=context)
    execution.start()

    result = execution.cancel()

    assert result.status is ExecutionStatus.CANCELLED
    assert context.is_cancelled is True
    assert execution.status is ExecutionStatus.CANCELLED


def test_execution_cannot_be_started_twice(execution):
    execution.start()

    with pytest.raises(ExecutionError):
        execution.start()


def test_execution_cannot_succeed_before_start(execution):
    with pytest.raises(ExecutionError):
        execution.succeed({"result": "invalid"})


def test_execution_cannot_fail_before_start(execution):
    with pytest.raises(ExecutionError):
        execution.fail(RuntimeError("too early"))


def test_terminal_execution_cannot_be_cancelled_again(execution):
    execution.start()
    execution.succeed({"done": True})

    with pytest.raises(ExecutionError):
        execution.cancel()


def test_execution_result_is_cached(execution):
    execution.start()
    first_result = execution.succeed({"value": 1})

    assert execution.result is first_result
    assert execution.result is execution.result


def test_execution_records_state_transitions(execution):
    execution.start()
    execution.succeed({"completed": True})

    history = execution.history
    assert len(history) >= 2
    assert execution.status is ExecutionStatus.SUCCEEDED


def test_execution_rejects_context_with_different_execution_id(
    request_factory,
):
    request = request_factory()
    mismatched_request = request_factory()
    mismatched_context = ExecutionContext.from_request(mismatched_request)

    with pytest.raises((ValueError, ContractValidationError)):
        RuntimeExecution(request, context=mismatched_context)


def test_execution_with_cancelled_context_cannot_start(request_obj):
    context = ExecutionContext.from_request(request_obj)
    context.request_cancellation()
    execution = RuntimeExecution(request_obj, context=context)

    with pytest.raises(ExecutionError, match="pending"):
        execution.start()


def test_execution_with_expired_context_cannot_start(request_factory):
    request = request_factory(timeout_seconds=1.0)
    context = ExecutionContext.from_request(request)
    context = replace(
        context,
        created_at=utc_now() - timedelta(seconds=10),
    )
    execution = RuntimeExecution(request, context=context)

    with pytest.raises(ExecutionError):
        execution.start()


def test_runtime_result_and_status_are_engine_contracts():
    from aapp_mart.engine.contracts import ExecutionResult as EngineExecutionResult

    assert ExecutionResult is EngineExecutionResult
    assert ExecutionStatus is not None
    assert ExecutionStatus.PENDING.value == "pending"
    assert ExecutionStatus.RUNNING.value == "running"
    assert ExecutionStatus.SUCCEEDED.value == "succeeded"
    assert ExecutionStatus.FAILED.value == "failed"
    assert ExecutionStatus.CANCELLED.value == "cancelled"


def test_utc_timestamp_fixture_is_timezone_aware():
    timestamp = utc_now()

    assert timestamp.tzinfo is not None
    assert timestamp.utcoffset() == timedelta(0)


def test_standard_utc_timezone_is_available():
    """Guard against accidental use of naive wall-clock timestamps in tests."""
    assert datetime.now(timezone.utc).utcoffset() == timedelta(0)
