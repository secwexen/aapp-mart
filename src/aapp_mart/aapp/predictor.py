"""Prediction engine abstraction for AAPP."""

from __future__ import annotations

from typing import Protocol

from aapp_mart.aapp.models import PredictionMode
from aapp_mart.engine.contracts import PredictionRequest, PredictionResult


class PredictionBackend(Protocol):
    """Contract for prediction model implementations."""

    # pylint: disable=too-few-public-methods

    def predict(
        self,
        request: PredictionRequest,
        mode: PredictionMode,
    ) -> PredictionResult:
        """Generate a prediction using the selected prediction mode."""
        ...


class PredictionBackendNotConfiguredError(RuntimeError):
    """Raised when no prediction backend has been configured."""


class PredictionExecutionError(RuntimeError):
    """Raised when prediction execution produces an invalid result."""


class Predictor:
    """Coordinate prediction requests through a configurable backend."""

    def __init__(
        self,
        backend: PredictionBackend | None = None,
    ) -> None:
        """Initialize the predictor with an optional prediction backend."""
        self._backend = backend

    @property
    def backend(self) -> PredictionBackend | None:
        """Return the configured prediction backend."""
        return self._backend

    def predict(
        self,
        request: PredictionRequest,
        mode: PredictionMode = PredictionMode.DETERMINISTIC,
    ) -> PredictionResult:
        """Execute a prediction using the configured backend."""
        if self._backend is None:
            raise PredictionBackendNotConfiguredError(
                "No prediction backend is configured; configure a backend before executing predictions."
            )

        result = self._backend.predict(request, mode)

        if result.subject != request.subject:
            raise PredictionExecutionError("Prediction result subject does not match the request subject.")

        return result


__all__ = [
    "PredictionBackend",
    "PredictionBackendNotConfiguredError",
    "PredictionExecutionError",
    "Predictor",
]
