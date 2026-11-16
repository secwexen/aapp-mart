"""Tests for AAPP risk scoring."""

import pytest

from aapp_mart.aapp.models import AttackEdge, AttackGraph, AttackNode, AttackPath
from aapp_mart.aapp.scoring import RiskLevel, RiskScore, RiskScorer


@pytest.fixture(name="scorer")
def fixture_scorer() -> RiskScorer:
    """Provide a risk scorer."""
    return RiskScorer()


@pytest.fixture(name="graph")
def fixture_graph() -> AttackGraph:
    """Provide an attack graph with criticality attributes."""
    return AttackGraph(
        graph_id="graph-001",
        nodes=(
            AttackNode(
                node_id="entry",
                name="Entry Point",
                node_type="external",
                attributes={"criticality": 2},
            ),
            AttackNode(
                node_id="application",
                name="Application Server",
                node_type="server",
                attributes={"criticality": 5},
            ),
            AttackNode(
                node_id="database",
                name="Production Database",
                node_type="database",
                attributes={"criticality": 10},
            ),
        ),
        edges=(
            AttackEdge(
                edge_id="edge-001",
                source="entry",
                target="application",
                probability=0.8,
            ),
            AttackEdge(
                edge_id="edge-002",
                source="application",
                target="database",
                probability=0.9,
            ),
        ),
    )


@pytest.fixture(name="attack_path")
def fixture_attack_path() -> AttackPath:
    """Provide an attack path targeting the production database."""
    return AttackPath(
        path_id="path-001",
        node_ids=("entry", "application", "database"),
        edge_ids=("edge-001", "edge-002"),
        probability=0.8,
        rationale="Test attack path.",
    )


def test_score_path_returns_risk_score(
    scorer: RiskScorer,
    graph: AttackGraph,
    attack_path: AttackPath,
) -> None:
    """Verify that scoring returns a RiskScore."""
    result = scorer.score_path(graph, attack_path)

    assert isinstance(result, RiskScore)
    assert result.graph_id == "graph-001"
    assert result.path_id == "path-001"
    assert result.target_node_id == "database"


def test_score_path_calculates_expected_score(
    scorer: RiskScorer,
    graph: AttackGraph,
    attack_path: AttackPath,
) -> None:
    """Verify the probability and criticality calculation."""
    result = scorer.score_path(graph, attack_path)

    assert result.probability == 0.8
    assert result.criticality == 10.0
    assert result.score == 80.0


def test_score_path_classifies_critical_risk(
    scorer: RiskScorer,
    graph: AttackGraph,
    attack_path: AttackPath,
) -> None:
    """Verify critical risk classification."""
    result = scorer.score_path(graph, attack_path)

    assert result.level == RiskLevel.CRITICAL


@pytest.mark.parametrize(
    ("probability", "criticality", "expected_score", "expected_level"),
    [
        (0.2, 10, 20.0, RiskLevel.LOW),
        (0.5, 5, 25.0, RiskLevel.MEDIUM),
        (0.6, 10, 60.0, RiskLevel.HIGH),
        (0.8, 10, 80.0, RiskLevel.CRITICAL),
        (1.0, 10, 100.0, RiskLevel.CRITICAL),
        (0.0, 10, 0.0, RiskLevel.LOW),
        (1.0, 0, 0.0, RiskLevel.LOW),
    ],
)
def test_score_path_risk_boundaries(
    scorer: RiskScorer,
    probability: float,
    criticality: int,
    expected_score: float,
    expected_level: RiskLevel,
) -> None:
    """Verify score calculation and risk classification boundaries."""
    graph = AttackGraph(
        graph_id="boundary-graph",
        nodes=(
            AttackNode(
                node_id="entry",
                name="Entry",
                node_type="external",
            ),
            AttackNode(
                node_id="target",
                name="Target",
                node_type="server",
                attributes={"criticality": criticality},
            ),
        ),
        edges=(
            AttackEdge(
                edge_id="edge-001",
                source="entry",
                target="target",
            ),
        ),
    )

    path = AttackPath(
        path_id="boundary-path",
        node_ids=("entry", "target"),
        edge_ids=("edge-001",),
        probability=probability,
    )

    result = scorer.score_path(graph, path)

    assert result.score == expected_score
    assert result.level == expected_level


