"""Core execution pipeline for AAPP, MART, and ENGINE."""

from __future__ import annotations

from dataclasses import replace
from threading import RLock
from uuid import UUID

from aapp_mart.engine.contracts import (
    ComponentName,
    ExecutionComponent,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
)
from aapp_mart.engine.exceptions import ComponentNotRegisteredError, ExecutionError
from aapp_mart.engine.state_machine import ExecutionStateMachine
from aapp_mart.engine.utils import normalize_error, utc_now, validate_execution_request
from aapp_mart.events import Event, EventMetadata, EventPublisher, EventType


def _validate_component_result(
    value: object,
) -> ExecutionResult:
    """Validate and return a component execution result."""

    if not isinstance(value, ExecutionResult):
        raise TypeError("Component must return an ExecutionResult.")

    return value


class ExecutionPipeline:
    """Orchestrate registered components through a shared pipeline."""

    def __init__(
        self,
        event_publisher: EventPublisher | None = None,
    ) -> None:
        """Initialize the execution pipeline."""

        self._components: dict[
            ComponentName,
            ExecutionComponent,
        ] = {}

        self._states: dict[
            UUID,
            ExecutionStateMachine,
        ] = {}

        self._lock = RLock()

        self._event_publisher = event_publisher if event_publisher is not None else EventPublisher()

    @property
    def event_publisher(self) -> EventPublisher:
        """Return the event publisher used by this pipeline."""

        return self._event_publisher

    @property
    def registered_components(
        self,
    ) -> tuple[ComponentName, ...]:
        """Return the registered component names."""

        with self._lock:
            return tuple(self._components)

    def register_component(
        self,
        component: ExecutionComponent,
        *,
        replace_existing: bool = False,
    ) -> None:
        """Register an executable component."""

        component_name = getattr(
            component,
            "component_name",
            None,
        )

        execute_method = getattr(
            component,
            "execute",
            None,
        )

        if not isinstance(component_name, ComponentName):
            raise TypeError("Component must expose a valid component_name.")

        if not callable(execute_method):
            raise TypeError("Component must implement execute().")

        with self._lock:
            if component_name in self._components and not replace_existing:
                raise ValueError(f"Component already registered: " f"{component_name.value}")

            self._components[component_name] = component

    def unregister_component(
        self,
        component_name: ComponentName,
    ) -> bool:
        """Remove a registered component."""

        with self._lock:
            if component_name not in self._components:
                return False

            del self._components[component_name]
            return True

    def get_state(
        self,
        execution_id: UUID,
    ) -> ExecutionStatus:
        """Return the state of a previously submitted execution."""

        with self._lock:
            state_machine = self._states.get(execution_id)

            if state_machine is None:
                raise ExecutionError(
                    "Execution state not found.",
                    execution_id=str(execution_id),
                )

            return state_machine.status

    def get_state_history(
        self,
        execution_id: UUID,
    ):
        """Return the transition history for an execution."""

        with self._lock:
            state_machine = self._states.get(execution_id)

            if state_machine is None:
                raise ExecutionError(
                    "Execution state not found.",
                    execution_id=str(execution_id),
                )

            return state_machine.history

    def submit(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        """Submit a request and execute its registered component."""

        validate_execution_request(request)

        with self._lock:
            component = self._components.get(request.component)

            if component is None:
                raise ComponentNotRegisteredError(f"Component is not registered: " f"{request.component.value}")

            if request.execution_id in self._states:
                raise ExecutionError(
                    "Execution ID has already been submitted.",
                    execution_id=str(request.execution_id),
                )

            state_machine = ExecutionStateMachine()

            self._states[request.execution_id] = state_machine

        # Publish submission before transitioning to RUNNING.
        self._publish_lifecycle_event(
            EventType.EXECUTION_SUBMITTED,
            request,
            ExecutionStatus.PENDING,
        )

        state_machine.transition(ExecutionStatus.RUNNING)

        started_at = utc_now()

        self._publish_lifecycle_event(
            EventType.EXECUTION_STARTED,
            request,
            ExecutionStatus.RUNNING,
        )

        try:
            result = _validate_component_result(component.execute(request))

            if result.execution_id != request.execution_id:
                raise ValueError("Component returned a mismatched execution ID.")

            if result.component != request.component:
                raise ValueError("Component returned a mismatched component name.")

            if result.status not in {
                ExecutionStatus.SUCCEEDED,
                ExecutionStatus.FAILED,
                ExecutionStatus.CANCELLED,
            }:
                raise ValueError("Component returned a non-terminal execution status.")

            state_machine.transition(result.status)

            final_result = replace(
                result,
                started_at=result.started_at or started_at,
                metadata=result.metadata or request.metadata,
            )

        except Exception as exc:  # pylint: disable=broad-exception-caught
            if state_machine.status is ExecutionStatus.RUNNING:
                state_machine.transition(ExecutionStatus.FAILED)

            final_result = ExecutionResult(
                execution_id=request.execution_id,
                component=request.component,
                status=ExecutionStatus.FAILED,
                error=normalize_error(exc),
                started_at=started_at,
                metadata=request.metadata,
            )

        terminal_events = {
            ExecutionStatus.SUCCEEDED: EventType.EXECUTION_SUCCEEDED,
            ExecutionStatus.FAILED: EventType.EXECUTION_FAILED,
            ExecutionStatus.CANCELLED: EventType.EXECUTION_CANCELLED,
        }

        self._publish_lifecycle_event(
            terminal_events[final_result.status],
            request,
            final_result.status,
        )

        return final_result

    def _publish_lifecycle_event(
        self,
        event_type: EventType,
        request: ExecutionRequest,
        status: ExecutionStatus,
    ) -> None:
        """Publish an execution lifecycle event safely."""

        try:
            event = Event(
                event_type=event_type,
                payload={
                    "execution_id": str(request.execution_id),
                    "component": request.component.value,
                    "operation": request.operation,
                    "status": status.value,
                },
                metadata=EventMetadata(
                    source="aapp_mart.engine",
                    correlation_id=request.metadata.correlation_id,
                    attributes={
                        "execution_id": str(request.execution_id),
                        "component": request.component.value,
                    },
                ),
            )

            self._event_publisher.publish(event)

        except Exception:  # pylint: disable=broad-exception-caught
            # Event delivery must not interrupt component execution.
            return


__all__ = ["ExecutionPipeline"]
