from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_status():
    candidate_response = client.post(
        "/api/candidates",
        json={
            "full_name": "Status Test Candidate",
            "email": "status-test@example.com",
            "training_track": "Python",
            "is_active": True
        }
    )

    candidate = candidate_response.json()

    response = client.post(
        "/api/statuses",
        json={
            "candidate_id": candidate["id"],
            "status_date": "2026-08-21",
            "work_completed": "Implemented API testing",
            "topics_learned": "Pytest and TestClient",
            "blockers": "None",
            "next_day_plan": "Complete documentation",
            "completion_percentage": 80
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["candidate_id"] == candidate["id"]
    assert data["completion_percentage"] == 80

def test_duplicate_daily_status_rejected():
    candidate_response = client.post(
        "/api/candidates",
        json={
            "full_name": "Duplicate Test",
            "email": "duplicate@example.com",
            "training_track": "Python",
            "is_active": True
        }
    )

    candidate_id = candidate_response.json()["id"]

    status_data = {
        "candidate_id": candidate_id,
        "status_date": "2026-08-21",
        "work_completed": "Testing",
        "topics_learned": "Pytest",
        "blockers": "None",
        "next_day_plan": "Continue testing",
        "completion_percentage": 70
    }

    first_response = client.post(
        "/api/statuses",
        json=status_data
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/statuses",
        json=status_data
    )

    assert second_response.status_code in [400, 409]


def test_update_status():
    candidate_response = client.post(
        "/api/candidates",
        json={
            "full_name": "Update Test",
            "email": "update@example.com",
            "training_track": "Python",
            "is_active": True
        }
    )

    candidate_id = candidate_response.json()["id"]

    status_response = client.post(
        "/api/statuses",
        json={
            "candidate_id": candidate_id,
            "status_date": "2026-08-21",
            "work_completed": "Initial work",
            "topics_learned": "Initial topic",
            "blockers": "None",
            "next_day_plan": "Continue",
            "completion_percentage": 40
        }
    )

    status_id = status_response.json()["id"]

    response = client.put(
        f"/api/statuses/{status_id}",
        json={
            "candidate_id": candidate_id,
            "status_date": "2026-08-21",
            "work_completed": "Updated work",
            "topics_learned": "Updated topic",
            "blockers": "None",
            "next_day_plan": "Continue project",
            "completion_percentage": 60
        }
    )


    assert response.status_code == 200

    data = response.json()

    assert data["completion_percentage"] == 60
    assert data["work_completed"] == "Updated work"


def test_missing_status():
    response = client.get("/api/statuses/999999")

    assert response.status_code == 404