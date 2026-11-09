"""Demonstrate a passive agent that ranks synthetic records only."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    label: str
    impact: int
    likelihood: int


class PassiveRiskAgent:
    def rank(self, candidates: list[Candidate]) -> list[Candidate]:
        for candidate in candidates:
            if not 1 <= candidate.impact <= 5:
                raise ValueError(f"{candidate.label}: impact must be between 1 and 5")
            if not 1 <= candidate.likelihood <= 5:
                raise ValueError(f"{candidate.label}: likelihood must be between 1 and 5")

        return sorted(
            candidates,
            key=lambda item: item.impact * item.likelihood,
            reverse=True,
        )


def main() -> None:
    agent = PassiveRiskAgent()
    ranked = agent.rank(
        [
            Candidate("synthetic-service-a", impact=4, likelihood=3),
            Candidate("synthetic-service-b", impact=2, likelihood=2),
        ]
    )

    for position, candidate in enumerate(ranked, start=1):
        print(
            f"{position}. {candidate.label}: "
            f"{candidate.impact * candidate.likelihood}/25"
        )


if __name__ == "__main__":
    main()
