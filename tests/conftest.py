from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

# Make both repo root and src importable to tests
for path in (str(SRC), str(ROOT)):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

# Ensure PYTHONPATH also includes src for subprocesses / tools
pythonpath = os.environ.get("PYTHONPATH", "")
paths = [str(SRC)]
if pythonpath:
    paths.append(pythonpath)
os.environ["PYTHONPATH"] = os.pathsep.join(paths)

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
