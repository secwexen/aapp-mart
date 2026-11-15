"""Immutable event and event-metadata contracts for AAPP-MART."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, cast
from uuid import UUID, uuid4

from aapp_mart.events.event_types import EventType, normalize_event_type


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


def _empty_string_mapping() -> dict[str, str]:
    """Create an empty string-to-string mapping."""
    return {}


def _empty_payload_mapping() -> dict[str, Any]:
    """Create an empty event payload."""
    return {}


def _validate_non_empty_string(
    value: object,
    field_name: str,
) -> str:
    """Validate and return a non-empty string."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")

    return value


def _validate_timestamp(value: object) -> datetime:
    """Validate a timezone-aware datetime."""

    if not isinstance(value, datetime):
        raise TypeError("occurred_at must be a datetime instance.")

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("occurred_at must be timezone-aware.")

    return value


def _validate_metadata(value: object) -> EventMetadata:
    """Validate and return event metadata."""

    if not isinstance(value, EventMetadata):
        raise TypeError("metadata must be an EventMetadata instance.")

    return value


def _validate_event_id(value: object) -> UUID:
    """Validate and return an event UUID."""

    if not isinstance(value, UUID):
        raise TypeError("event_id must be a UUID instance.")

    return value


def _freeze_string_mapping(
    value: object,
    field_name: str,
) -> Mapping[str, str]:
    """Validate and freeze a string-to-string mapping."""

    if not isinstance(value, Mapping):
        raise TypeError(f"{field_name} must be a mapping.")

    mapping: Mapping[object, object] = cast(
        Mapping[object, object],
        value,
    )

    normalized: dict[str, str] = {}

    for key, item in mapping.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError(f"{field_name} keys must be non-empty strings.")

        if not isinstance(item, str):
            raise TypeError(f"{field_name} values must be strings.")

        normalized[key] = item

    frozen: Mapping[str, str] = MappingProxyType(normalized)

    return frozen


def _freeze_payload(value: object) -> Mapping[str, Any]:
    """Validate and freeze an event payload."""

    if not isinstance(value, Mapping):
        raise TypeError("Event payload must be a mapping.")

    payload_mapping: Mapping[str, Any] = cast(
        Mapping[str, Any],
        value,
    )

    frozen_payload: dict[str, Any] = dict(payload_mapping)

    frozen: Mapping[str, Any] = MappingProxyType(frozen_payload)

    return frozen


@dataclass(frozen=True, slots=True)
class EventMetadata:
    """Describe the origin and correlation context of an event."""

    source: str = "aapp_mart"
    correlation_id: str | None = None
    occurred_at: datetime = field(default_factory=_utc_now)
    attributes: Mapping[str, str] = field(default_factory=_empty_string_mapping)

    def __post_init__(self) -> None:
        source = _validate_non_empty_string(
            self.source,
            "Event metadata source",
        )

        if self.correlation_id is not None:
            _validate_non_empty_string(
                self.correlation_id,
                "correlation_id",
            )

        occurred_at = _validate_timestamp(self.occurred_at)

        attributes: Mapping[str, str] = _freeze_string_mapping(
            self.attributes,
            "Event metadata attributes",
        )

        object.__setattr__(self, "source", source.strip())
        object.__setattr__(self, "occurred_at", occurred_at)
        object.__setattr__(self, "attributes", attributes)


@dataclass(frozen=True, slots=True)
class Event:
    """An immutable event envelope delivered by the event publisher."""

    event_type: EventType | str
    payload: Mapping[str, Any] = field(default_factory=_empty_payload_mapping)
    metadata: EventMetadata = field(default_factory=EventMetadata)
    event_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        normalize_event_type(self.event_type)

        payload: Mapping[str, Any] = _freeze_payload(self.payload)

        metadata = _validate_metadata(self.metadata)

        event_id = _validate_event_id(self.event_id)

        object.__setattr__(self, "payload", payload)
        object.__setattr__(self, "metadata", metadata)
        object.__setattr__(self, "event_id", event_id)

    @property
    def occurred_at(self) -> datetime:
        """Return the event timestamp."""
        return self.metadata.occurred_at

    @property
    def source(self) -> str:
        """Return the event source."""
        return self.metadata.source

    @property
    def correlation_id(self) -> str | None:
        """Return the optional correlation identifier."""
        return self.metadata.correlation_id


__all__ = [
    "Event",
    "EventMetadata",
]
