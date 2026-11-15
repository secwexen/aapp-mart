"""Public event contracts and synchronous event-dispatch API."""

from aapp_mart.events.event import Event, EventMetadata
from aapp_mart.events.event_types import (
    EventType,
    normalize_event_type,
)
from aapp_mart.events.publisher import (
    EventDispatchFailure,
    EventDispatchResult,
    EventPublisher,
)
from aapp_mart.events.subscriber import (
    EventHandler,
    EventSubscriber,
    Subscription,
)

__all__ = [
    "Event",
    "EventMetadata",
    "EventType",
    "normalize_event_type",
    "EventHandler",
    "EventSubscriber",
    "Subscription",
    "EventDispatchFailure",
    "EventDispatchResult",
    "EventPublisher",
]
