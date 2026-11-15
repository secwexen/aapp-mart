"""Load and validate policy definitions from YAML files."""

from pathlib import Path
from typing import Any, cast

import yaml

from aapp_mart.policy.models import Policy
from aapp_mart.policy.rules import validate_policy


class PolicyFileError(ValueError):
    """Raised when a policy file is missing, malformed, or invalid."""


def _read_string_list(data: dict[str, Any], key: str) -> frozenset[str]:
    """Read and validate a list of strings from policy data."""

    value = data.get(key)

    if not isinstance(value, list):
        raise PolicyFileError(f"'{key}' must be a list of strings.")

    items = cast(list[object], value)

    if any(not isinstance(item, str) for item in items):
        raise PolicyFileError(f"Every item in '{key}' must be a string.")

    return frozenset(cast(list[str], items))


def load_policy(path: str | Path) -> Policy:
    """Load a policy from YAML without performing network or system actions."""

    policy_path = Path(path)

    try:
        text = policy_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise PolicyFileError(f"Could not read policy file: {policy_path}") from exc

    try:
        parsed: object = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise PolicyFileError("Policy file contains invalid YAML.") from exc

    if not isinstance(parsed, dict):
        raise PolicyFileError("Policy file must contain a YAML object.")

    raw_data = cast(dict[object, object], parsed)

    if any(not isinstance(key, str) for key in raw_data):
        raise PolicyFileError("Policy field names must be strings.")

    data = cast(dict[str, Any], raw_data)

    allowed_keys = {"enabled", "allowed_targets", "allowed_actions"}
    unknown_keys: set[str] = set(data) - allowed_keys

    if unknown_keys:
        names = ", ".join(sorted(unknown_keys))
        raise PolicyFileError(f"Unknown policy field(s): {names}")

    enabled: object = data.get("enabled", True)

    if not isinstance(enabled, bool):
        raise PolicyFileError("'enabled' must be a boolean.")

    policy = Policy(
        allowed_targets=_read_string_list(data, "allowed_targets"),
        allowed_actions=_read_string_list(data, "allowed_actions"),
        enabled=enabled,
    )

    try:
        validate_policy(policy)
    except ValueError as exc:
        raise PolicyFileError(str(exc)) from exc

    return policy
