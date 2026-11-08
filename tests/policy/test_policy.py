from aapp_mart.policy.evaluator import evaluate
from aapp_mart.policy.models import Decision, Policy, PolicyRequest


def make_policy() -> Policy:
    return Policy(
        allowed_targets=frozenset({"staging.example.test"}),
        allowed_actions=frozenset({"read_only_check"}),
    )


def test_allows_authorized_request_in_scope() -> None:
    result = evaluate(
        make_policy(),
        PolicyRequest(
            target="staging.example.test",
            action="read_only_check",
            authorization_reference="approval-123",
        ),
    )

    assert result.decision is Decision.ALLOW
    assert result.reason == "request_in_scope"


def test_denies_target_outside_scope() -> None:
    result = evaluate(
        make_policy(),
        PolicyRequest(
            target="other.example.test",
            action="read_only_check",
            authorization_reference="approval-123",
        ),
    )

    assert result.decision is Decision.DENY
    assert result.reason == "target_not_in_scope"


def test_denies_request_without_authorization_reference() -> None:
    result = evaluate(
        make_policy(),
        PolicyRequest(
            target="staging.example.test",
            action="read_only_check",
            authorization_reference=" ",
        ),
    )

    assert result.decision is Decision.DENY
    assert result.reason == "missing_authorization_reference"


def test_denies_action_not_in_allowlist() -> None:
    result = evaluate(
        make_policy(),
        PolicyRequest(
            target="staging.example.test",
            action="unlisted_action",
            authorization_reference="approval-123",
        ),
    )

    assert result.decision is Decision.DENY
    assert result.reason == "action_not_permitted"
