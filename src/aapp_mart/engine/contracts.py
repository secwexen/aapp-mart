"""Core execution contracts shared by AAPP, MART, and ENGINE."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Mapping, Protocol, Sequence
from uuid import UUID, uuid4


class ComponentName(StrEnum):
    """Names of the core execution components."""

    AAPP = "aapp"
    MART = "mart"
    ENGINE = "engine"


class ExecutionStatus(StrEnum):
    """Lifecycle states exposed by the core execution contract."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class ContractMetadata:
    """Common metadata attached to requests and results."""

    correlation_id: str
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    schema_version: str = "1.0"
    labels: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.correlation_id.strip():
            raise ValueError("correlation_id must not be empty")

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        if not self.schema_version.strip():
            raise ValueError("schema_version must not be empty")


@dataclass(frozen=True, slots=True)
class ExecutionRequest:
    """Immutable request submitted to the core execution engine."""

    component: ComponentName
    operation: str
    payload: Mapping[str, Any]
    metadata: ContractMetadata
    execution_id: UUID = field(default_factory=uuid4)
    timeout_seconds: float | None = None
    deterministic: bool = True
    seed: int | None = 0

    def __post_init__(self) -> None:
        if not self.operation.strip():
            raise ValueError("operation must not be empty")

        if (
            self.timeout_seconds is not None
            and self.timeout_seconds <= 0
        ):
            raise ValueError(
                "timeout_seconds must be greater than zero"
            )

        if self.deterministic and self.seed is None:
            raise ValueError(
                "deterministic execution requires a seed"
            )


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """Normalized result returned by AAPP, MART, or ENGINE."""

    execution_id: UUID
    component: ComponentName
    status: ExecutionStatus
    output: Mapping[str, Any] = field(default_factory=dict)
    error: Mapping[str, str] | None = None
    started_at: datetime | None = None
    completed_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: ContractMetadata | None = None

    def __post_init__(self) -> None:
        if self.completed_at.tzinfo is None:
            raise ValueError(
                "completed_at must be timezone-aware"
            )

        if (
            self.started_at is not None
            and self.started_at.tzinfo is None
        ):
            raise ValueError(
                "started_at must be timezone-aware"
            )

        if (
            self.status is ExecutionStatus.FAILED
            and not self.error
        ):
            raise ValueError(
                "failed results must include error details"
            )

        if (
            self.status is not ExecutionStatus.FAILED
            and self.error is not None
        ):
            raise ValueError(
                "only failed results may include error details"
            )


@dataclass(frozen=True, slots=True)
class PredictionRequest:
    """Input contract for an AAPP prediction operation."""

    subject: str
    features: Mapping[str, Any]
    objective: str
    metadata: ContractMetadata
    model_name: str | None = None

    def __post_init__(self) -> None:
        if not self.subject.strip():
            raise ValueError("subject must not be empty")

        if not self.objective.strip():
            raise ValueError("objective must not be empty")


@dataclass(frozen=True, slots=True)
class PredictionResult:
    """Output contract for an AAPP prediction operation."""

    subject: str
    predicted_paths: Sequence[Mapping[str, Any]]
    confidence: float
    rationale: str
    metadata: ContractMetadata

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "confidence must be between 0 and 1"
            )

        if not self.rationale.strip():
            raise ValueError("rationale must not be empty")


@dataclass(frozen=True, slots=True)
class SimulationRequest:
    """Input contract for a MART simulation operation."""

    scenario: str
    target: str
    parameters: Mapping[str, Any]
    metadata: ContractMetadata
    seed: int = 0

    def __post_init__(self) -> None:
        if not self.scenario.strip():
            raise ValueError("scenario must not be empty")

        if not self.target.strip():
            raise ValueError("target must not be empty")


@dataclass(frozen=True, slots=True)
class SimulationResult:
    """Output contract for a MART simulation operation."""

    scenario: str
    events: Sequence[Mapping[str, Any]]
    summary: Mapping[str, Any]
    started_at: datetime
    completed_at: datetime
    metadata: ContractMetadata

    def __post_init__(self) -> None:
        if (
            self.started_at.tzinfo is None
            or self.completed_at.tzinfo is None
        ):
            raise ValueError(
                "simulation timestamps must be timezone-aware"
            )

        if self.completed_at < self.started_at:
            raise ValueError(
                "completed_at cannot precede started_at"
            )


class ExecutionComponent(Protocol):
    """Protocol implemented by an executable core component."""

    @property
    def component_name(self) -> ComponentName:
        """Return the component identifier."""

    def execute(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        """Execute a request and return a normalized result."""


class AAPPInterface(Protocol):
    """Public boundary exposed by the AAPP prediction component."""

    def predict(
        self,
        request: PredictionRequest,
    ) -> PredictionResult:
        """Produce a prediction without asserting real-world compromise."""


class MARTInterface(Protocol):
    """Public boundary exposed by the MART simulation component."""

    def simulate(
        self,
        request: SimulationRequest,
    ) -> SimulationResult:
        """Run a bounded simulation and return its observed events."""


class EngineInterface(Protocol):
    """Public orchestration boundary exposed by ENGINE."""

    def submit(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        """Submit and execute a normalized component request."""


def new_contract_metadata(
    correlation_id: str | None = None,
    *,
    labels: Mapping[str, str] | None = None,
) -> ContractMetadata:
    """Create metadata with a generated correlation ID when omitted."""

    return ContractMetadata(
        correlation_id=correlation_id or str(uuid4()),
        labels=dict(labels or {}),
    )
