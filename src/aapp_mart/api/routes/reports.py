"""API routes for execution reports."""

from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


class ReportResponse(BaseModel):
    """Response schema for an execution report."""

    model_config = ConfigDict(extra="forbid")

    execution_id: UUID
    component: str
    status: str
    output: dict[str, Any] = Field(default_factory=dict)
    error: dict[str, str] | None = None
    summary: str


@router.get(
    "/{execution_id}",
    response_model=ReportResponse,
)
async def get_execution_report(
    execution_id: UUID,
) -> ReportResponse:
    """Retrieve an execution report by execution ID.

    Report storage and retrieval integration will be implemented
    in a subsequent development step.
    """
    raise HTTPException(
        status_code=501,
        detail="Execution report retrieval is not implemented yet.",
    )


__all__ = [
    "ReportResponse",
    "router",
]
