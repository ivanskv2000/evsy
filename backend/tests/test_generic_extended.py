def test_ping_endpoint(auth_client):
    """Test ping health check endpoint"""
    response = auth_client.get("/v1/ping")
    assert response.status_code == 200

    data = response.json()
    assert "pong" in data
    assert data["pong"] is True
    assert "debug_mode" in data
    assert isinstance(data["debug_mode"], bool)


def test_config_endpoint(auth_client):
    """Test config endpoint"""
    response = auth_client.get("/v1/config")
    assert response.status_code == 200

    data = response.json()
    assert "database_url" in data
    assert "debug" in data
    assert isinstance(data["debug"], bool)


def test_link_types_endpoint(auth_client):
    """Test link types endpoint"""
    response = auth_client.get("/v1/link-types")
    assert response.status_code == 200

    link_types = response.json()
    assert isinstance(link_types, list)
    assert len(link_types) > 0

    # Check that common link types are present
    expected_types = [
        "figma",
        "miro",
        "confluence",
        "jira",
        "notion",
        "loom",
        "slack",
        "google",
        "other",
    ]
    for expected_type in expected_types:
        assert expected_type in link_types

    # Check caching header is set
    assert response.headers.get("cache-control") == "public, max-age=3600"


def test_field_types_endpoint(auth_client):
    """Test field types endpoint"""
    response = auth_client.get("/v1/field-types")
    assert response.status_code == 200

    field_types = response.json()
    assert isinstance(field_types, list)
    assert len(field_types) > 0

    # Check that all expected field types are present
    expected_types = ["string", "number", "integer", "boolean", "array", "object"]
    for expected_type in expected_types:
        assert expected_type in field_types

    # Check caching header is set
    assert response.headers.get("cache-control") == "public, max-age=3600"


def test_ping_without_auth(client):
    """Test ping endpoint works without authentication"""
    response = client.get("/v1/ping")
    assert response.status_code == 200

    data = response.json()
    assert data["pong"] is True


def test_config_without_auth(client):
    """Test config endpoint works without authentication"""
    response = client.get("/v1/config")
    assert response.status_code == 200


def test_link_types_without_auth(client):
    """Test link types endpoint works without authentication"""
    response = client.get("/v1/link-types")
    assert response.status_code == 200

    link_types = response.json()
    assert isinstance(link_types, list)
    assert "figma" in link_types


def test_field_types_without_auth(client):
    """Test field types endpoint works without authentication"""
    response = client.get("/v1/field-types")
    assert response.status_code == 200

    field_types = response.json()
    assert isinstance(field_types, list)
    assert "string" in field_types
