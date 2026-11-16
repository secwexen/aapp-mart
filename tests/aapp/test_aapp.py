"""Tests for AAPP core data models."""

from typing import Any, MutableMapping, cast

import pytest

from aapp_mart.aapp.analyzer import AttackGraphAnalyzer
from aapp_mart.aapp.models import AttackEdge, AttackGraph, AttackNode, AttackPath, PredictionMode


def create_node(node_id: str) -> AttackNode:
    """Create a valid attack graph node."""
    return AttackNode(
        node_id=node_id,
        name=f"Node {node_id}",
        node_type="asset",
    )


def create_edge(
    edge_id: str,
    source: str,
    target: str,
) -> AttackEdge:
    """Create a valid directed attack graph edge."""
    return AttackEdge(
        edge_id=edge_id,
        source=source,
        target=target,
    )


@pytest.mark.parametrize(
    ("node_id", "name", "node_type"),
    [
        ("", "Node 1", "asset"),
        ("node-1", "", "asset"),
        ("node-1", "Node 1", ""),
    ],
)
def test_attack_node_rejects_empty_fields(
    node_id: str,
    name: str,
    node_type: str,
) -> None:
    """Reject nodes containing empty required fields."""
    with pytest.raises(ValueError):
        AttackNode(
            node_id=node_id,
            name=name,
            node_type=node_type,
        )


def test_attack_node_creation() -> None:
    """Create a valid attack node."""
    node = create_node("node-1")

    assert node.node_id == "node-1"
    assert node.name == "Node node-1"
    assert node.node_type == "asset"
    assert node.attributes == {}


def test_attack_node_attributes_are_immutable() -> None:
    """Prevent external modification of node attributes."""
    attributes: dict[str, Any] = {"environment": "production"}

    node = AttackNode(
        node_id="node-1",
        name="Node 1",
        node_type="asset",
        attributes=attributes,
    )

    attributes["environment"] = "development"

    assert node.attributes["environment"] == "production"

    mutable_attributes = cast(
        MutableMapping[str, Any],
        node.attributes,
    )

    with pytest.raises(TypeError):
        mutable_attributes["environment"] = "development"


def test_attack_edge_creation() -> None:
    """Create a valid directed attack edge."""
    edge = create_edge("edge-1", "node-1", "node-2")

    assert edge.edge_id == "edge-1"
    assert edge.source == "node-1"
    assert edge.target == "node-2"
    assert edge.probability == 1.0


@pytest.mark.parametrize(
    "probability",
    [-0.1, 1.1],
)
def test_attack_edge_rejects_invalid_probability(
    probability: float,
) -> None:
    """Reject probabilities outside the valid range."""
    with pytest.raises(ValueError):
        AttackEdge(
            edge_id="edge-1",
            source="node-1",
            target="node-2",
            probability=probability,
        )


def test_attack_path_creation() -> None:
    """Create a valid ordered attack path."""
    path = AttackPath(
        path_id="path-1",
        node_ids=("node-1", "node-2", "node-3"),
        edge_ids=("edge-1", "edge-2"),
        probability=0.75,
        rationale="A possible attack route.",
    )

    assert path.path_id == "path-1"
    assert len(path.node_ids) == 3
    assert len(path.edge_ids) == 2
    assert path.probability == 0.75


def test_attack_path_rejects_invalid_edge_count() -> None:
    """Reject paths with an incorrect number of edges."""
    with pytest.raises(ValueError):
        AttackPath(
            path_id="path-1",
            node_ids=("node-1", "node-2", "node-3"),
            edge_ids=("edge-1",),
        )


def test_attack_graph_creation() -> None:
    """Create a valid directed attack graph."""
    graph = AttackGraph(
        graph_id="graph-1",
        nodes=(
            create_node("node-1"),
            create_node("node-2"),
            create_node("node-3"),
        ),
        edges=(
            create_edge("edge-1", "node-1", "node-2"),
            create_edge("edge-2", "node-2", "node-3"),
        ),
    )

    assert graph.graph_id == "graph-1"
    assert len(graph.nodes) == 3
    assert len(graph.edges) == 2


def test_attack_graph_rejects_duplicate_node_ids() -> None:
    """Reject graphs containing duplicate node identifiers."""
    with pytest.raises(ValueError, match="duplicate node IDs"):
        AttackGraph(
            graph_id="graph-1",
            nodes=(
                create_node("node-1"),
                create_node("node-1"),
            ),
        )


def test_attack_graph_rejects_duplicate_edge_ids() -> None:
    """Reject graphs containing duplicate edge identifiers."""
    with pytest.raises(ValueError, match="duplicate edge IDs"):
        AttackGraph(
            graph_id="graph-1",
            nodes=(
                create_node("node-1"),
                create_node("node-2"),
            ),
            edges=(
                create_edge("edge-1", "node-1", "node-2"),
                create_edge("edge-1", "node-2", "node-1"),
            ),
        )


