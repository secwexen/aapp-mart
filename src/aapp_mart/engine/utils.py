"""Shared utility functions for the AAPP-MART core engine."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any

from aapp_mart.engine.contracts import ExecutionRequest


def utc_now() -> datetime:
    """Return the current timezone-aware UTC timestamp."""

    return datetime.now(timezone.utc)


def ensure_timezone_aware(value: datetime) -> datetime:
    """Validate that a datetime contains timezone information."""

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(
            "Datetime value must be timezone-aware."
        )

    return value


def validate_execution_request(
    request: ExecutionRequest,
) -> None:
    """Validate the structure of an execution request."""

    if not isinstance(request, ExecutionRequest):
        raise TypeError(
            "request must be an ExecutionRequest instance."
        )

    if not request.operation.strip():
        raise ValueError(
            "Execution operation must not be empty."
        )

    if not request.metadata.correlation_id.strip():
        raise ValueError(
            "Execution correlation ID must not be empty."
        )

    if request.timeout_seconds is not None:
        if request.timeout_seconds <= 0:
            raise ValueError(
                "Execution timeout must be greater than zero."
            )

    if request.deterministic and request.seed is None:
        raise ValueError(
            "Deterministic execution requires a seed."
        )


def normalize_error(error: Exception) -> dict[str, str]:
    """Convert an exception into a normalized error structure."""

    return {
        "type": type(error).__name__,
        "message": str(error) or "An unexpected execution error occurred.",
    }


def derive_seed(
    base_seed: int,
    namespace: str,
) -> int:
    """Derive a reproducible seed for a named execution component."""

    if not isinstance(base_seed, int):
        raise TypeError("base_seed must be an integer.")

    if not namespace.strip():
        raise ValueError("namespace must not be empty.")

    seed_material = f"{base_seed}:{namespace}".encode("utf-8")

    digest = hashlib.blake2b(
        seed_material,
        digest_size=8,
    ).digest()

    return int.from_bytes(digest, byteorder="big")
