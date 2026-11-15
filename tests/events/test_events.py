"""Tests for the AAPP-MART event system."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Lock
from typing import Any, cast
from uuid import UUID

import pytest

from aapp_mart.events import Event, EventMetadata, EventPublisher, EventType, normalize_event_type

# ============================================================
# Event Type Tests
# ============================================================


def test_normalize_event_type_accepts_enum() -> None:
    """Normalize an EventType enum to its string value."""

    result = normalize_event_type(EventType.EXECUTION_STARTED)

    assert result == "execution.started"


def test_normalize_event_type_trims_custom_string() -> None:
    """Remove surrounding whitespace from custom event types."""

    result = normalize_event_type("  plugin.scan.completed  ")

    assert result == "plugin.scan.completed"


@pytest.mark.parametrize(
    "value",
    [
        None,
        1,
        [],
    ],
)
def test_normalize_event_type_rejects_non_string(
    value: object,
) -> None:
    """Reject values that are neither strings nor EventType members."""

    with pytest.raises(TypeError):
        normalize_event_type(value)


def test_normalize_event_type_rejects_empty_string() -> None:
    """Reject empty or whitespace-only event types."""

    with pytest.raises(ValueError):
        normalize_event_type("")

    with pytest.raises(ValueError):
        normalize_event_type("   ")


# ============================================================
# Event Envelope Tests
# ============================================================


def test_event_has_generated_id_and_aware_timestamp() -> None:
    """Generate a UUID and timezone-aware timestamp automatically."""

    event = Event(
        event_type=EventType.EXECUTION_STARTED,
    )

    assert isinstance(event.event_id, UUID)
    assert event.occurred_at.tzinfo is not None
    assert event.occurred_at.utcoffset() is not None


def test_event_accepts_custom_string_type() -> None:
    """Accept custom event names."""

    event = Event(
        event_type="plugin.scan.completed",
    )

    assert event.event_type == "plugin.scan.completed"


def test_event_rejects_empty_type() -> None:
    """Reject an empty event type."""

    with pytest.raises(ValueError):
        Event(event_type="   ")


def test_event_rejects_non_mapping_payload() -> None:
    """Reject payloads that are not mappings."""

    with pytest.raises(TypeError):
        Event(
            event_type=EventType.EXECUTION_STARTED,
            payload=cast(Any, ["invalid"]),
        )


def test_event_rejects_invalid_metadata() -> None:
    """Reject metadata objects that are not EventMetadata instances."""

    with pytest.raises(TypeError):
        Event(
            event_type=EventType.EXECUTION_STARTED,
            metadata=cast(Any, None),
        )


def test_event_rejects_non_uuid_event_id() -> None:
    """Reject event identifiers that are not UUID instances."""

    with pytest.raises(TypeError):
        Event(
            event_type=EventType.EXECUTION_STARTED,
            event_id=cast(Any, "invalid-uuid"),
        )


def test_event_payload_is_read_only() -> None:
    """Ensure that event payloads cannot be modified externally."""

    original_payload: dict[str, Any] = {
        "target": "10.0.0.1",
        "port": 443,
    }

    event = Event(
        event_type=EventType.EXECUTION_STARTED,
        payload=original_payload,
    )

    original_payload["target"] = "10.0.0.2"

    assert event.payload["target"] == "10.0.0.1"

    with pytest.raises(TypeError):
        cast(Any, event.payload)["target"] = "10.0.0.3"


# ============================================================
# Event Metadata Tests
# ============================================================


def test_event_metadata_rejects_empty_source() -> None:
    """Reject empty metadata source values."""

    with pytest.raises(ValueError):
        EventMetadata(source="")

    with pytest.raises(ValueError):
        EventMetadata(source="   ")


def test_event_metadata_rejects_empty_correlation_id() -> None:
    """Reject empty correlation identifiers."""

    with pytest.raises(ValueError):
        EventMetadata(correlation_id="")

    with pytest.raises(ValueError):
        EventMetadata(correlation_id="   ")


def test_event_metadata_rejects_naive_timestamp() -> None:
    """Reject timestamps without timezone information."""

    naive_timestamp = datetime(2026, 1, 1, 12, 0, 0)

    with pytest.raises(ValueError):
        EventMetadata(
            occurred_at=naive_timestamp,
        )


def test_event_metadata_rejects_invalid_attributes() -> None:
    """Reject invalid metadata attribute values."""

    with pytest.raises(TypeError):
        EventMetadata(
            attributes=cast(
                Any,
                {"attempts": 3},
            ),
        )


def test_event_metadata_attributes_are_read_only() -> None:
    """Ensure metadata attributes cannot be modified externally."""

    original_attributes = {
        "environment": "test",
        "component": "engine",
    }

    metadata = EventMetadata(
        attributes=original_attributes,
    )

    original_attributes["environment"] = "production"

    assert metadata.attributes["environment"] == "test"

    with pytest.raises(TypeError):
        cast(Any, metadata.attributes)["environment"] = "production"


# ============================================================
# Event Publisher Tests
# ============================================================


def test_subscribe_receives_matching_event() -> None:
    """Deliver an event to a registered subscriber."""

    publisher = EventPublisher()
    received: list[Event] = []

    publisher.subscribe(received.append)

    event = Event(
        event_type=EventType.EXECUTION_STARTED,
    )

    result = publisher.publish(event)

    assert len(received) == 1
    assert received[0] == event
    assert result.delivered_count == 1
    assert result.failed_count == 0


def test_unfiltered_subscriber_receives_all_event_types() -> None:
    """Deliver different event types to an unfiltered subscriber."""

    publisher = EventPublisher()
    received: list[Event] = []

    publisher.subscribe(received.append)

    first_event = Event(
        event_type=EventType.EXECUTION_STARTED,
    )

    second_event = Event(
        event_type="plugin.scan.completed",
    )

    publisher.publish(first_event)
    publisher.publish(second_event)

    assert len(received) == 2
    assert received[0] == first_event
    assert received[1] == second_event


def test_event_type_filter_does_not_receive_other_types() -> None:
    """Prevent delivery of events that do not match the filter."""

    publisher = EventPublisher()
    received: list[Event] = []

    publisher.subscribe(
        received.append,
        event_type=EventType.EXECUTION_STARTED,
    )

    publisher.publish(Event(event_type=EventType.EXECUTION_FAILED))

    assert not received


def test_subscribers_are_called_in_registration_order() -> None:
    """Preserve subscriber registration order during dispatch."""

    publisher = EventPublisher()
    received: list[str] = []

    def first_subscriber(_event: Event) -> None:
        received.append("first")

    def second_subscriber(_event: Event) -> None:
        received.append("second")

    def third_subscriber(_event: Event) -> None:
        received.append("third")

    publisher.subscribe(first_subscriber)
    publisher.subscribe(second_subscriber)
    publisher.subscribe(third_subscriber)

    publisher.publish(Event(event_type=EventType.EXECUTION_STARTED))

    assert received == [
        "first",
        "second",
        "third",
    ]


# ============================================================
# Subscription Management Tests
# ============================================================


def test_unsubscribe_by_subscription_handle() -> None:
    """Remove a subscriber using its subscription handle."""

    publisher = EventPublisher()

    def subscriber(_event: Event) -> None:
        pass

    subscription = publisher.subscribe(subscriber)

    assert publisher.subscriber_count == 1
    assert publisher.unsubscribe(subscription) is True
    assert publisher.subscriber_count == 0


def test_unsubscribe_by_uuid() -> None:
    """Remove a subscriber using its UUID."""

    publisher = EventPublisher()

    def subscriber(_event: Event) -> None:
        pass

    subscription = publisher.subscribe(subscriber)

    assert publisher.unsubscribe(subscription.subscription_id) is True
    assert publisher.subscriber_count == 0


def test_unsubscribe_rejects_invalid_identifier() -> None:
    """Reject invalid subscription identifiers."""

    publisher = EventPublisher()

    with pytest.raises(TypeError):
        publisher.unsubscribe(cast(Any, "invalid"))


def test_duplicate_subscriptions_have_independent_handles() -> None:
    """Allow duplicate callback registrations with independent handles."""

    publisher = EventPublisher()
    received: list[Event] = []

    def subscriber(event: Event) -> None:
        received.append(event)

    first = publisher.subscribe(subscriber)
    second = publisher.subscribe(subscriber)

    assert first.subscription_id != second.subscription_id
    assert publisher.subscriber_count == 2

    publisher.unsubscribe(first)

    event = Event(
        event_type=EventType.EXECUTION_STARTED,
    )

    publisher.publish(event)

    assert publisher.subscriber_count == 1
    assert len(received) == 1


# ============================================================
# Subscriber Error Isolation Tests
# ============================================================


def test_subscriber_exception_isolated_from_other_subscribers() -> None:
    """Continue dispatching when one subscriber raises an exception."""

    publisher = EventPublisher()
    received: list[str] = []

    def failing_subscriber(event: Event) -> None:
        """Raise an exception to test subscriber error isolation."""
        raise RuntimeError("Subscriber failed")

    def successful_subscriber(_event: Event) -> None:
        received.append("success")

    publisher.subscribe(failing_subscriber)
    publisher.subscribe(successful_subscriber)

    result = publisher.publish(Event(event_type=EventType.EXECUTION_STARTED))

    assert received == ["success"]
    assert result.attempted_count == 2
    assert result.delivered_count == 1
    assert result.failed_count == 1
    assert result.succeeded is False
    assert result.failures[0].exception_type == "RuntimeError"


def test_object_subscriber_is_supported() -> None:
    """Support subscriber objects exposing handle_event."""

    class RecordingSubscriber:
        """Record received events."""

        def __init__(self) -> None:
            """Initialize the event collection."""
            self.events: list[Event] = []

        def handle_event(self, event: Event, /) -> None:
            """Record a received event."""
            self.events.append(event)

    publisher = EventPublisher()
    subscriber = RecordingSubscriber()

    publisher.subscribe(subscriber)

    event = Event(
        event_type=EventType.EXECUTION_STARTED,
    )

    result = publisher.publish(event)

    assert len(subscriber.events) == 1
    assert subscriber.events[0] == event
    assert result.delivered_count == 1
    assert result.failed_count == 0


def test_invalid_subscriber_is_rejected() -> None:
    """Reject objects without a callable subscriber interface."""

    publisher = EventPublisher()

    with pytest.raises(TypeError):
        publisher.subscribe(cast(Any, object()))


def test_publish_rejects_non_event() -> None:
    """Reject values that are not Event instances."""

    publisher = EventPublisher()

    with pytest.raises(TypeError):
        publisher.publish(cast(Any, "invalid-event"))


# ============================================================
# Publisher Lifecycle Tests
# ============================================================


def test_clear_removes_all_subscribers_and_returns_count() -> None:
    """Clear all subscriber registrations."""

    publisher = EventPublisher()

    def first(_event: Event) -> None:
        pass

    def second(_event: Event) -> None:
        pass

    publisher.subscribe(first)
    publisher.subscribe(second)

    assert publisher.subscriber_count == 2

    removed_count = publisher.clear()

    assert removed_count == 2
    assert publisher.subscriber_count == 0

    assert publisher.clear() == 0


def test_subscription_changes_during_dispatch_apply_to_next_publish() -> None:
    """Apply subscription changes after the current dispatch snapshot."""

    publisher = EventPublisher()
    received: list[str] = []

    state = {"changed": False}
    second_handle: list[Any] = []

    def first_subscriber(_event: Event) -> None:
        received.append("first")

        if not state["changed"]:
            state["changed"] = True

            publisher.unsubscribe(second_handle[0])

            def third_subscriber(_next_event: Event) -> None:
                received.append("third")

            publisher.subscribe(third_subscriber)

    def second_subscriber(_event: Event) -> None:
        received.append("second")

    publisher.subscribe(first_subscriber)

    second_handle.append(publisher.subscribe(second_subscriber))

    event = Event(
        event_type=EventType.EXECUTION_STARTED,
    )

    publisher.publish(event)

    assert received == [
        "first",
        "second",
    ]

    received.clear()

    publisher.publish(event)

    assert received == [
        "first",
        "third",
    ]


# ============================================================
# Concurrency Tests
# ============================================================


def test_concurrent_publish_delivers_each_event_to_registered_subscriber() -> None:
    """Deliver concurrent publications without losing events."""

    publisher = EventPublisher()

    received: list[UUID] = []
    received_lock = Lock()

    def subscriber(event: Event) -> None:
        with received_lock:
            received.append(event.event_id)

    publisher.subscribe(subscriber)

    events = [Event(event_type=EventType.EXECUTION_STARTED) for _ in range(100)]

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(
            executor.map(
                publisher.publish,
                events,
            )
        )

    expected_ids = {event.event_id for event in events}

    assert len(received) == 100
    assert set(received) == expected_ids

    assert all(
        result.attempted_count == 1 and result.delivered_count == 1 and result.failed_count == 0 for result in results
    )


# ============================================================
# Event Type Stability Tests
# ============================================================


def test_event_type_values_are_stable_strings() -> None:
    """Ensure canonical event names remain stable strings."""

    expected_values = [
        "execution.submitted",
        "execution.started",
        "execution.succeeded",
        "execution.failed",
        "execution.cancelled",
        "component.registered",
        "component.unregistered",
        "prediction.completed",
        "simulation.completed",
        "custom",
    ]

    actual_values = [event_type.value for event_type in EventType]

    assert actual_values == expected_values

    assert all(isinstance(value, str) for value in actual_values)
