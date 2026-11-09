"""Read the bundled synthetic JSON sample and print a local risk summary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_sample(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not load sample input: {path}") from exc

    if not isinstance(data, dict):
        raise ValueError("Sample input must contain a JSON object.")

    assets = data.get("assets")
    if not isinstance(assets, list):
        raise ValueError("'assets' must be a JSON list.")

    for asset in assets:
        if not isinstance(asset, dict):
            raise ValueError("Each asset must be a JSON object.")
        if not isinstance(asset.get("id"), str):
            raise ValueError("Each asset must have a string 'id'.")
        for field in ("impact", "likelihood"):
            value = asset.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
                raise ValueError(f"Each asset must have an integer '{field}' from 1 to 5.")

    return data


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    sample_path = root / "data" / "samples" / "example_input.json"
    sample = load_sample(sample_path)

    results = [
        {
            "id": asset["id"],
            "score": asset["impact"] * asset["likelihood"],
        }
        for asset in sample["assets"]
    ]

    print(json.dumps(
        {
            "scenario_id": sample.get("scenario_id", "unknown"),
            "status": "completed",
            "results": results,
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()
