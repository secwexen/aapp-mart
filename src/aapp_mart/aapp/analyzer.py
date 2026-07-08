from typing import List, Dict
import networkx as nx


class AttackPathAnalyzer:

    def __init__(self, graph: nx.DiGraph):

        self.graph = graph



    def calculate_path_risk(
        self,
        path: List[str]
    ) -> float:
        """
        Calculates accumulated attack path risk.
        """

        risk = 0

        for index in range(len(path)-1):

            edge = self.graph[
                path[index]
            ][
                path[index+1]
            ]

            risk += edge.get(
                "risk",
                1
            )


        return round(risk,2)



    def predict_attack_paths(
        self,
        attacker_start: str,
        target: str,
        limit: int = 5
    ):

        """
        Predict possible attack paths.
        """

        paths = []

        try:

            all_paths = nx.all_simple_paths(
                self.graph,
                attacker_start,
                target
            )


            for path in all_paths:

                paths.append(
                    {
                        "path": path,
                        "risk": self.calculate_path_risk(path)
                    }
                )


        except nx.NetworkXNoPath:

            return []


        paths.sort(
            key=lambda x:x["risk"],
            reverse=True
        )


        return paths[:limit]



    def find_critical_assets(
        self,
        threshold:int = 8
    ):

        """
        Finds high-value assets.
        """

        critical=[]


        for node,data in self.graph.nodes(data=True):

            if data.get(
                "criticality",
                0
            ) >= threshold:

                critical.append(
                    {
                        "asset":node,
                        "criticality":
                        data["criticality"]
                    }
                )


        return critical
