from dataclasses import dataclass
from enum import StrEnum


class Decision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True, slots=True)
class Policy:
    """An explicit allowlist for authorized assessment targets and actions."""

    allowed_targets: frozenset[str]
    allowed_actions: frozenset[str]
    enabled: bool = True


@dataclass(frozen=True, slots=True)
class PolicyRequest:
    """A proposed action to evaluate; this model does not execute it."""

    target: str
    action: str
    authorization_reference: str


@dataclass(frozen=True, slots=True)
class PolicyResult:
    decision: Decision
    reason: str
