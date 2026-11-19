"""Tests for the AAPP prediction API route."""

from typing import Any

from fastapi.testclient import TestClient

from aapp_mart.api.app import app


def test_prediction_route_is_registered() -> None:
    """Verify that the prediction endpoint is registered in OpenAPI."""
    with TestClient(app) as client:
        response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/predictions/" in response.json()["paths"]
    assert "post" in response.json()["paths"]["/predictions/"]


def test_prediction_executes_through_engine_pipeline() -> None:
    """Verify that prediction requests are processed through ENGINE."""
    payload: dict[str, Any] = {
        "subject": "staging.example.test",
        "features": {},
        "objective": "assess_attack_paths",
        "model_name": "default",
        "deterministic": True,
        "seed": 42,
    }

    with TestClient(app, raise_server_exceptions=False) as client:
        pipeline = app.state.execution_pipeline

        assert pipeline is not None

        response = client.post("/predictions/", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert result["execution_id"]
    assert result["component"] == "aapp"
    assert result["status"] == "failed"

    assert result["error"]["type"] == "PredictionBackendNotConfiguredError"


def test_prediction_returns_service_unavailable_when_pipeline_is_unavailable() -> None:
    """Verify the API response when the execution pipeline is unavailable."""
    payload: dict[str, Any] = {
        "subject": "staging.example.test",
        "features": {},
        "objective": "assess_attack_paths",
        "model_name": "default",
        "deterministic": True,
        "seed": 42,
    }

    with TestClient(app, raise_server_exceptions=False) as client:
        app.state.execution_pipeline = None

        response = client.post("/predictions/", json=payload)

    assert response.status_code == 503
    assert response.json() == {
        "detail": {
            "error": "execution_pipeline_unavailable",
            "message": "The execution pipeline is not available.",
        }
    }


def test_prediction_rejects_invalid_request() -> None:
    """Verify that invalid prediction requests are rejected."""
    with TestClient(app) as client:
        response = client.post("/predictions/", json={})

    assert response.status_code == 422


__all__ = [
    "test_prediction_route_is_registered",
    "test_prediction_executes_through_engine_pipeline",
    "test_prediction_returns_service_unavailable_when_pipeline_is_unavailable",
    "test_prediction_rejects_invalid_request",
]
