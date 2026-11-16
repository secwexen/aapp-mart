"""Tests for the AAPP prediction component."""

from collections.abc import Mapping
from typing import Any
from uuid import uuid4

import pytest

from aapp_mart.aapp.feature_pipeline import FeaturePipeline
from aapp_mart.aapp.models import PredictionMode
from aapp_mart.aapp.prediction import Prediction
from aapp_mart.aapp.predictor import PredictionBackendNotConfiguredError, Predictor
from aapp_mart.engine.contracts import (
    ComponentName,
    ContractMetadata,
    ExecutionRequest,
    ExecutionStatus,
    PredictionRequest,
    PredictionResult,
)

# pylint: disable=redefined-outer-name


class MockPredictionBackend:
    """Provide deterministic prediction results for testing."""

    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        self.last_request: PredictionRequest | None = None
        self.last_mode: PredictionMode | None = None

    def predict(
        self,
        request: PredictionRequest,
        mode: PredictionMode,
    ) -> PredictionResult:
        """Return a controlled prediction result."""
        self.last_request = request
        self.last_mode = mode

        return PredictionResult(
            subject=request.subject,
            predicted_paths=(
                {
                    "path_id": "path-001",
                    "nodes": ("entry", "target"),
                },
            ),
            confidence=0.85,
            rationale="Mock prediction result.",
            metadata=request.metadata,
        )


@pytest.fixture
def metadata() -> ContractMetadata:
    """Provide prediction metadata."""
    return ContractMetadata(
        correlation_id="test-correlation-001",
    )


@pytest.fixture
def backend() -> MockPredictionBackend:
    """Provide a mock prediction backend."""
    return MockPredictionBackend()


@pytest.fixture
def prediction(
    backend: MockPredictionBackend,
) -> Prediction:
    """Provide an initialized prediction component."""
    return Prediction(
        predictor=Predictor(backend=backend),
        feature_pipeline=FeaturePipeline(),
    )


@pytest.fixture
def prediction_request(
    metadata: ContractMetadata,
) -> PredictionRequest:
    """Provide a prediction request."""
    return PredictionRequest(
        subject="server-01",
        features={
            "hostname": "server-01",
            "port": 443,
            "is_external": True,
        },
        objective="Identify potential attack paths.",
        metadata=metadata,
    )


def test_prediction_initialization(
    prediction: Prediction,
) -> None:
    """Initialize the prediction component."""
    assert prediction.component_name == ComponentName.AAPP


def test_prediction_with_deterministic_mode(
    prediction: Prediction,
    prediction_request: PredictionRequest,
    backend: MockPredictionBackend,
) -> None:
    """Execute a deterministic prediction."""
    result = prediction.predict(
        prediction_request,
        PredictionMode.DETERMINISTIC,
    )

    assert result.subject == prediction_request.subject
    assert result.confidence == 0.85
    assert backend.last_mode == PredictionMode.DETERMINISTIC


def test_prediction_with_probabilistic_mode(
    prediction: Prediction,
    prediction_request: PredictionRequest,
    backend: MockPredictionBackend,
) -> None:
    """Execute a probabilistic prediction."""
    result = prediction.predict(
        prediction_request,
        PredictionMode.PROBABILISTIC,
    )

    assert result.subject == prediction_request.subject
    assert backend.last_mode == PredictionMode.PROBABILISTIC


def test_prediction_prepares_features(
    prediction: Prediction,
    prediction_request: PredictionRequest,
    backend: MockPredictionBackend,
) -> None:
    """Prepare and sort features before prediction."""
    prediction.predict(prediction_request)

    assert backend.last_request is not None
    assert list(backend.last_request.features) == [
        "hostname",
        "is_external",
        "port",
    ]


def test_prediction_preserves_request_metadata(
    prediction: Prediction,
    prediction_request: PredictionRequest,
    backend: MockPredictionBackend,
) -> None:
    """Preserve metadata during prediction preparation."""
    prediction.predict(prediction_request)

    assert backend.last_request is not None
    assert backend.last_request.metadata == prediction_request.metadata


def test_prediction_without_backend_raises_error(
    prediction_request: PredictionRequest,
) -> None:
    """Reject prediction when no backend is configured."""
    prediction = Prediction()

    with pytest.raises(PredictionBackendNotConfiguredError):
        prediction.predict(prediction_request)


def test_prediction_engine_execution(
    prediction: Prediction,
    metadata: ContractMetadata,
) -> None:
    """Execute prediction through the ENGINE contract."""
    execution_request = ExecutionRequest(
        component=ComponentName.AAPP,
        operation="predict",
        payload={
            "subject": "server-01",
            "objective": "Identify potential attack paths.",
            "features": {
                "hostname": "server-01",
                "port": 443,
            },
            "mode": "deterministic",
        },
        metadata=metadata,
    )

    result = prediction.execute(execution_request)

    assert result.execution_id == execution_request.execution_id
    assert result.component == ComponentName.AAPP
    assert result.status == ExecutionStatus.SUCCEEDED
    assert result.output["subject"] == "server-01"
    assert result.error is None


