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


def test_repeated_idempotency_key_returns_original_issue() -> None:
    payload = {
        "title": "Login failure",
        "description": "Users receive an error after submitting credentials.",
        "priority": "high",
    }
    headers = {"Idempotency-Key": "test-retry-safe-request-001"}

    first_response = client.post(
        "/issues",
        json=payload,
        headers=headers,
    )
    second_response = client.post(
        "/issues",
        json=payload,
        headers=headers,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    first_issue = first_response.json()
    second_issue = second_response.json()

    assert second_issue == first_issue
