"""Central constants and enumerations for the AAPP-MART engine.

This module defines shared enumerations, severity weights, and default configuration values used across the application.
"""

from enum import StrEnum


class Severity(StrEnum):
    """Represent standardized security severity levels."""

    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AssetType(StrEnum):
    """Define supported infrastructure asset categories."""

    ENDPOINT = "ENDPOINT"
    SERVER = "SERVER"
    DATABASE = "DATABASE"
    NETWORK = "NETWORK"
    IDENTITY = "IDENTITY"
    CLOUD = "CLOUD"
    BACKUP = "BACKUP"


class SimulationStatus(StrEnum):
    """Represent the lifecycle states of a simulation."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


# Normalized weights used by the risk assessment engine.
SEVERITY_WEIGHTS: dict[Severity, float] = {
    Severity.INFO: 0.0,
    Severity.LOW: 1.0,
    Severity.MEDIUM: 3.0,
    Severity.HIGH: 6.0,
    Severity.CRITICAL: 10.0,
}

# Global risk score boundaries.
MAX_RISK_SCORE: float = 10.0

# Attack graph analysis limits.
DEFAULT_MAX_PATHS: int = 20
DEFAULT_MAX_PATH_DEPTH: int = 8
