import pytest

from app.modules.tags.schemas import TagCreate


@pytest.fixture
def sample_tag():
    return TagCreate(
        id="release",
        description="Some tag description.",
    )


def test_create_tag(auth_client, sample_tag):
    response = auth_client.post("/v1/tags/", json=sample_tag.model_dump())
    assert response.status_code == 201
    assert response.json()["id"] == sample_tag.id


def test_get_tag(auth_client, sample_tag):
    auth_client.post("/v1/tags/", json=sample_tag.model_dump())
    response = auth_client.get(f"/v1/tags/{sample_tag.id}")
    assert response.status_code == 200
    assert response.json()["id"] == sample_tag.id
