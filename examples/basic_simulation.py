"""Run a deterministic, offline scoring example with synthetic values."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScenarioItem:
    name: str
    impact: int
    likelihood: int


def score(item: ScenarioItem) -> int:
    if not 1 <= item.impact <= 5:
        raise ValueError("impact must be between 1 and 5")
    if not 1 <= item.likelihood <= 5:
        raise ValueError("likelihood must be between 1 and 5")
    return item.impact * item.likelihood


def main() -> None:
    items = [
        ScenarioItem("synthetic-service-a", impact=4, likelihood=3),
        ScenarioItem("synthetic-service-b", impact=2, likelihood=2),
    ]

    print("Offline synthetic risk summary")
    for item in items:
        print(f"- {item.name}: score={score(item)}/25")


if __name__ == "__main__":
    main()
