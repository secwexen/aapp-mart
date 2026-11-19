"""Pydantic schemas for the AAPP-MART API."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from aapp_mart.engine.contracts import ComponentName, ExecutionStatus


class APIBaseModel(BaseModel):
    """Base model for API request and response schemas."""

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
    )


class HealthResponse(APIBaseModel):
    """Response schema for the health endpoint."""

    status: str
    service: str


class PredictionRequestSchema(APIBaseModel):
    """API request schema for AAPP prediction."""

    subject: str = Field(min_length=1)
    features: dict[str, Any] = Field(default_factory=dict)
    objective: str = Field(min_length=1)
    model_name: str | None = None
    deterministic: bool = True
    seed: int | None = Field(default=0, strict=True)


class PredictionResponseSchema(APIBaseModel):
    """API response schema for AAPP prediction."""

    subject: str
    predicted_paths: list[dict[str, Any]]
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str
    metadata: "ContractMetadataSchema"


class SimulationRequestSchema(APIBaseModel):
    """API request schema for MART simulation."""

    scenario: str = Field(min_length=1)
    target: str = Field(min_length=1)
    parameters: dict[str, Any] = Field(default_factory=dict)
    seed: int | None = Field(default=0, strict=True)
    deterministic: bool = True


class SimulationResponseSchema(APIBaseModel):
    """API response schema for MART simulation."""

    scenario: str
    events: list[dict[str, Any]]
    summary: dict[str, Any]
    started_at: datetime
    completed_at: datetime
    metadata: "ContractMetadataSchema"


class ContractMetadataSchema(APIBaseModel):
    """Response schema for shared contract metadata."""

    correlation_id: str
    created_at: datetime
    schema_version: str
    labels: dict[str, str]


class ExecutionResponseSchema(APIBaseModel):
    """Unified API response schema for execution results."""

    execution_id: UUID
    component: ComponentName
    status: ExecutionStatus
    output: dict[str, Any] = Field(default_factory=dict)
    error: dict[str, str] | None = None
    started_at: datetime | None = None
    completed_at: datetime
    metadata: ContractMetadataSchema | None = None


__all__ = [
    "APIBaseModel",
    "ContractMetadataSchema",
    "ExecutionResponseSchema",
    "HealthResponse",
    "PredictionRequestSchema",
    "PredictionResponseSchema",
    "SimulationRequestSchema",
    "SimulationResponseSchema",
]
