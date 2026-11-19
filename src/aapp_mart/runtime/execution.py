"""Runtime execution lifecycle management."""

from __future__ import annotations

import logging
from datetime import datetime
from threading import RLock
from typing import Any, Mapping

from aapp_mart.engine.contracts import ExecutionRequest, ExecutionResult, ExecutionStatus
from aapp_mart.engine.exceptions import ExecutionError
from aapp_mart.engine.state_machine import ExecutionStateMachine, StateTransition
from aapp_mart.engine.utils import normalize_error, utc_now
from aapp_mart.events import Event, EventMetadata, EventPublisher, EventType
from aapp_mart.runtime.context import ExecutionContext

logger = logging.getLogger(__name__)


class RuntimeExecution:  # pylint: disable=too-many-instance-attributes
    """Manage the lifecycle of one runtime execution."""

    def __init__(
        self,
        request: ExecutionRequest,
        context: ExecutionContext | None = None,
        *,
        event_publisher: EventPublisher | None = None,
        publish_submitted: bool = True,
        event_source: str = "aapp_mart.runtime",
    ) -> None:
        """Initialize an execution from its request and context."""
        self.request = request
        self.context = context or ExecutionContext.from_request(request)

        if self.context.execution_id != request.execution_id:
            raise ValueError("Runtime context execution ID does not match request")

        if self.context.component != request.component:
            raise ValueError("Runtime context component does not match request")

        self._event_publisher = event_publisher if event_publisher is not None else EventPublisher()
        self._event_source = event_source

        self._state_machine = ExecutionStateMachine()
        self._started_at: datetime | None = None
        self._result: ExecutionResult | None = None
        self._lock = RLock()
        self._submission_event_published = False

        if publish_submitted:
            self.publish_submitted()

    @property
    def event_publisher(self) -> EventPublisher:
        """Return the event publisher used by this execution."""
        return self._event_publisher

    @property
    def status(self) -> ExecutionStatus:
        """Return the current execution status."""
        return self._state_machine.status

    @property
    def started_at(self) -> datetime | None:
        """Return the execution start timestamp."""
        return self._started_at

    @property
    def result(self) -> ExecutionResult | None:
        """Return the final execution result, if available."""
        with self._lock:
            return self._result

    @property
    def history(self) -> tuple[StateTransition, ...]:
        """Return the execution state transition history."""
        return self._state_machine.history

    @property
    def is_terminal(self) -> bool:
        """Return whether execution has reached a terminal state."""
        return self._state_machine.is_terminal

    def publish_submitted(self) -> None:
        """Publish the submission event once the execution is registered."""
        with self._lock:
            if self._submission_event_published:
                return

            if self.status is not ExecutionStatus.PENDING:
                raise ExecutionError(
                    "Submission event requires a pending execution.",
                    execution_id=str(self.request.execution_id),
                )

            self._submission_event_published = True

        self._publish_lifecycle_event(
            EventType.EXECUTION_SUBMITTED,
            ExecutionStatus.PENDING,
        )

    def start(self) -> None:
        """Start a pending execution."""
        with self._lock:
            if self.status is not ExecutionStatus.PENDING:
                raise ExecutionError(
                    "Only pending executions can be started.",
                    execution_id=str(self.request.execution_id),
                )

            if self.context.is_cancelled:
                raise ExecutionError(
                    "Execution has already been cancelled.",
                    execution_id=str(self.request.execution_id),
                )

            if self.context.is_expired:
                raise ExecutionError(
                    "Execution deadline has already expired.",
                    execution_id=str(self.request.execution_id),
                )

            self._started_at = utc_now()
            self._state_machine.transition(ExecutionStatus.RUNNING)

        self._publish_lifecycle_event(
            EventType.EXECUTION_STARTED,
            ExecutionStatus.RUNNING,
        )

    def succeed(
        self,
        output: Mapping[str, Any] | None = None,
    ) -> ExecutionResult:
        """Complete a running execution successfully."""
        with self._lock:
            self._ensure_running()
            self._state_machine.transition(ExecutionStatus.SUCCEEDED)

            result = ExecutionResult(
                execution_id=self.request.execution_id,
                component=self.request.component,
                status=ExecutionStatus.SUCCEEDED,
                output=dict(output or {}),
                started_at=self._started_at,
                completed_at=utc_now(),
                metadata=self.request.metadata,
            )

            self._result = result

        self._publish_lifecycle_event(
            EventType.EXECUTION_SUCCEEDED,
            ExecutionStatus.SUCCEEDED,
        )

        return result

    def complete(self, result: ExecutionResult) -> ExecutionResult:
        """Complete execution using a validated component result."""
        if result.execution_id != self.request.execution_id:
            raise ValueError("Component returned a mismatched execution ID.")

        if result.component != self.request.component:
            raise ValueError("Component returned a mismatched component name.")

        if result.status not in {
            ExecutionStatus.SUCCEEDED,
            ExecutionStatus.FAILED,
            ExecutionStatus.CANCELLED,
        }:
            raise ValueError("Component returned a non-terminal execution status.")

        with self._lock:
            self._ensure_running()

            if result.status is ExecutionStatus.FAILED and not result.error:
                raise ValueError("Failed component results must include error details.")

            final_result = ExecutionResult(
                execution_id=result.execution_id,
                component=result.component,
                status=result.status,
                output=result.output,
                error=result.error,
                started_at=result.started_at or self._started_at,
                completed_at=result.completed_at,
                metadata=result.metadata or self.request.metadata,
            )

            self._state_machine.transition(final_result.status)
            self._result = final_result

        self._publish_terminal_event(final_result.status)

        return final_result

    def fail(self, error: Exception) -> ExecutionResult:
        """Complete a running execution with an error."""
        with self._lock:
            self._ensure_running()
            self._state_machine.transition(ExecutionStatus.FAILED)

            result = ExecutionResult(
                execution_id=self.request.execution_id,
                component=self.request.component,
                status=ExecutionStatus.FAILED,
                error=normalize_error(error),
                started_at=self._started_at,
                completed_at=utc_now(),
                metadata=self.request.metadata,
            )

            self._result = result

        self._publish_terminal_event(ExecutionStatus.FAILED)
        return result

    def fail_before_start(self, error: Exception) -> ExecutionResult:
        """Reject a pending execution before its component starts."""
        with self._lock:
            if self.status is not ExecutionStatus.PENDING:
                raise ExecutionError(
                    "Only pending executions can fail before start.",
                    execution_id=str(self.request.execution_id),
                )

            self._state_machine.transition(ExecutionStatus.FAILED)

            result = ExecutionResult(
                execution_id=self.request.execution_id,
                component=self.request.component,
                status=ExecutionStatus.FAILED,
                error=normalize_error(error),
                started_at=None,
                completed_at=utc_now(),
                metadata=self.request.metadata,
            )

            self._result = result

        self._publish_terminal_event(ExecutionStatus.FAILED)
        return result

    def cancel(self) -> ExecutionResult:
        """Cancel a pending or running execution."""
        with self._lock:
            if self.is_terminal:
                raise ExecutionError(
                    "Terminal executions cannot be cancelled.",
                    execution_id=str(self.request.execution_id),
                )

            self.context.request_cancellation()
            self._state_machine.transition(ExecutionStatus.CANCELLED)

            result = ExecutionResult(
                execution_id=self.request.execution_id,
                component=self.request.component,
                status=ExecutionStatus.CANCELLED,
                output={"reason": "Execution cancelled"},
                started_at=self._started_at,
                completed_at=utc_now(),
                metadata=self.request.metadata,
            )

            self._result = result

        self._publish_lifecycle_event(
            EventType.EXECUTION_CANCELLED,
            ExecutionStatus.CANCELLED,
        )

        return result

    def _publish_terminal_event(
        self,
        status: ExecutionStatus,
    ) -> None:
        """Publish the event corresponding to a terminal status."""
        event_types: dict[ExecutionStatus, EventType] = {
            ExecutionStatus.SUCCEEDED: EventType.EXECUTION_SUCCEEDED,
            ExecutionStatus.FAILED: EventType.EXECUTION_FAILED,
            ExecutionStatus.CANCELLED: EventType.EXECUTION_CANCELLED,
        }

        event_type = event_types.get(status)

        if event_type is None:
            raise ValueError(f"Unsupported terminal execution status: {status}")

        self._publish_lifecycle_event(event_type, status)

    def _publish_lifecycle_event(
        self,
        event_type: EventType,
        status: ExecutionStatus,
    ) -> None:
        """Publish a runtime lifecycle event safely."""
        try:
            event = Event(
                event_type=event_type,
                payload={
                    "execution_id": str(self.request.execution_id),
                    "component": self.request.component.value,
                    "operation": self.request.operation,
                    "status": status.value,
                },
                metadata=EventMetadata(
                    source=self._event_source,
                    correlation_id=self.request.metadata.correlation_id,
                    attributes={
                        "execution_id": str(self.request.execution_id),
                        "component": self.request.component.value,
                    },
                ),
            )

            self._event_publisher.publish(event)

        except Exception:  # pylint: disable=broad-exception-caught
            logger.warning(
                "Runtime lifecycle event publication failed "
                "(event_type=%s, execution_id=%s).",
                event_type.value,
                self.request.execution_id,
            )

    def _ensure_running(self) -> None:
        """Ensure that the execution is currently running."""
        if self.status is not ExecutionStatus.RUNNING:
            raise ExecutionError(
                "Operation requires a running execution.",
                execution_id=str(self.request.execution_id),
            )


__all__ = ["RuntimeExecution"]
