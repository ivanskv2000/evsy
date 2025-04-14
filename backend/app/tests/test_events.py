import pytest
from app.schemas import EventCreate
from fastapi.testclient import TestClient

@pytest.fixture
def sample_event():
    """Тестовое событие"""
    return EventCreate(
        name="Test Event",
        description="Test Description",
        tags=["feature"]
    )

def test_create_event(client, sample_event):
    """Тест на создание события"""
    response = client.post("/api/v1/events/", json=sample_event.model_dump())
    assert response.status_code == 201
    assert response.json()["name"] == sample_event.name

def test_get_event(client):
    """Тест на получение события"""
    response = client.get("/api/v1/events/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
