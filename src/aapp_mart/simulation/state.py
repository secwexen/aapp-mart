"""Simulation lifecycle state definitions."""

from enum import Enum


class SimulationState(str, Enum):
    """Represent the lifecycle states of a simulation."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
