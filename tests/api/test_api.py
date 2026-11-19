"""Tests for the AAPP-MART API application."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from aapp_mart.api.app import app

client = TestClient(app)


def test_api_app_is_fastapi_instance() -> None:
    """Verify that the API application is a FastAPI instance."""
    assert isinstance(app, FastAPI)


def test_health_endpoint_returns_success() -> None:
    """Verify the health endpoint response."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "aapp-mart",
    }


def test_openapi_contains_registered_endpoints() -> None:
    """Verify that all expected API endpoints are registered."""
    response = client.get("/openapi.json")

    assert response.status_code == 200

    paths = response.json()["paths"]

    expected_paths = {
        "/health",
        "/predictions/",
        "/simulations/",
        "/risks/assess",
        "/reports/{execution_id}",
        "/attack-graphs/{graph_id}",
    }

    assert expected_paths.issubset(paths.keys())
