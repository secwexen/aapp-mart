from dataclasses import dataclass, field
from typing import Dict, List
import networkx as nx


@dataclass
class Asset:
    """
    Represents an environment asset.
    """

    name: str
    asset_type: str
    criticality: int = 5

    vulnerabilities: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)


class AttackGraphBuilder:
    """
    Builds attack knowledge graphs.
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self.assets: Dict[str, Asset] = {}


    def add_asset(self, asset: Asset):
        """
        Add asset into attack graph.
        """

        self.assets[asset.name] = asset

        self.graph.add_node(
            asset.name,
            type=asset.asset_type,
            criticality=asset.criticality,
            vulnerabilities=asset.vulnerabilities,
            permissions=asset.permissions
        )


    def add_relationship(
        self,
        source: str,
        target: str,
        technique: str,
        risk: float
    ):
        """
        Add attacker movement relationship.

        Example:
        User-PC -> Domain Controller
        Technique: T1021
        """

        self.graph.add_edge(
            source,
            target,
            technique=technique,
            risk=risk
        )


    def get_graph(self):
        """
        Returns generated attack graph.
        """

        return self.graph


    def export_graph(self):
        """
        Export graph into JSON compatible format.
        """

        return nx.node_link_data(self.graph)
