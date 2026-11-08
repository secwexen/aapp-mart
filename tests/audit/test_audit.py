import json

import pytest

from aapp_mart.audit import (
    AuditLogError,
    AuditOutcome,
    create_event,
    record_event,
    verify_log,
)


def test_records_and_verifies_event(tmp_path) -> None:
    log_path = tmp_path / "audit.jsonl"
    event = create_event(
        actor="test-user",
        action="read_only_check",
        target="staging.example.test",
        outcome=AuditOutcome.ALLOWED,
        reason="request_in_scope",
    )

    record_event(log_path, event)

    assert verify_log(log_path) is True
    record = json.loads(log_path.read_text(encoding="utf-8").splitlines()[0])
    assert record["event"]["event_id"] == event.event_id
    assert record["event"]["outcome"] == "allowed"


def test_detects_modified_record(tmp_path) -> None:
    log_path = tmp_path / "audit.jsonl"
    event = create_event(
        actor="test-user",
        action="read_only_check",
        target="staging.example.test",
        outcome=AuditOutcome.DENIED,
        reason="target_not_in_scope",
    )
    record_event(log_path, event)

    contents = log_path.read_text(encoding="utf-8")
    log_path.write_text(
        contents.replace("staging.example.test", "changed.example.test"),
        encoding="utf-8",
    )

    with pytest.raises(AuditLogError, match="Hash mismatch"):
        verify_log(log_path)


def test_rejects_event_without_actor() -> None:
    with pytest.raises(ValueError, match="actor"):
        create_event(
            actor=" ",
            action="read_only_check",
            target="staging.example.test",
            outcome=AuditOutcome.ALLOWED,
            reason="request_in_scope",
        )


def test_does_not_append_if_existing_log_is_tampered(tmp_path) -> None:
    log_path = tmp_path / "audit.jsonl"
    event = create_event(
        actor="test-user",
        action="read_only_check",
        target="staging.example.test",
        outcome=AuditOutcome.ALLOWED,
        reason="request_in_scope",
    )
    record_event(log_path, event)

    log_path.write_text("invalid json\n", encoding="utf-8")

    another_event = create_event(
        actor="test-user",
        action="read_only_check",
        target="staging.example.test",
        outcome=AuditOutcome.DENIED,
        reason="test",
    )
    with pytest.raises(AuditLogError):
        record_event(log_path, another_event)