def test_attack_graph_rejects_unknown_node_reference() -> None:
    """Reject edges referencing unknown graph nodes."""
    with pytest.raises(ValueError, match="Unknown target node"):
        AttackGraph(
            graph_id="graph-1",
            nodes=(create_node("node-1"),),
            edges=(create_edge("edge-1", "node-1", "node-2"),),
        )


def test_attack_graph_get_node() -> None:
    """Retrieve graph nodes by identifier."""
    node = create_node("node-1")
    graph = AttackGraph(
        graph_id="graph-1",
        nodes=(node,),
    )

    assert graph.get_node("node-1") == node
    assert graph.get_node("unknown") is None


def test_attack_graph_get_edge() -> None:
    """Retrieve graph edges by identifier."""
    edge = create_edge("edge-1", "node-1", "node-2")
    graph = AttackGraph(
        graph_id="graph-1",
        nodes=(
            create_node("node-1"),
            create_node("node-2"),
        ),
        edges=(edge,),
    )

    assert graph.get_edge("edge-1") == edge
    assert graph.get_edge("unknown") is None


def test_attack_graph_outgoing_edges() -> None:
    """Retrieve directed outgoing edges from a node."""
    graph = AttackGraph(
        graph_id="graph-1",
        nodes=(
            create_node("node-1"),
            create_node("node-2"),
            create_node("node-3"),
        ),
        edges=(
            create_edge("edge-1", "node-1", "node-2"),
            create_edge("edge-2", "node-1", "node-3"),
            create_edge("edge-3", "node-2", "node-3"),
        ),
    )

    assert len(graph.outgoing_edges("node-1")) == 2
    assert len(graph.outgoing_edges("node-2")) == 1
    assert not graph.outgoing_edges("node-3")


def test_attack_graph_outgoing_edges_rejects_unknown_node() -> None:
    """Reject outgoing edge queries for unknown nodes."""
    graph = AttackGraph(graph_id="graph-1")

    with pytest.raises(ValueError, match="Unknown node ID"):
        graph.outgoing_edges("unknown")


def test_prediction_modes() -> None:
    """Expose deterministic and probabilistic prediction modes."""
    assert PredictionMode.DETERMINISTIC.value == "deterministic"
    assert PredictionMode.PROBABILISTIC.value == "probabilistic"


def test_analyzer_returns_graph_counts() -> None:
    """Return the correct number of graph nodes and edges."""
    graph = AttackGraph(
        graph_id="graph-1",
        nodes=(
            AttackNode("node-1", "Entry", "host"),
            AttackNode("node-2", "Target", "server"),
        ),
        edges=(AttackEdge("edge-1", "node-1", "node-2"),),
    )

    result = AttackGraphAnalyzer().analyze(graph)

    assert result.graph_id == "graph-1"
    assert result.node_count == 2
    assert result.edge_count == 1


def test_analyzer_identifies_entry_and_terminal_nodes() -> None:
    """Identify nodes without incoming or outgoing edges."""
    graph = AttackGraph(
        graph_id="graph-2",
        nodes=(
            AttackNode("node-1", "Entry", "host"),
            AttackNode("node-2", "Middle", "server"),
            AttackNode("node-3", "Target", "database"),
        ),
        edges=(
            AttackEdge("edge-1", "node-1", "node-2"),
            AttackEdge("edge-2", "node-2", "node-3"),
        ),
    )

    result = AttackGraphAnalyzer().analyze(graph)

    assert result.entry_nodes == ("node-1",)
    assert result.terminal_nodes == ("node-3",)


def test_analyzer_identifies_isolated_nodes() -> None:
    """Identify nodes that are not connected to any edge."""
    graph = AttackGraph(
        graph_id="graph-3",
        nodes=(
            AttackNode("node-1", "Entry", "host"),
            AttackNode("node-2", "Target", "server"),
            AttackNode("node-3", "Isolated", "device"),
        ),
        edges=(AttackEdge("edge-1", "node-1", "node-2"),),
    )

    result = AttackGraphAnalyzer().analyze(graph)

    assert result.isolated_nodes == ("node-3",)


def test_analyzer_finds_reachable_nodes() -> None:
    """Find all nodes reachable from graph entry nodes."""
    graph = AttackGraph(
        graph_id="graph-4",
        nodes=(
            AttackNode("node-1", "Entry", "host"),
            AttackNode("node-2", "Middle", "server"),
            AttackNode("node-3", "Target", "database"),
            AttackNode("node-4", "Isolated", "device"),
        ),
        edges=(
            AttackEdge("edge-1", "node-1", "node-2"),
            AttackEdge("edge-2", "node-2", "node-3"),
        ),
    )

    result = AttackGraphAnalyzer().analyze(graph)

    assert result.reachable_node_ids == (
        "node-1",
        "node-2",
        "node-3",
    )


def test_analyzer_handles_empty_graph() -> None:
    """Handle a graph without nodes or edges."""
    graph = AttackGraph(graph_id="empty-graph")

    result = AttackGraphAnalyzer().analyze(graph)

    assert result.node_count == 0
    assert result.edge_count == 0
    assert not result.entry_nodes
    assert not result.terminal_nodes
    assert not result.isolated_nodes
    assert not result.reachable_node_ids
