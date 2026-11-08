from datetime import UTC, datetime
from uuid import uuid4

from aapp_mart.audit.models import AuditEvent, AuditOutcome


def create_event(
    *,
    actor: str,
    action: str,
    target: str,
    outcome: AuditOutcome,
    reason: str,
) -> AuditEvent:
    """Create a timestamped audit event; this function performs no external actions."""
    return AuditEvent(
        event_id=str(uuid4()),
        occurred_at=datetime.now(UTC),
        actor=actor,
        action=action,
        target=target,
        outcome=outcome,
        reason=reason,
    )
