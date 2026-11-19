"""Tests for the attack graph API route."""

from fastapi.testclient import TestClient

from aapp_mart.api.app import app

client = TestClient(app)


def test_attack_graph_route_is_registered() -> None:
    """Verify that the attack graph endpoint is registered in OpenAPI."""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/attack-graphs/{graph_id}" in response.json()["paths"]
    assert "get" in response.json()["paths"]["/attack-graphs/{graph_id}"]


def test_attack_graph_returns_not_implemented() -> None:
    """Verify that valid graph requests return HTTP 501."""
    response = client.get("/attack-graphs/graph-123")

    assert response.status_code == 501
    assert response.json() == {"detail": "Attack graph retrieval is not implemented yet."}


def test_attack_graph_rejects_blank_graph_id() -> None:
    """Verify that graph identifiers containing only whitespace are rejected."""
    response = client.get("/attack-graphs/%20")

    assert response.status_code == 400
    assert response.json() == {"detail": "Graph ID must not be empty."}
