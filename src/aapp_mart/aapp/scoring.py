"""Risk scoring implementation for AAPP attack paths."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite

from aapp_mart.aapp.models import AttackGraph, AttackPath


class RiskLevel(StrEnum):
    """Risk severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class RiskScore:
    """Represent the calculated risk score of an attack path."""

    graph_id: str
    path_id: str
    target_node_id: str
    probability: float
    criticality: float
    score: float
    level: RiskLevel


class RiskScorer:
    """Calculate deterministic risk scores for attack paths."""

    # pylint: disable=too-few-public-methods

    MIN_CRITICALITY = 0.0
    MAX_CRITICALITY = 10.0
    MAX_SCORE = 100.0

    def score_path(
        self,
        graph: AttackGraph,
        path: AttackPath,
    ) -> RiskScore:
        """Calculate the risk score for an attack path."""
        target_node_id = self._validate_path(graph, path)

        target_node = graph.get_node(target_node_id)

        if target_node is None:
            raise ValueError(f"Unknown target node '{target_node_id}'.")

        criticality = target_node.attributes.get("criticality")

        if isinstance(criticality, bool) or not isinstance(criticality, (int, float)):
            raise ValueError("Target node must define a numeric criticality attribute.")

        if not isfinite(criticality):
            raise ValueError("Criticality must be a finite number.")

        if not self.MIN_CRITICALITY <= criticality <= self.MAX_CRITICALITY:
            raise ValueError("Criticality must be between 0 and 10.")

        probability = path.probability

        score = probability * criticality * self.MAX_SCORE / self.MAX_CRITICALITY

        score = round(score, 2)

        return RiskScore(
            graph_id=graph.graph_id,
            path_id=path.path_id,
            target_node_id=target_node_id,
            probability=probability,
            criticality=float(criticality),
            score=score,
            level=self._classify_risk(score),
        )

    @staticmethod
    def _validate_path(
        graph: AttackGraph,
        path: AttackPath,
    ) -> str:
        """Validate that an attack path belongs to the supplied graph."""
        for node_id in path.node_ids:
            if graph.get_node(node_id) is None:
                raise ValueError(f"Attack path references unknown node '{node_id}'.")

        for index, edge_id in enumerate(path.edge_ids):
            edge = graph.get_edge(edge_id)

            if edge is None:
                raise ValueError(f"Attack path references unknown edge '{edge_id}'.")

            expected_source = path.node_ids[index]
            expected_target = path.node_ids[index + 1]

            if edge.source != expected_source or edge.target != expected_target:
                raise ValueError(f"Edge '{edge_id}' does not connect " f"'{expected_source}' to '{expected_target}'.")

        return path.node_ids[-1]

    @staticmethod
    def _classify_risk(score: float) -> RiskLevel:
        """Classify a numerical risk score."""
        if score < 25.0:
            return RiskLevel.LOW

        if score < 50.0:
            return RiskLevel.MEDIUM

        if score < 75.0:
            return RiskLevel.HIGH

        return RiskLevel.CRITICAL


__all__ = [
    "RiskLevel",
    "RiskScore",
    "RiskScorer",
]
