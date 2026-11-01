from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

for entry in (str(SRC), str(ROOT)):
    if entry not in sys.path:
        sys.path.insert(0, entry)


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Repository root for tests needing project-relative paths."""
    return ROOT
