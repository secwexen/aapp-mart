"""Runtime execution lifecycle management."""

from __future__ import annotations

from threading import RLock
from typing import Any, Mapping

from aapp_mart.engine.contracts import (
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
)
from aapp_mart.engine.exceptions import ExecutionError
from aapp_mart.engine.state_machine import (
    ExecutionStateMachine,
    StateTransition,
)
from aapp_mart.engine.utils import normalize_error, utc_now
from aapp_mart.runtime.context import ExecutionContext


class RuntimeExecution:
    """Manage the lifecycle of one runtime execution."""

    def __init__(
        self,
        request: ExecutionRequest,
        context: ExecutionContext | None = None,
    ) -> None:
        """Initialize an execution from its request and context."""

        self.request = request
        self.context = context or ExecutionContext.from_request(
            request
        )

        if self.context.execution_id != request.execution_id:
            raise ValueError(
                "Runtime context execution ID does not match request"
            )

        if self.context.component != request.component:
            raise ValueError(
                "Runtime context component does not match request"
            )

        self._state_machine = ExecutionStateMachine()
        self._started_at = None
        self._result: ExecutionResult | None = None
        self._lock = RLock()

    @property
    def status(self) -> ExecutionStatus:
        """Return the current execution status."""

        return self._state_machine.status

    @property
    def started_at(self):
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

            self._state_machine.transition(
                ExecutionStatus.RUNNING
            )

    def succeed(
        self,
        output: Mapping[str, Any] | None = None,
    ) -> ExecutionResult:
        """Complete a running execution successfully."""

        with self._lock:
            self._ensure_running()

            self._state_machine.transition(
                ExecutionStatus.SUCCEEDED
            )

            self._result = ExecutionResult(
                execution_id=self.request.execution_id,
                component=self.request.component,
                status=ExecutionStatus.SUCCEEDED,
                output=dict(output or {}),
                started_at=self._started_at,
                completed_at=utc_now(),
                metadata=self.request.metadata,
            )

            return self._result

    def fail(
        self,
        error: Exception,
    ) -> ExecutionResult:
        """Complete a running execution with an error."""

        with self._lock:
            self._ensure_running()

            self._state_machine.transition(
                ExecutionStatus.FAILED
            )

            self._result = ExecutionResult(
                execution_id=self.request.execution_id,
                component=self.request.component,
                status=ExecutionStatus.FAILED,
                error=normalize_error(error),
                started_at=self._started_at,
                completed_at=utc_now(),
                metadata=self.request.metadata,
            )

            return self._result

    def cancel(self) -> ExecutionResult:
        """Cancel a pending or running execution."""

        with self._lock:
            if self.is_terminal:
                raise ExecutionError(
                    "Terminal executions cannot be cancelled.",
                    execution_id=str(self.request.execution_id),
                )

            self.context.request_cancellation()

            self._state_machine.transition(
                ExecutionStatus.CANCELLED
            )

            self._result = ExecutionResult(
                execution_id=self.request.execution_id,
                component=self.request.component,
                status=ExecutionStatus.CANCELLED,
                output={"reason": "Execution cancelled"},
                started_at=self._started_at,
                completed_at=utc_now(),
                metadata=self.request.metadata,
            )

            return self._result

    def _ensure_running(self) -> None:
        """Ensure that the execution is currently running."""

        if self.status is not ExecutionStatus.RUNNING:
            raise ExecutionError(
                "Operation requires a running execution.",
                execution_id=str(self.request.execution_id),
            )
