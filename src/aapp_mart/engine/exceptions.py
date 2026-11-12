"""Exception hierarchy for core contract and execution failures."""

from __future__ import annotations


class AAPPMartError(Exception):
    """Base class for expected AAPP-MART core errors."""


class ContractValidationError(AAPPMartError, ValueError):
    """Raised when a request or result violates a core contract."""


class ComponentNotRegisteredError(AAPPMartError):
    """Raised when ENGINE cannot resolve a requested component."""


class ExecutionError(AAPPMartError):
    """Raised when a component execution fails unexpectedly."""

    def __init__(
        self,
        message: str,
        *,
        execution_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.execution_id = execution_id
