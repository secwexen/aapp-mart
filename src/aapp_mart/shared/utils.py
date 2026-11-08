from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def normalize_name(value: Any, *, field_name: str) -> str:
    """Normalize names by trimming whitespace and lowercasing."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a str.")

    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty.")

    return normalized.casefold()


def flatten(items: Iterable[Iterable[Any]]) -> list[Any]:
    """Flatten one level of nested iterables."""
    result: list[Any] = []
    for group in items:
        result.extend(group)
    return result
