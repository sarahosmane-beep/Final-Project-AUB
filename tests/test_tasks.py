import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage.task_store import task_store


client = TestClient(app)


@pytest.fixture(autouse=True)
def empty_store() -> None:
    task_store.clear()


def create_task(**overrides: str) -> dict:
    payload = {
        "title": "Write documentation",
        "description": "Cover the public API",
        "status": "ToDo",
        "priority": "High",
        "assignee": "Sam",
        **overrides,
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_and_get_task() -> None:
    created = create_task()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Write documentation"
    assert response.json()["created_at"]


def test_list_tasks_can_filter_status_and_priority() -> None:
    create_task()
    create_task(title="Ship release", status="Done", priority="Low")
    assert len(client.get("/tasks").json()) == 2
    filtered = client.get("/tasks", params={"status": "Done", "priority": "Low"})
    assert [task["title"] for task in filtered.json()] == ["Ship release"]


def test_update_task_including_status_transition() -> None:
    created = create_task()
    response = client.patch(
        f"/tasks/{created['id']}",
        json={"status": "InProgress", "assignee": "Jo"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"
    assert response.json()["assignee"] == "Jo"


def test_delete_task() -> None:
    created = create_task()
    assert client.delete(f"/tasks/{created['id']}").status_code == 204
    assert client.get(f"/tasks/{created['id']}").status_code == 404


def test_validation_and_missing_tasks() -> None:
    assert client.post("/tasks", json={"title": ""}).status_code == 422
    assert client.patch("/tasks/999", json={"status": "Done"}).status_code == 404
    assert client.delete("/tasks/999").status_code == 404
