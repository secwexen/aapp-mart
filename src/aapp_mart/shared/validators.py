from __future__ import annotations

from typing import Any


def require_non_empty_string(value: Any, field_name: str) -> str:
    """Validate that a field is a non-empty string."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string.")
    clean = value.strip()
    if not clean:
        raise ValueError(f"{field_name} must not be empty.")
    return clean


def require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    """Validate that a field is a dictionary-like mapping."""
    if not isinstance(value, dict):
        raise TypeError(f"{field_name} must be a mapping.")
    return value


def require_list(value: Any, field_name: str) -> list[Any]:
    """Validate that a field is a list."""
    if not isinstance(value, list):
        raise TypeError(f"{field_name} must be a list.")
    return value
