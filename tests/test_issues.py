from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_create_issue() -> None:
    payload = {
        "title": "Login failure",
        "description": "Users receive an error after submitting credentials.",
        "priority": "high",
    }

    response = client.post(
        "/issues",
        json=payload,
        headers={"Idempotency-Key": "test-create-issue-001"},
    )

    assert response.status_code == 201

    body = response.json()
    assert body["title"] == payload["title"]
    assert body["description"] == payload["description"]
    assert body["priority"] == payload["priority"]
    assert body["status"] == "open"
    assert body["id"]
    assert body["created_at"]
