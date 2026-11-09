from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RuntimeContext:
    run_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
    state: dict[str, Any] = field(default_factory=dict)
