"""AAPP prediction orchestration and execution component."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, cast

from aapp_mart.aapp.feature_pipeline import FeaturePipeline
from aapp_mart.aapp.models import PredictionMode
from aapp_mart.aapp.predictor import Predictor
from aapp_mart.engine.contracts import (
    ComponentName,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
    PredictionRequest,
    PredictionResult,
)


class Prediction:
    """Coordinate AAPP prediction through shared execution contracts."""

    def __init__(
        self,
        predictor: Predictor | None = None,
        feature_pipeline: FeaturePipeline | None = None,
    ) -> None:
        """Initialize the AAPP prediction component."""
        self._predictor = predictor or Predictor()
        self._feature_pipeline = feature_pipeline or FeaturePipeline()

    @property
    def component_name(self) -> ComponentName:
        """Return the component identifier used by ENGINE."""
        return ComponentName.AAPP

    def predict(
        self,
        request: PredictionRequest,
        mode: PredictionMode = PredictionMode.DETERMINISTIC,
    ) -> PredictionResult:
        """Prepare features and execute an AAPP prediction."""
        prepared_features = self._feature_pipeline.transform(request.features)

        prepared_request = PredictionRequest(
            subject=request.subject,
            features=prepared_features,
            objective=request.objective,
            metadata=request.metadata,
            model_name=request.model_name,
        )

        return self._predictor.predict(
            prepared_request,
            mode,
        )

    def execute(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        """Execute an AAPP operation through the ENGINE contract."""
        started_at = datetime.now(timezone.utc)

        try:
            if request.component != ComponentName.AAPP:
                raise ValueError("Execution request component must be AAPP.")

            if request.operation != "predict":
                raise ValueError(f"Unsupported AAPP operation: {request.operation}")

            prediction_request = self._build_prediction_request(request)

            mode = PredictionMode(
                request.payload.get(
                    "mode",
                    PredictionMode.DETERMINISTIC.value,
                )
            )

            result = self.predict(
                prediction_request,
                mode,
            )

            return ExecutionResult(
                execution_id=request.execution_id,
                component=ComponentName.AAPP,
                status=ExecutionStatus.SUCCEEDED,
                output=self._serialize_prediction_result(result),
                started_at=started_at,
                completed_at=datetime.now(timezone.utc),
                metadata=request.metadata,
            )

        except Exception as exc:  # pylint: disable=broad-exception-caught
            return ExecutionResult(
                execution_id=request.execution_id,
                component=ComponentName.AAPP,
                status=ExecutionStatus.FAILED,
                error={
                    "type": type(exc).__name__,
                    "message": str(exc),
                },
                started_at=started_at,
                completed_at=datetime.now(timezone.utc),
                metadata=request.metadata,
            )

    @staticmethod
    def _build_prediction_request(
        request: ExecutionRequest,
    ) -> PredictionRequest:
        """Build a prediction request from an ENGINE execution request."""
        payload = request.payload

        subject = payload.get("subject")
        objective = payload.get("objective")
        features = payload.get("features")

        if not isinstance(subject, str):
            raise ValueError("Prediction subject must be a string.")

        if not isinstance(objective, str):
            raise ValueError("Prediction objective must be a string.")

        if not isinstance(features, Mapping):
            raise ValueError("Prediction features must be a mapping.")

        typed_features = cast(
            Mapping[str, Any],
            features,
        )

        model_name = payload.get("model_name")

        if model_name is not None and not isinstance(model_name, str):
            raise ValueError("Prediction model_name must be a string.")

        return PredictionRequest(
            subject=subject,
            features=typed_features,
            objective=objective,
            metadata=request.metadata,
            model_name=model_name,
        )

    @staticmethod
    def _serialize_prediction_result(
        result: PredictionResult,
    ) -> Mapping[str, Any]:
        """Convert a prediction result into the ENGINE output mapping."""
        return {
            "subject": result.subject,
            "predicted_paths": result.predicted_paths,
            "confidence": result.confidence,
            "rationale": result.rationale,
        }


__all__ = ["Prediction"]
