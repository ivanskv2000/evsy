import pytest

from app.modules.fields.schemas import FieldCreate


@pytest.fixture
def sample_field():
    """Тестовое событие"""
    return FieldCreate(
        name="from_page", description="Some field description.", field_type="string"
    )


def test_create_field(auth_client, sample_field):
    """Тест на создание события"""
    response = auth_client.post("/v1/fields/", json=sample_field.model_dump())
    assert response.status_code == 201
    assert response.json()["name"] == "from_page"


def test_get_field(auth_client, sample_field):
    """Тест на получение события"""
    response = auth_client.get("/v1/fields/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
