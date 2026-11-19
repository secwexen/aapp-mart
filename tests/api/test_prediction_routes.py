"""Tests for the AAPP prediction API route."""

from fastapi.testclient import TestClient

from aapp_mart.api.app import app

client = TestClient(app, raise_server_exceptions=False)


def test_prediction_route_is_registered() -> None:
    """Verify that the prediction endpoint is registered in OpenAPI."""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/predictions/" in response.json()["paths"]
    assert "post" in response.json()["paths"]["/predictions/"]


def test_prediction_returns_service_unavailable_when_pipeline_is_unavailable() -> None:
    """Verify structured error handling when the execution pipeline is unavailable."""
    payload: dict[str, object] = {
        "subject": "staging.example.test",
        "features": {},
        "objective": "assess_attack_paths",
        "model_name": "default",
        "deterministic": True,
        "seed": 42,
    }

    response = client.post("/predictions/", json=payload)

    assert response.status_code == 503
    assert response.json() == {
        "detail": {
            "error": "execution_pipeline_unavailable",
            "message": "The execution pipeline is not available.",
        }
    }


def test_prediction_rejects_invalid_request() -> None:
    """Verify that invalid prediction requests fail schema validation."""
    response = client.post("/predictions/", json={})

    assert response.status_code == 422
