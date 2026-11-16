"""Core data models for AAPP attack graph analysis and prediction."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any


class PredictionMode(StrEnum):
    """Supported attack path prediction modes."""

    DETERMINISTIC = "deterministic"
    PROBABILISTIC = "probabilistic"


@dataclass(frozen=True, slots=True)
class AttackNode:
    """Represent a system asset or security entity in an attack graph."""

    node_id: str
    name: str
    node_type: str
    attributes: Mapping[str, Any] = field(default_factory=dict[str, Any])

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise ValueError("node_id must not be empty.")

        if not self.name.strip():
            raise ValueError("name must not be empty.")

        if not self.node_type.strip():
            raise ValueError("node_type must not be empty.")

        object.__setattr__(
            self,
            "attributes",
            MappingProxyType(dict(self.attributes)),
        )


@dataclass(frozen=True, slots=True)
class AttackEdge:
    """Represent a directed relationship between two attack graph nodes."""

    edge_id: str
    source: str
    target: str
    probability: float = 1.0
    technique_id: str | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict[str, Any])

    def __post_init__(self) -> None:
        if not self.edge_id.strip():
            raise ValueError("edge_id must not be empty.")

        if not self.source.strip():
            raise ValueError("source must not be empty.")

        if not self.target.strip():
            raise ValueError("target must not be empty.")

        if not 0.0 <= self.probability <= 1.0:
            raise ValueError("probability must be between 0 and 1.")

        if self.technique_id is not None and not self.technique_id.strip():
            raise ValueError("technique_id must not be empty.")

        object.__setattr__(
            self,
            "attributes",
            MappingProxyType(dict(self.attributes)),
        )


@dataclass(frozen=True, slots=True)
class AttackPath:
    """Represent an ordered attack path through a directed graph."""

    path_id: str
    node_ids: tuple[str, ...]
    edge_ids: tuple[str, ...]
    probability: float = 1.0
    rationale: str = ""

    def __post_init__(self) -> None:
        if not self.path_id.strip():
            raise ValueError("path_id must not be empty.")

        if len(self.node_ids) < 2:
            raise ValueError("An attack path must contain at least two nodes.")

        if len(self.edge_ids) != len(self.node_ids) - 1:
            raise ValueError("" "An attack path must contain exactly one edge " + "between consecutive nodes.")

        if any(not node_id.strip() for node_id in self.node_ids):
            raise ValueError("node_ids must not contain empty values.")

        if any(not edge_id.strip() for edge_id in self.edge_ids):
            raise ValueError("edge_ids must not contain empty values.")

        if not 0.0 <= self.probability <= 1.0:
            raise ValueError("probability must be between 0 and 1.")


@dataclass(frozen=True, slots=True)
class AttackGraph:
    """Represent a directed attack graph containing nodes and edges."""

    graph_id: str
    nodes: tuple[AttackNode, ...] = ()
    edges: tuple[AttackEdge, ...] = ()

    def __post_init__(self) -> None:
        if not self.graph_id.strip():
            raise ValueError("graph_id must not be empty.")

        node_ids = [node.node_id for node in self.nodes]
        edge_ids = [edge.edge_id for edge in self.edges]

        if len(node_ids) != len(set(node_ids)):
            raise ValueError("Attack graph contains duplicate node IDs.")

        if len(edge_ids) != len(set(edge_ids)):
            raise ValueError("Attack graph contains duplicate edge IDs.")

        known_nodes = set(node_ids)

        for edge in self.edges:
            if edge.source not in known_nodes:
                raise ValueError(f"Unknown source node '{edge.source}' " f"referenced by edge '{edge.edge_id}'.")

            if edge.target not in known_nodes:
                raise ValueError(f"Unknown target node '{edge.target}' " f"referenced by edge '{edge.edge_id}'.")

    def get_node(self, node_id: str) -> AttackNode | None:
        """Return a node by its identifier."""

        return next(
            (node for node in self.nodes if node.node_id == node_id),
            None,
        )

    def get_edge(self, edge_id: str) -> AttackEdge | None:
        """Return an edge by its identifier."""

        return next(
            (edge for edge in self.edges if edge.edge_id == edge_id),
            None,
        )

    def outgoing_edges(self, node_id: str) -> tuple[AttackEdge, ...]:
        """Return all directed edges originating from a node."""

        if self.get_node(node_id) is None:
            raise ValueError(f"Unknown node ID '{node_id}'.")

        return tuple(edge for edge in self.edges if edge.source == node_id)
