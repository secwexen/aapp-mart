"""API routes for security risk assessment."""

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(
    prefix="/risks",
    tags=["Risk Assessment"],
)


def _empty_findings() -> list[dict[str, Any]]:
    """Return an empty findings list with an explicit type."""
    return []


class RiskAssessmentRequest(BaseModel):
    """Request schema for security risk assessment."""

    model_config = ConfigDict(extra="forbid")

    subject: str = Field(min_length=1)
    features: dict[str, Any] = Field(default_factory=dict)
    context: dict[str, Any] = Field(default_factory=dict)


class RiskAssessmentResponse(BaseModel):
    """Response schema for security risk assessment."""

    risk_score: float = Field(ge=0.0, le=1.0)
    risk_level: str
    findings: list[dict[str, Any]] = Field(
        default_factory=_empty_findings,
    )
    summary: str


@router.post(
    "/assess",
    response_model=RiskAssessmentResponse,
)
async def assess_risk(
    request: RiskAssessmentRequest,
) -> RiskAssessmentResponse:
    """Accept a security risk assessment request.

    Risk scoring integration will be implemented in a
    subsequent development step.
    """
    raise NotImplementedError("Risk assessment integration has not been implemented yet.")


__all__ = [
    "RiskAssessmentRequest",
    "RiskAssessmentResponse",
    "router",
]