def test_score_path_rejects_missing_criticality(
    scorer: RiskScorer,
) -> None:
    """Verify that missing criticality is rejected."""
    graph = AttackGraph(
        graph_id="graph-002",
        nodes=(
            AttackNode("entry", "Entry", "external"),
            AttackNode("target", "Target", "server"),
        ),
        edges=(AttackEdge("edge-001", "entry", "target"),),
    )

    path = AttackPath(
        path_id="path-002",
        node_ids=("entry", "target"),
        edge_ids=("edge-001",),
    )

    with pytest.raises(
        ValueError,
        match="criticality",
    ):
        scorer.score_path(graph, path)


@pytest.mark.parametrize(
    "criticality",
    [
        -1,
        11,
        float("inf"),
        float("-inf"),
        float("nan"),
        True,
        "high",
        None,
    ],
)
def test_score_path_rejects_invalid_criticality(
    scorer: RiskScorer,
    criticality: object,
) -> None:
    """Verify that invalid criticality values are rejected."""
    graph = AttackGraph(
        graph_id="graph-003",
        nodes=(
            AttackNode("entry", "Entry", "external"),
            AttackNode(
                "target",
                "Target",
                "server",
                attributes={"criticality": criticality},
            ),
        ),
        edges=(AttackEdge("edge-001", "entry", "target"),),
    )

    path = AttackPath(
        path_id="path-003",
        node_ids=("entry", "target"),
        edge_ids=("edge-001",),
    )

    with pytest.raises(ValueError):
        scorer.score_path(graph, path)


def test_score_path_rejects_unknown_node(
    scorer: RiskScorer,
    graph: AttackGraph,
) -> None:
    """Verify that unknown path nodes are rejected."""
    path = AttackPath(
        path_id="path-004",
        node_ids=("entry", "unknown"),
        edge_ids=("edge-001",),
    )

    with pytest.raises(
        ValueError,
        match="unknown node",
    ):
        scorer.score_path(graph, path)


def test_score_path_rejects_unknown_edge(
    scorer: RiskScorer,
    graph: AttackGraph,
) -> None:
    """Verify that unknown path edges are rejected."""
    path = AttackPath(
        path_id="path-005",
        node_ids=("entry", "application"),
        edge_ids=("unknown-edge",),
    )

    with pytest.raises(
        ValueError,
        match="unknown edge",
    ):
        scorer.score_path(graph, path)


def test_score_path_rejects_inconsistent_edge(
    scorer: RiskScorer,
    graph: AttackGraph,
) -> None:
    """Verify that incorrectly connected edges are rejected."""
    path = AttackPath(
        path_id="path-006",
        node_ids=("entry", "database"),
        edge_ids=("edge-001",),
    )

    with pytest.raises(
        ValueError,
        match="does not connect",
    ):
        scorer.score_path(graph, path)


def test_score_path_is_deterministic(
    scorer: RiskScorer,
    graph: AttackGraph,
    attack_path: AttackPath,
) -> None:
    """Verify identical inputs produce identical results."""
    first_result = scorer.score_path(graph, attack_path)
    second_result = scorer.score_path(graph, attack_path)

    assert first_result == second_result


def test_score_path_uses_target_node_criticality(
    scorer: RiskScorer,
    graph: AttackGraph,
) -> None:
    """Verify that the final target determines asset criticality."""
    path = AttackPath(
        path_id="path-007",
        node_ids=("entry", "application"),
        edge_ids=("edge-001",),
        probability=0.8,
    )

    result = scorer.score_path(graph, path)

    assert result.target_node_id == "application"
    assert result.criticality == 5.0
    assert result.score == 40.0
    assert result.level == RiskLevel.MEDIUM
