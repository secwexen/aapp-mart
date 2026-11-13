"""Runtime execution context and environment management."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from threading import Event, RLock
from typing import Any, Mapping
from uuid import UUID

from aapp_mart.engine.contracts import (
    ComponentName,
    ContractMetadata,
    ExecutionRequest,
)
from aapp_mart.engine.utils import derive_seed


@dataclass(slots=True)
class ExecutionContext:
    """Hold runtime information for a single execution."""

    execution_id: UUID
    component: ComponentName
    metadata: ContractMetadata
    deterministic: bool
    seed: int | None
    created_at: datetime
    timeout_seconds: float | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    _cancel_event: Event = field(
        default_factory=Event,
        repr=False,
    )
    _lock: RLock = field(
        default_factory=RLock,
        repr=False,
    )

    def __post_init__(self) -> None:
        """Validate runtime context invariants."""

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        if self.deterministic and self.seed is None:
            raise ValueError(
                "Deterministic execution requires a seed"
            )

        if (
            self.timeout_seconds is not None
            and self.timeout_seconds <= 0
        ):
            raise ValueError(
                "timeout_seconds must be greater than zero"
            )

    @classmethod
    def from_request(
        cls,
        request: ExecutionRequest,
    ) -> ExecutionContext:
        """Create a runtime context from an execution request."""

        return cls(
            execution_id=request.execution_id,
            component=request.component,
            metadata=request.metadata,
            deterministic=request.deterministic,
            seed=request.seed,
            created_at=datetime.now(timezone.utc),
            timeout_seconds=request.timeout_seconds,
        )

    @property
    def correlation_id(self) -> str:
        """Return the execution correlation identifier."""

        return self.metadata.correlation_id

    @property
    def deadline(self) -> datetime | None:
        """Return the execution deadline when a timeout exists."""

        if self.timeout_seconds is None:
            return None

        return self.created_at + timedelta(
            seconds=self.timeout_seconds
        )

    @property
    def is_cancelled(self) -> bool:
        """Return whether cancellation has been requested."""

        return self._cancel_event.is_set()

    @property
    def is_expired(self) -> bool:
        """Check whether the execution deadline has passed."""

        deadline = self.deadline

        if deadline is None:
            return False

        return datetime.now(timezone.utc) >= deadline

    def request_cancellation(self) -> None:
        """Signal cancellation to the running execution."""

        self._cancel_event.set()

    def wait_for_cancellation(
        self,
        timeout: float | None = None,
    ) -> bool:
        """Wait for cancellation and return whether it was requested."""

        return self._cancel_event.wait(timeout)

    def set_attribute(
        self,
        key: str,
        value: Any,
    ) -> None:
        """Store a runtime-specific attribute."""

        if not key.strip():
            raise ValueError("Attribute key must not be empty")

        with self._lock:
            self.attributes[key] = value

    def get_attribute(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """Retrieve a runtime-specific attribute."""

        with self._lock:
            return self.attributes.get(key, default)

    def derive_component_seed(
        self,
        namespace: str,
    ) -> int:
        """Derive a reproducible seed for a component namespace."""

        if self.seed is None:
            raise ValueError(
                "Cannot derive a seed without a base seed"
            )

        return derive_seed(self.seed, namespace)

    def snapshot_attributes(self) -> Mapping[str, Any]:
        """Return a shallow snapshot of runtime attributes."""

        with self._lock:
            return dict(self.attributes)
