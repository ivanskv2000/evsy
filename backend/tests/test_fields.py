import pytest

from app.modules.fields.schemas import FieldCreate


@pytest.fixture
def sample_field():
    return FieldCreate(
        name="from_page", description="Some field description.", field_type="string"
    )


def test_create_field(auth_client, sample_field):
    response = auth_client.post("/v1/fields/", json=sample_field.model_dump())
    assert response.status_code == 201
    assert response.json()["name"] == "from_page"


def test_get_field(auth_client, sample_field):
    create_response = auth_client.post("/v1/fields/", json=sample_field.model_dump())
    field_id = create_response.json()["id"]

    response = auth_client.get(f"/v1/fields/{field_id}")
    assert response.status_code == 200
    assert response.json()["id"] == field_id
