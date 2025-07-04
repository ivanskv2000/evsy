import pytest

from app.modules.tags.schemas import TagCreate


@pytest.fixture
def sample_tag():
    """Тестовое событие"""
    return TagCreate(
        id="release",
        description="Some tag description.",
    )


def test_create_tag(auth_client, sample_tag):
    """Тест на создание события"""
    response = auth_client.post("/v1/tags/", json=sample_tag.model_dump())
    assert response.status_code == 201
    assert response.json()["id"] == sample_tag.id


def test_get_tag(auth_client, sample_tag):
    """Тест на получение события"""
    response = auth_client.get("/v1/tags/release")
    assert response.status_code == 200
    assert response.json()["id"] == sample_tag.id
