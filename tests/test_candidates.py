from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_candidate():
    response = client.post(
        "/api/candidates",
        json={
            "full_name": "Test Candidate",
            "email": "test@example.com",
            "training_track": "Python",
            "is_active": True
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["full_name"] == "Test Candidate"
    assert data["email"] == "test@example.com"


def test_missing_candidate():
    response = client.get("/api/candidates/999999")

    assert response.status_code == 404