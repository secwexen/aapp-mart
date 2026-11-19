"""Tests for the execution reports API route."""

from uuid import uuid4

from fastapi.testclient import TestClient

from aapp_mart.api.app import app

client = TestClient(app)


def test_report_route_is_registered() -> None:
    """Verify that the execution report endpoint is registered in OpenAPI."""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/reports/{execution_id}" in response.json()["paths"]
    assert "get" in response.json()["paths"]["/reports/{execution_id}"]


def test_report_returns_not_implemented() -> None:
    """Verify that report retrieval returns HTTP 501."""
    execution_id = uuid4()

    response = client.get(f"/reports/{execution_id}")

    assert response.status_code == 501
    assert response.json() == {"detail": "Execution report retrieval is not implemented yet."}


def test_report_rejects_invalid_execution_id() -> None:
    """Verify that invalid execution IDs are rejected."""
    response = client.get("/reports/invalid-uuid")

    assert response.status_code == 422
