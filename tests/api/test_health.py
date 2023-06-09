from fastapi.testclient import TestClient
from server.app import create_app

client = TestClient(create_app())


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
