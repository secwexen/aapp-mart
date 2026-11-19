"""Tests for the MART simulation API route."""

from fastapi.testclient import TestClient

from aapp_mart.api.app import app

client = TestClient(app, raise_server_exceptions=False)


def test_simulation_route_is_registered() -> None:
    """Verify that the simulation endpoint is registered in OpenAPI."""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/simulations/" in response.json()["paths"]
    assert "post" in response.json()["paths"]["/simulations/"]


def test_simulation_returns_not_implemented() -> None:
    """Verify that simulation requests report the unimplemented integration."""
    payload: dict[str, object] = {
        "scenario": "staging_assessment",
        "target": "staging.example.test",
        "parameters": {},
        "seed": 42,
        "deterministic": True,
    }

    response = client.post("/simulations/", json=payload)

    assert response.status_code == 500
    assert response.text == "Internal Server Error"


def test_simulation_rejects_invalid_request() -> None:
    """Verify that invalid simulation requests fail schema validation."""
    response = client.post("/simulations/", json={})

    assert response.status_code == 422
