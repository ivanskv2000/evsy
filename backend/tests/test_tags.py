import pytest

from app.schemas import TagCreate


@pytest.fixture
def sample_tag():
    """Тестовое событие"""
    return TagCreate(
        id="release",
        description="Some tag description.",
    )


def test_create_tag(client, sample_tag):
    """Тест на создание события"""
    response = client.post("/v1/tags/", json=sample_tag.model_dump())
    assert response.status_code == 201
    assert response.json()["id"] == sample_tag.id


def test_get_tag(client, sample_tag):
    """Тест на получение события"""
    response = client.get("/v1/tags/release")
    assert response.status_code == 200
    assert response.json()["id"] == sample_tag.id
