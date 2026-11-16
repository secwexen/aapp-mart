"""Structural attack graph analysis for AAPP."""

from __future__ import annotations

from dataclasses import dataclass

from aapp_mart.aapp.models import AttackGraph


@dataclass(frozen=True, slots=True)
class AttackGraphAnalysis:
    """Immutable structural analysis result for an attack graph."""

    graph_id: str
    node_count: int
    edge_count: int
    entry_nodes: tuple[str, ...]
    terminal_nodes: tuple[str, ...]
    isolated_nodes: tuple[str, ...]
    reachable_node_ids: tuple[str, ...]


class AttackGraphAnalyzer:
    """Analyze the structural properties of an attack graph."""

    # pylint: disable=too-few-public-methods

    def analyze(self, graph: AttackGraph) -> AttackGraphAnalysis:
        """Analyze graph structure without predicting attack behavior."""
        outgoing_node_ids: set[str] = {edge.source for edge in graph.edges}
        incoming_node_ids: set[str] = {edge.target for edge in graph.edges}

        entry_nodes: tuple[str, ...] = tuple(
            sorted(node.node_id for node in graph.nodes if node.node_id not in incoming_node_ids)
        )

        terminal_nodes: tuple[str, ...] = tuple(
            sorted(node.node_id for node in graph.nodes if node.node_id not in outgoing_node_ids)
        )

        isolated_nodes: tuple[str, ...] = tuple(
            sorted(
                node.node_id
                for node in graph.nodes
                if node.node_id not in incoming_node_ids and node.node_id not in outgoing_node_ids
            )
        )

        reachable_node_ids: tuple[str, ...] = self._find_reachable_nodes(graph, entry_nodes)

        return AttackGraphAnalysis(
            graph_id=graph.graph_id,
            node_count=len(graph.nodes),
            edge_count=len(graph.edges),
            entry_nodes=entry_nodes,
            terminal_nodes=terminal_nodes,
            isolated_nodes=isolated_nodes,
            reachable_node_ids=reachable_node_ids,
        )

    @staticmethod
    def _find_reachable_nodes(
        graph: AttackGraph,
        entry_nodes: tuple[str, ...],
    ) -> tuple[str, ...]:
        """Find nodes reachable from entry nodes through graph edges."""
        visited: set[str] = set()
        pending: list[str] = [node_id for node_id in entry_nodes if graph.outgoing_edges(node_id)]

        while pending:
            node_id = pending.pop()

            if node_id in visited:
                continue

            visited.add(node_id)

            for edge in graph.outgoing_edges(node_id):
                if edge.target not in visited:
                    pending.append(edge.target)

        return tuple(sorted(visited))


__all__ = [
    "AttackGraphAnalysis",
    "AttackGraphAnalyzer",
]
