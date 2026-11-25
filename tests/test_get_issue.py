from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_get_existing_issue() -> None:
    create_payload = {
        "title": "Login failure",
        "description": "Users receive an error after submitting credentials.",
        "priority": "high",
    }

    create_response = client.post("/issues", json=create_payload)
    created_issue = create_response.json()

    get_response = client.get(f"/issues/{created_issue['id']}")

    assert get_response.status_code == 200
    assert get_response.json() == created_issue


def test_get_missing_issue_returns_not_found() -> None:
    response = client.get("/issues/not-a-real-id")

    assert response.status_code == 404
    assert response.json() == {"detail": "Issue not found"}
