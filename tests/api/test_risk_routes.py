"""Tests for the security risk assessment API route."""

from fastapi.testclient import TestClient

from aapp_mart.api.app import app

client = TestClient(app, raise_server_exceptions=False)


def test_risk_route_is_registered() -> None:
    """Verify that the risk assessment endpoint is registered in OpenAPI."""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/risks/assess" in response.json()["paths"]
    assert "post" in response.json()["paths"]["/risks/assess"]


def test_risk_assessment_returns_not_implemented() -> None:
    """Verify that valid risk assessment requests reach the unimplemented route."""
    payload: dict[str, object] = {
        "subject": "staging.example.test",
        "features": {},
        "context": {},
    }

    response = client.post("/risks/assess", json=payload)

    assert response.status_code == 500
    assert response.text == "Internal Server Error"


def test_risk_assessment_rejects_invalid_request() -> None:
    """Verify that invalid risk assessment requests fail schema validation."""
    response = client.post("/risks/assess", json={})

    assert response.status_code == 422


def test_risk_assessment_rejects_additional_fields() -> None:
    """Verify that additional request fields are rejected."""
    payload: dict[str, object] = {
        "subject": "staging.example.test",
        "features": {},
        "context": {},
        "unexpected": "value",
    }

    response = client.post("/risks/assess", json=payload)

    assert response.status_code == 422
