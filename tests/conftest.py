from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

for path in (str(SRC), str(ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

os.environ.setdefault("PYTHONPATH", str(SRC) + os.pathsep + os.environ.get("PYTHONPATH", ""))

@pytest.fixture(scope="session")
def project_root() -> Path:
    """Repository root."""
    return ROOT

@pytest.fixture(scope="session")
def src_root() -> Path:
    """Source directory."""
    return SRC

@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Alias for project_root for readability."""
    return ROOT
