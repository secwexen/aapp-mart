"""Core execution pipeline for AAPP, MART, and ENGINE."""

from __future__ import annotations

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
from aapp_mart.engine.state_machine import StateTransition
from aapp_mart.engine.utils import validate_execution_request
from aapp_mart.events import EventPublisher
from aapp_mart.runtime.execution import RuntimeExecution


def _validate_component_result(value: object) -> ExecutionResult:
    """Validate and return a component execution result."""
    if not isinstance(value, ExecutionResult):
        raise TypeError("Component must return an ExecutionResult.")

    return value


class ExecutionPipeline:
    """Orchestrate registered components through a shared runtime."""

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
            RuntimeExecution,
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
                raise ValueError(f"Component already registered: {component_name.value}")

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
            runtime = self._states.get(execution_id)

        if runtime is None:
            raise ExecutionError(
                "Execution state not found.",
                execution_id=str(execution_id),
            )

        return runtime.status

    def get_state_history(
        self,
        execution_id: UUID,
    ) -> tuple[StateTransition, ...]:
        """Return the transition history for an execution."""
        with self._lock:
            runtime = self._states.get(execution_id)

        if runtime is None:
            raise ExecutionError(
                "Execution state not found.",
                execution_id=str(execution_id),
            )

        return runtime.history

    def submit(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        """Submit a request and execute its registered component."""
        validate_execution_request(request)

        with self._lock:
            component = self._components.get(request.component)

            if component is None:
                raise ComponentNotRegisteredError("Component is not registered: " f"{request.component.value}")

            if request.execution_id in self._states:
                raise ExecutionError(
                    "Execution ID has already been submitted.",
                    execution_id=str(request.execution_id),
                )

            runtime = RuntimeExecution(
                request,
                event_publisher=self._event_publisher,
                publish_submitted=False,
                event_source="aapp_mart.engine",
            )
            self._states[request.execution_id] = runtime

        # Register the runtime before notifying event subscribers.
        runtime.publish_submitted()

        try:
            runtime.start()
        except Exception as exc:  # pylint: disable=broad-exception-caught
            if runtime.context.is_cancelled:
                return runtime.cancel()

            return runtime.fail_before_start(exc)

        try:
            result = _validate_component_result(component.execute(request))
            return runtime.complete(result)

        except Exception as exc:  # pylint: disable=broad-exception-caught
            return runtime.fail(exc)


__all__ = ["ExecutionPipeline"]
