"""Subscriber contracts and subscription identifiers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol, TypeAlias
from uuid import UUID, uuid4

from aapp_mart.events.event import Event

EventHandler: TypeAlias = Callable[[Event], None]


class EventSubscriber(Protocol):
    """Object-based subscriber contract."""

    def handle_event(self, event: Event, /) -> None:
        """Handle one event synchronously."""


@dataclass(frozen=True, slots=True)
class Subscription:
    """Opaque handle used to remove a registered subscription."""

    subscription_id: UUID
    event_type: str | None = None

    @classmethod
    def create(
        cls,
        event_type: str | None = None,
    ) -> Subscription:
        """Create a subscription with a fresh identifier."""

        return cls(
            subscription_id=uuid4(),
            event_type=event_type,
        )


__all__ = [
    "EventHandler",
    "EventSubscriber",
    "Subscription",
]
