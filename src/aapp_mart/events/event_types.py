"""Canonical event types and event-type normalization helpers."""

from __future__ import annotations

from enum import StrEnum


class EventType(StrEnum):
    """Event names emitted by AAPP-MART core components."""

    EXECUTION_SUBMITTED = "execution.submitted"
    EXECUTION_STARTED = "execution.started"
    EXECUTION_SUCCEEDED = "execution.succeeded"
    EXECUTION_FAILED = "execution.failed"
    EXECUTION_CANCELLED = "execution.cancelled"

    COMPONENT_REGISTERED = "component.registered"
    COMPONENT_UNREGISTERED = "component.unregistered"

    PREDICTION_COMPLETED = "prediction.completed"
    SIMULATION_COMPLETED = "simulation.completed"

    CUSTOM = "custom"


def normalize_event_type(event_type: object) -> str:
    """Validate and normalize an event type.

    Matching is case-sensitive. Surrounding whitespace is removed
    from string event types. Unknown custom event names are supported.
    """

    if isinstance(event_type, EventType):
        return event_type.value

    if not isinstance(event_type, str):
        raise TypeError("event_type must be an EventType or string.")

    normalized = event_type.strip()

    if not normalized:
        raise ValueError("event_type must not be empty.")

    return normalized


__all__ = [
    "EventType",
    "normalize_event_type",
]
