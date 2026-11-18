"""Data models for audit events and their outcomes."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class AuditOutcome(StrEnum):
    """Represent the possible outcomes of an audited operation."""

    ALLOWED = "allowed"
    DENIED = "denied"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class AuditEvent:
    """Represent an immutable, timestamped audit event."""

    event_id: str
    occurred_at: datetime
    actor: str
    action: str
    target: str
    outcome: AuditOutcome
    reason: str

    def __post_init__(self) -> None:
        """Validate required fields and timezone-aware timestamps."""
        for field_name in ("event_id", "actor", "action", "target", "reason"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string.")

        if self.occurred_at.tzinfo is None:
            raise ValueError("occurred_at must include a timezone.")
