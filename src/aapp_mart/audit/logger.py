"""Append-only audit logging with hash-chain integrity verification."""

import hashlib
import json
import os
from pathlib import Path
from typing import Any, cast

from aapp_mart.audit.models import AuditEvent

_ZERO_HASH = "0" * 64


class AuditLogError(ValueError):
    """Raised when an audit log is malformed or its hash chain is invalid."""


def _event_payload(event: AuditEvent) -> dict[str, str]:
    """Convert an audit event into a JSON-compatible payload."""
    return {
        "event_id": event.event_id,
        "occurred_at": event.occurred_at.isoformat(),
        "actor": event.actor,
        "action": event.action,
        "target": event.target,
        "outcome": event.outcome.value,
        "reason": event.reason,
    }


def _digest(event_payload: dict[str, str], previous_hash: str) -> str:
    """Calculate the SHA-256 digest of an event and its previous hash."""
    chain_payload: dict[str, dict[str, str] | str] = {
        "event": event_payload,
        "previous_hash": previous_hash,
    }

    encoded = json.dumps(
        chain_payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    return hashlib.sha256(encoded).hexdigest()


def _last_hash(path: Path) -> str:
    """Verify the existing audit log and return its final hash."""
    if not path.exists():
        return _ZERO_HASH

    previous_hash = _ZERO_HASH

    try:
        with path.open("r", encoding="utf-8") as audit_file:
            for line_number, line in enumerate(audit_file, start=1):
                try:
                    raw_record: Any = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise AuditLogError(f"Invalid audit record on line {line_number}.") from exc

                if not isinstance(raw_record, dict):
                    raise AuditLogError(f"Invalid audit record on line {line_number}.")

                record = cast(dict[str, Any], raw_record)

                event_payload: Any = record.get("event")
                recorded_previous_hash: Any = record.get("previous_hash")
                recorded_hash: Any = record.get("hash")

                if not isinstance(event_payload, dict):
                    raise AuditLogError(f"Invalid event payload on line {line_number}.")

                typed_event_payload = cast(
                    dict[str, Any],
                    event_payload,
                )

                validated_event_payload: dict[str, str] = {}

                for key, value in typed_event_payload.items():
                    if not isinstance(value, str):
                        raise AuditLogError(f"Invalid event payload on line {line_number}.")

                    validated_event_payload[key] = value

                if not isinstance(recorded_previous_hash, str):
                    raise AuditLogError(f"Invalid previous hash on line {line_number}.")

                if not isinstance(recorded_hash, str):
                    raise AuditLogError(f"Invalid record hash on line {line_number}.")

                if recorded_previous_hash != previous_hash:
                    raise AuditLogError(f"Broken hash chain on line {line_number}.")

                expected_hash = _digest(
                    validated_event_payload,
                    previous_hash,
                )

                if recorded_hash != expected_hash:
                    raise AuditLogError(f"Hash mismatch on line {line_number}.")

                previous_hash = recorded_hash

    except OSError as exc:
        raise AuditLogError(f"Could not read audit log: {path}") from exc

    return previous_hash


def record_event(path: str | Path, event: AuditEvent) -> None:
    """Append one event after checking the integrity of existing records.

    Use a single writer for a given file. This simple implementation does not
    coordinate concurrent writers across processes.
    """
    audit_path = Path(path)
    previous_hash = _last_hash(audit_path)
    event_payload = _event_payload(event)

    record: dict[str, dict[str, str] | str] = {
        "event": event_payload,
        "previous_hash": previous_hash,
        "hash": _digest(event_payload, previous_hash),
    }

    line = json.dumps(
        record,
        sort_keys=True,
        ensure_ascii=False,
    )

    try:
        audit_path.parent.mkdir(parents=True, exist_ok=True)

        with audit_path.open("a", encoding="utf-8") as audit_file:
            audit_file.write(line + "\n")
            audit_file.flush()
            os.fsync(audit_file.fileno())

    except OSError as exc:
        raise AuditLogError(f"Could not write audit log: {audit_path}") from exc


def verify_log(path: str | Path) -> bool:
    """Return True if the existing audit log's hash chain is valid."""
    audit_path = Path(path)

    if not audit_path.exists():
        raise AuditLogError(f"Audit log does not exist: {audit_path}")

    _last_hash(audit_path)
    return True


__all__ = [
    "AuditLogError",
    "record_event",
    "verify_log",
]
