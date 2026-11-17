"""MART agent state definitions."""

from enum import Enum


class AgentState(str, Enum):
    """Represent the lifecycle states of a MART agent."""

    IDLE = "idle"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    DISABLED = "disabled"
