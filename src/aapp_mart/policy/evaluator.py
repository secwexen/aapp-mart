from aapp_mart.policy.models import Decision, Policy, PolicyRequest, PolicyResult


def _normalize(value: str) -> str:
    return value.strip().casefold()


def evaluate(policy: Policy, request: PolicyRequest) -> PolicyResult:
    """Allow only explicitly scoped requests with an authorization reference.

    Target matching is exact after trimming whitespace and case normalization.
    Wildcards and implicit subdomain matching are intentionally unsupported.
    """
    if not policy.enabled:
        return PolicyResult(Decision.DENY, "policy_disabled")

    target = _normalize(request.target)
    action = _normalize(request.action)
    authorization_reference = request.authorization_reference.strip()

    if not target:
        return PolicyResult(Decision.DENY, "missing_target")

    if not action:
        return PolicyResult(Decision.DENY, "missing_action")

    if not authorization_reference:
        return PolicyResult(Decision.DENY, "missing_authorization_reference")

    allowed_targets = {_normalize(item) for item in policy.allowed_targets}
    if target not in allowed_targets:
        return PolicyResult(Decision.DENY, "target_not_in_scope")

    allowed_actions = {_normalize(item) for item in policy.allowed_actions}
    if action not in allowed_actions:
        return PolicyResult(Decision.DENY, "action_not_permitted")

    return PolicyResult(Decision.ALLOW, "request_in_scope")
