from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_missing_candidates():
    candidates = []

    for i in range(3):
        response = client.post(
            "/api/candidates",
            json={
                "full_name": f"Dashboard Test {i}",
                "email": f"dashboard{i}@example.com",
                "training_track": "Python",
                "is_active": True
            }
        )

        candidates.append(response.json()["id"])

    status_response = client.post(
        "/api/statuses",
        json={
            "candidate_id": candidates[0],
            "status_date": "2026-08-21",
            "work_completed": "Testing",
            "topics_learned": "Testing",
            "blockers": "None",
            "next_day_plan": "Continue",
            "completion_percentage": 50
        }
    )

    print("STATUS:", status_response.status_code)
    print("BODY:", status_response.json())  

    response = client.get(
        "/api/dashboard/summary?date=2026-08-21"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["submitted_count"] == 1
    assert data["missing_count"] == 2