def test_prediction_engine_execution_with_probabilistic_mode(
    prediction: Prediction,
    metadata: ContractMetadata,
) -> None:
    """Execute probabilistic prediction through ENGINE."""
    execution_request = ExecutionRequest(
        component=ComponentName.AAPP,
        operation="predict",
        payload={
            "subject": "server-01",
            "objective": "Identify potential attack paths.",
            "features": {"port": 443},
            "mode": "probabilistic",
        },
        metadata=metadata,
    )

    result = prediction.execute(execution_request)

    assert result.status == ExecutionStatus.SUCCEEDED
    assert result.output["subject"] == "server-01"


def test_prediction_engine_execution_without_backend(
    metadata: ContractMetadata,
) -> None:
    """Return a failed execution result without a backend."""
    prediction = Prediction()

    execution_request = ExecutionRequest(
        component=ComponentName.AAPP,
        operation="predict",
        payload={
            "subject": "server-01",
            "objective": "Identify potential attack paths.",
            "features": {"port": 443},
        },
        metadata=metadata,
    )

    result = prediction.execute(execution_request)

    assert result.status == ExecutionStatus.FAILED
    assert result.error is not None
    assert result.error["type"] == "PredictionBackendNotConfiguredError"


def test_prediction_rejects_wrong_component(
    prediction: Prediction,
    metadata: ContractMetadata,
) -> None:
    """Reject execution requests for another component."""
    execution_request = ExecutionRequest(
        component=ComponentName.MART,
        operation="predict",
        payload={},
        metadata=metadata,
    )

    result = prediction.execute(execution_request)

    assert result.status == ExecutionStatus.FAILED
    assert result.error is not None
    assert result.error["type"] == "ValueError"


def test_prediction_rejects_unsupported_operation(
    prediction: Prediction,
    metadata: ContractMetadata,
) -> None:
    """Reject unsupported AAPP operations."""
    execution_request = ExecutionRequest(
        component=ComponentName.AAPP,
        operation="unsupported",
        payload={},
        metadata=metadata,
    )

    result = prediction.execute(execution_request)

    assert result.status == ExecutionStatus.FAILED
    assert result.error is not None
    assert result.error["type"] == "ValueError"


@pytest.mark.parametrize(
    ("payload", "expected_message"),
    [
        (
            {
                "objective": "Identify attack paths.",
                "features": {},
            },
            "Prediction subject must be a string.",
        ),
        (
            {
                "subject": "server-01",
                "features": {},
            },
            "Prediction objective must be a string.",
        ),
        (
            {
                "subject": "server-01",
                "objective": "Identify attack paths.",
                "features": [],
            },
            "Prediction features must be a mapping.",
        ),
        (
            {
                "subject": "server-01",
                "objective": "Identify attack paths.",
                "features": {},
                "model_name": 123,
            },
            "Prediction model_name must be a string.",
        ),
    ],
)
def test_prediction_rejects_invalid_payload(
    prediction: Prediction,
    metadata: ContractMetadata,
    payload: Mapping[str, Any],
    expected_message: str,
) -> None:
    """Reject invalid prediction payload values."""
    execution_request = ExecutionRequest(
        component=ComponentName.AAPP,
        operation="predict",
        payload=payload,
        metadata=metadata,
    )

    result = prediction.execute(execution_request)

    assert result.status == ExecutionStatus.FAILED
    assert result.error is not None
    assert result.error["message"] == expected_message


def test_prediction_result_contains_execution_timestamps(
    prediction: Prediction,
    metadata: ContractMetadata,
) -> None:
    """Include execution timestamps in the result."""
    execution_request = ExecutionRequest(
        component=ComponentName.AAPP,
        operation="predict",
        payload={
            "subject": "server-01",
            "objective": "Identify potential attack paths.",
            "features": {},
        },
        metadata=metadata,
    )

    result = prediction.execute(execution_request)

    assert result.started_at is not None
    assert result.completed_at is not None
    assert result.completed_at >= result.started_at


def test_prediction_preserves_execution_id(
    prediction: Prediction,
    metadata: ContractMetadata,
) -> None:
    """Preserve the execution identifier."""
    execution_id = uuid4()

    execution_request = ExecutionRequest(
        component=ComponentName.AAPP,
        operation="predict",
        payload={
            "subject": "server-01",
            "objective": "Identify potential attack paths.",
            "features": {},
        },
        metadata=metadata,
        execution_id=execution_id,
    )

    result = prediction.execute(execution_request)

    assert result.execution_id == execution_id
