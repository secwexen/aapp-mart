"""API routes for attack graph representation."""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(
    prefix="/attack-graphs",
    tags=["Attack Graphs"],
)


def _empty_nodes() -> list["AttackGraphNode"]:
    """Return an empty list of attack graph nodes."""
    return []


def _empty_edges() -> list["AttackGraphEdge"]:
    """Return an empty list of attack graph edges."""
    return []


class AttackGraphNode(BaseModel):
    """A node in an attack graph."""

    model_config = ConfigDict(extra="forbid")

    node_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    node_type: str = Field(min_length=1)
    properties: dict[str, Any] = Field(default_factory=dict)


class AttackGraphEdge(BaseModel):
    """A directed connection between attack graph nodes."""

    model_config = ConfigDict(extra="forbid")

    source: str = Field(min_length=1)
    target: str = Field(min_length=1)
    relationship: str = Field(min_length=1)
    properties: dict[str, Any] = Field(default_factory=dict)


class AttackGraphResponse(BaseModel):
    """Response schema for an attack graph."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str
    nodes: list[AttackGraphNode] = Field(default_factory=_empty_nodes)
    edges: list[AttackGraphEdge] = Field(default_factory=_empty_edges)
    metadata: dict[str, Any] = Field(default_factory=dict)


@router.get(
    "/{graph_id}",
    response_model=AttackGraphResponse,
)
async def get_attack_graph(
    graph_id: str,
) -> AttackGraphResponse:
    """Retrieve an attack graph by its identifier.

    Attack graph generation and retrieval integration will be
    implemented in a subsequent development step.
    """
    if not graph_id.strip():
        raise HTTPException(
            status_code=400,
            detail="Graph ID must not be empty.",
        )

    raise HTTPException(
        status_code=501,
        detail="Attack graph retrieval is not implemented yet.",
    )


__all__ = [
    "AttackGraphEdge",
    "AttackGraphNode",
    "AttackGraphResponse",
    "router",
]
