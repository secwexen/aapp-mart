"""Thread-safe synchronous event publisher."""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import cast
from uuid import UUID

from aapp_mart.events.event import Event
from aapp_mart.events.event_types import EventType, normalize_event_type
from aapp_mart.events.subscriber import EventHandler, EventSubscriber, Subscription


@dataclass(frozen=True, slots=True)
class EventDispatchFailure:
    """Sanitized description of a subscriber callback failure."""

    subscription_id: UUID
    exception_type: str
    message: str


@dataclass(frozen=True, slots=True)
class EventDispatchResult:
    """Summary of an event dispatch operation."""

    event_id: UUID
    attempted_count: int
    delivered_count: int
    failures: tuple[EventDispatchFailure, ...] = ()

    @property
    def failed_count(self) -> int:
        """Return the number of failed callbacks."""
        return len(self.failures)

    @property
    def succeeded(self) -> bool:
        """Return whether every matching subscriber succeeded."""
        return not self.failures


@dataclass(frozen=True, slots=True)
class _RegisteredSubscriber:
    """Internal subscriber registry entry."""

    subscription: Subscription
    callback: EventHandler


def _resolve_subscription_id(value: object) -> UUID:
    """Validate and resolve a subscription identifier."""

    if isinstance(value, Subscription):
        return value.subscription_id

    if isinstance(value, UUID):
        return value

    raise TypeError("subscription must be a Subscription or UUID instance.")


def _validate_event(value: object) -> Event:
    """Validate and return an event instance."""

    if not isinstance(value, Event):
        raise TypeError("event must be an Event instance.")

    return value


class EventPublisher:
    """Publish events to matching subscribers in registration order.

    Subscriber registry operations are protected by an RLock.

    Publishing creates a snapshot of matching subscribers and executes
    callbacks outside the lock. Subscription changes during dispatch
    affect subsequent publications only.

    Subscriber exceptions are isolated and recorded in the result.
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._subscribers: dict[UUID, _RegisteredSubscriber] = {}

    @property
    def subscriber_count(self) -> int:
        """Return the number of registered subscribers."""

        with self._lock:
            return len(self._subscribers)

    def subscribe(
        self,
        subscriber: EventHandler | EventSubscriber,
        *,
        event_type: EventType | str | None = None,
    ) -> Subscription:
        """Register a callable or object-based subscriber."""

        callback: EventHandler = self._resolve_callback(subscriber)

        normalized_type = normalize_event_type(event_type) if event_type is not None else None

        subscription = Subscription.create(normalized_type)

        registered = _RegisteredSubscriber(
            subscription=subscription,
            callback=callback,
        )

        with self._lock:
            self._subscribers[subscription.subscription_id] = registered

        return subscription

    def unsubscribe(
        self,
        subscription: Subscription | UUID,
    ) -> bool:
        """Remove a subscription."""

        subscription_id = _resolve_subscription_id(subscription)

        with self._lock:
            return self._subscribers.pop(subscription_id, None) is not None

    def publish(self, event: Event) -> EventDispatchResult:
        """Dispatch an event to all matching subscribers."""

        validated_event = _validate_event(event)

        event_type = normalize_event_type(validated_event.event_type)

        with self._lock:
            matching = tuple(
                registered
                for registered in self._subscribers.values()
                if (registered.subscription.event_type is None or registered.subscription.event_type == event_type)
            )

        failures: list[EventDispatchFailure] = []
        delivered_count = 0

        for registered in matching:
            try:
                registered.callback(validated_event)

            except Exception as exc:  # pylint: disable=broad-exception-caught
                # Subscriber isolation is intentional.
                # A failed subscriber must not interrupt other deliveries.
                failures.append(
                    EventDispatchFailure(
                        subscription_id=registered.subscription.subscription_id,
                        exception_type=type(exc).__name__,
                        message=str(exc) or "Subscriber callback failed.",
                    )
                )

            else:
                delivered_count += 1

        return EventDispatchResult(
            event_id=validated_event.event_id,
            attempted_count=len(matching),
            delivered_count=delivered_count,
            failures=tuple(failures),
        )

    def clear(self) -> int:
        """Remove all subscribers and return the removed count."""

        with self._lock:
            removed_count = len(self._subscribers)
            self._subscribers.clear()

        return removed_count

    @staticmethod
    def _resolve_callback(
        subscriber: EventHandler | EventSubscriber,
    ) -> EventHandler:
        """Resolve a supported subscriber to a callable."""

        if callable(subscriber):
            return subscriber

        callback: object = getattr(
            subscriber,
            "handle_event",
            None,
        )

        if callable(callback):
            return cast(EventHandler, callback)

        raise TypeError("subscriber must be callable or expose a callable handle_event method.")


__all__ = [
    "EventDispatchFailure",
    "EventDispatchResult",
    "EventPublisher",
]
