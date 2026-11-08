from aapp_mart.policy.models import Policy


def normalize_scope_value(value: str) -> str:
    """Normalize an exact-match policy value; wildcard scopes are not supported."""
    normalized = value.strip().casefold()

    if not normalized:
        raise ValueError("Policy values must not be empty.")

    if "*" in normalized:
        raise ValueError("Wildcard policy values are not supported.")

    return normalized


def validate_policy(policy: Policy) -> None:
    """Check policy invariants before the policy is used."""
    if not isinstance(policy.enabled, bool):
        raise ValueError("'enabled' must be a boolean.")

    for target in policy.allowed_targets:
        normalize_scope_value(target)

    for action in policy.allowed_actions:
        normalize_scope_value(action)
