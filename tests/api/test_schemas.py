"""Tests for AAPP-MART API Pydantic schemas."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from aapp_mart.api.schemas import (
    ContractMetadataSchema,
    ExecutionResponseSchema,
    HealthResponse,
    PredictionRequestSchema,
    PredictionResponseSchema,
    SimulationRequestSchema,
    SimulationResponseSchema,
)
from aapp_mart.engine.contracts import ComponentName, ExecutionStatus


def get_component() -> ComponentName:
    """Return a valid component enum member."""
    return next(iter(ComponentName.__members__.values()))


def create_metadata() -> ContractMetadataSchema:
    """Create valid contract metadata for schema tests."""
    return ContractMetadataSchema(
        correlation_id="test-correlation-id",
        created_at=datetime.now(UTC),
        schema_version="1.0",
        labels={"source": "test"},
    )


def test_health_response_accepts_valid_data() -> None:
    """Verify that valid health response data is accepted."""
    response = HealthResponse(
        status="ok",
        service="aapp-mart",
    )

    assert response.status == "ok"
    assert response.service == "aapp-mart"


def test_health_response_rejects_extra_fields() -> None:
    """Verify that unexpected health response fields are rejected."""
    with pytest.raises(ValueError):
        HealthResponse.model_validate(
            {
                "status": "ok",
                "service": "aapp-mart",
                "unexpected": "value",
            }
        )


def test_contract_metadata_accepts_valid_data() -> None:
    """Verify that valid contract metadata is accepted."""
    metadata = create_metadata()

    assert metadata.correlation_id == "test-correlation-id"
    assert metadata.schema_version == "1.0"
    assert metadata.labels == {"source": "test"}


def test_prediction_request_accepts_valid_data() -> None:
    """Verify that valid prediction request data is accepted."""
    request = PredictionRequestSchema(
        subject="test-host",
        features={"exposed_ports": [22, 443]},
        objective="identify_attack_paths",
        model_name="test-model",
        deterministic=True,
        seed=42,
    )

    assert request.subject == "test-host"
    assert request.seed == 42
    assert request.deterministic is True


@pytest.mark.parametrize("field", ["subject", "objective"])
def test_prediction_request_rejects_empty_required_fields(
    field: str,
) -> None:
    """Verify that empty required prediction fields are rejected."""
    data: dict[str, object] = {
        "subject": "test-host",
        "features": {},
        "objective": "identify_attack_paths",
    }
    data[field] = ""

    with pytest.raises(ValueError):
        PredictionRequestSchema.model_validate(data)


def test_prediction_request_rejects_boolean_seed() -> None:
    """Verify that boolean values are rejected as prediction seeds."""
    with pytest.raises(ValueError):
        PredictionRequestSchema.model_validate(
            {
                "subject": "test-host",
                "objective": "identify_attack_paths",
                "seed": True,
            }
        )


def test_prediction_response_accepts_valid_data() -> None:
    """Verify that valid prediction response data is accepted."""
    response = PredictionResponseSchema(
        subject="test-host",
        predicted_paths=[{"path": ["entry", "target"]}],
        confidence=0.85,
        rationale="Test prediction",
        metadata=create_metadata(),
    )

    assert response.subject == "test-host"
    assert response.confidence == 0.85
    assert len(response.predicted_paths) == 1


@pytest.mark.parametrize("confidence", [-0.1, 1.1])
def test_prediction_response_rejects_invalid_confidence(
    confidence: float,
) -> None:
    """Verify that confidence values outside the valid range are rejected."""
    with pytest.raises(ValueError):
        PredictionResponseSchema(
            subject="test-host",
            predicted_paths=[],
            confidence=confidence,
            rationale="Test prediction",
            metadata=create_metadata(),
        )


def test_simulation_request_accepts_valid_data() -> None:
    """Verify that valid simulation request data is accepted."""
    request = SimulationRequestSchema(
        scenario="network_intrusion",
        target="test-network",
        parameters={"max_steps": 5},
        seed=123,
        deterministic=True,
    )

    assert request.scenario == "network_intrusion"
    assert request.target == "test-network"
    assert request.seed == 123


@pytest.mark.parametrize("field", ["scenario", "target"])
def test_simulation_request_rejects_empty_required_fields(
    field: str,
) -> None:
    """Verify that empty required simulation fields are rejected."""
    data: dict[str, object] = {
        "scenario": "network_intrusion",
        "target": "test-network",
        "parameters": {},
    }
    data[field] = ""

    with pytest.raises(ValueError):
        SimulationRequestSchema.model_validate(data)


def test_simulation_request_rejects_boolean_seed() -> None:
    """Verify that boolean values are rejected as simulation seeds."""
    with pytest.raises(ValueError):
        SimulationRequestSchema.model_validate(
            {
                "scenario": "network_intrusion",
                "target": "test-network",
                "seed": True,
            }
        )


def test_simulation_response_accepts_valid_data() -> None:
    """Verify that valid simulation response data is accepted."""
    started_at = datetime.now(UTC)
    completed_at = datetime.now(UTC)

    response = SimulationResponseSchema(
        scenario="network_intrusion",
        events=[{"type": "discovery", "target": "test-host"}],
        summary={"completed_steps": 1},
        started_at=started_at,
        completed_at=completed_at,
        metadata=create_metadata(),
    )

    assert response.scenario == "network_intrusion"
    assert len(response.events) == 1
    assert response.summary["completed_steps"] == 1


def test_execution_response_accepts_valid_data() -> None:
    """Verify that a non-failed execution response is accepted."""
    completed_at = datetime.now(UTC)
    execution_id = uuid4()
    successful_status = next(status for status in ExecutionStatus if status is not ExecutionStatus.FAILED)

    response = ExecutionResponseSchema(
        execution_id=execution_id,
        component=get_component(),
        status=successful_status,
        output={"result": "success"},
        completed_at=completed_at,
        metadata=create_metadata(),
    )

    assert response.execution_id == execution_id
    assert response.status == successful_status
    assert response.error is None


def test_execution_response_accepts_failed_execution() -> None:
    """Verify that a failed execution response accepts error details."""
    response = ExecutionResponseSchema(
        execution_id=uuid4(),
        component=get_component(),
        status=ExecutionStatus.FAILED,
        output={},
        error={
            "type": "ExecutionError",
            "message": "Simulation failed",
        },
        completed_at=datetime.now(UTC),
    )

    assert response.status is ExecutionStatus.FAILED
    assert response.model_dump()["error"] == {
        "type": "ExecutionError",
        "message": "Simulation failed",
    }
