import pytest

from app.modules.events.schemas import EventCreate


@pytest.fixture
def sample_event():
    """Тестовое событие"""
    return EventCreate(
        name="Test Event",
        description="Some event description.",
        tags=["feature", "experiment"],
        fields=[],
    )


def test_create_event(auth_client, sample_event):
    response = auth_client.post("/v1/events/", json=sample_event.model_dump())
    assert response.status_code == 201
    assert response.json()["name"] == sample_event.name


def test_get_event(auth_client):
    response = auth_client.get("/v1/events/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_create_event_with_invalid_field(auth_client):
    response = auth_client.post(
        "/v1/events/",
        json={
            "name": "Event with a bad field",
            "description": "Some event description.",
            "tags": [],
            "fields": [999],
        },
    )
    assert response.status_code == 400
    assert "fields" in response.json()["detail"].lower()


def test_create_event_with_new_tag(auth_client):
    response = auth_client.post(
        "/v1/events/",
        json={
            "name": "Event with a new tag",
            "description": "Some event description.",
            "tags": ["new-tag"],
            "fields": [],
        },
    )
    assert response.status_code == 201

    tag_response = auth_client.get("/v1/tags/new-tag")
    assert tag_response.status_code == 200
    assert tag_response.json()["id"] == "new-tag"


def test_update_event_with_new_tag(auth_client):
    create_response = auth_client.post(
        "/v1/events/",
        json={
            "name": "Event without optional fields",
            "description": "Some event description.",
            "tags": [],
            "fields": [],
        },
    )
    event_id = create_response.json()["id"]

    update_response = auth_client.put(
        f"/v1/events/{event_id}",
        json={
            "name": "Updated Event, now with a tag!",
            "description": "Some event description.",
            "tags": ["updated-tag"],
            "fields": [],
        },
    )
    assert update_response.status_code == 200

    tag_response = auth_client.get("/v1/tags/updated-tag")
    assert tag_response.status_code == 200
    assert tag_response.json()["id"] == "updated-tag"
