"""Execution lifecycle state machine for the AAPP-MART core engine."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from threading import RLock

from aapp_mart.engine.contracts import ExecutionStatus


@dataclass(frozen=True, slots=True)
class StateTransition:
    """Represents a state transition in an execution lifecycle."""

    previous: ExecutionStatus
    current: ExecutionStatus
    timestamp: datetime


class ExecutionStateMachine:
    """Manage valid execution lifecycle transitions."""

    _ALLOWED_TRANSITIONS = {
        ExecutionStatus.PENDING: {
            ExecutionStatus.RUNNING,
            ExecutionStatus.CANCELLED,
        },
        ExecutionStatus.RUNNING: {
            ExecutionStatus.SUCCEEDED,
            ExecutionStatus.FAILED,
            ExecutionStatus.CANCELLED,
        },
        ExecutionStatus.SUCCEEDED: set(),
        ExecutionStatus.FAILED: set(),
        ExecutionStatus.CANCELLED: set(),
    }

    def __init__(self) -> None:
        """Initialize the execution state machine."""

        self._status = ExecutionStatus.PENDING
        self._history: list[StateTransition] = []
        self._lock = RLock()

    @property
    def status(self) -> ExecutionStatus:
        """Return the current execution status."""

        with self._lock:
            return self._status

    @property
    def history(self) -> tuple[StateTransition, ...]:
        """Return an immutable snapshot of transition history."""

        with self._lock:
            return tuple(self._history)

    @property
    def is_terminal(self) -> bool:
        """Check whether execution has reached a terminal state."""

        with self._lock:
            return self._status in {
                ExecutionStatus.SUCCEEDED,
                ExecutionStatus.FAILED,
                ExecutionStatus.CANCELLED,
            }

    def transition(
        self,
        target: ExecutionStatus,
    ) -> StateTransition:
        """Move execution into a valid target state."""

        with self._lock:
            allowed = self._ALLOWED_TRANSITIONS[self._status]

            if target not in allowed:
                raise ValueError(
                    f"Invalid execution transition: "
                    f"{self._status.value} -> {target.value}"
                )

            transition = StateTransition(
                previous=self._status,
                current=target,
                timestamp=datetime.now(timezone.utc),
            )

            self._status = target
            self._history.append(transition)

            return transition
