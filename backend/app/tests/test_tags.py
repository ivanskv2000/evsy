import pytest
from app.schemas import TagCreate
from fastapi.testclient import TestClient

@pytest.fixture
def sample_tag():
    """Тестовое событие"""
    return TagCreate(
        id="experiment",
        description="Some tag description.",
    )

def test_create_event(client, sample_tag):
    """Тест на создание события"""
    response = client.post("/api/v1/tags/", json=sample_tag.model_dump())
    assert response.status_code == 201
    assert response.json()["id"] == sample_tag.id

def test_get_event(client, sample_tag):
    """Тест на получение события"""
    response = client.get("/api/v1/tags/experiment")
    assert response.status_code == 200
    assert response.json()["id"] == sample_tag.id
