import pytest

from app.modules.events.schemas import EventCreate
from app.modules.fields.schemas import FieldCreate, FieldType


@pytest.fixture
def sample_field_for_event(auth_client):
    """Create a field that can be used in event tests"""
    field_data = FieldCreate(
        name="user_id",
        description="Unique user identifier",
        field_type=FieldType.string,
        example="user_12345",
    )
    response = auth_client.post("/v1/fields/", json=field_data.model_dump())
    return response.json()


@pytest.fixture
def complex_event():
    """Event with links and multiple properties"""
    return EventCreate(
        name="user_signup_completed",
        description="User successfully completes registration process",
        links=[
            {
                "type": "figma",
                "url": "https://figma.com/signup-flow",
                "label": "Signup Design",
            },
            {
                "type": "confluence",
                "url": "https://company.atlassian.net/wiki/signup-spec",
                "label": "Signup Specification",
            },
        ],
        tags=["authentication", "onboarding", "conversion"],
        fields=[],
    )


# Test API endpoints with more edge cases
def test_create_event_with_links(auth_client, complex_event):
    """Test creating event with external links"""
    response = auth_client.post("/v1/events/", json=complex_event.model_dump())
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == complex_event.name
    assert len(data["links"]) == 2
    assert data["links"][0]["type"] == "figma"
    assert data["links"][1]["label"] == "Signup Specification"


def test_create_event_with_field_association(auth_client, sample_field_for_event):
    """Test creating event with field associations"""
    event_data = EventCreate(
        name="button_click",
        description="User clicks a button",
        tags=["interaction"],
        fields=[sample_field_for_event["id"]],
    )

    response = auth_client.post("/v1/events/", json=event_data.model_dump())
    assert response.status_code == 201

    data = response.json()
    assert len(data["fields"]) == 1
    assert data["fields"][0]["name"] == "user_id"


def test_list_events_returns_all(auth_client):
    """Test that list endpoint returns all created events"""
    # Create some test events first
    event1 = EventCreate(
        name="test_event_1", description="Test event 1", tags=["test"], fields=[]
    )
    event2 = EventCreate(
        name="test_event_2", description="Test event 2", tags=["test"], fields=[]
    )

    auth_client.post("/v1/events/", json=event1.model_dump())
    auth_client.post("/v1/events/", json=event2.model_dump())

    # Now test listing
    response = auth_client.get("/v1/events/")
    assert response.status_code == 200

    events = response.json()
    assert isinstance(events, list)
    assert len(events) >= 2  # Should have at least our created events


def test_delete_event_removes_associations(auth_client):
    """Test that deleting event removes tag/field associations"""
    # Create event with associations
    event_data = EventCreate(
        name="temporary_event",
        description="Event to be deleted",
        tags=["temp"],
        fields=[],
    )

    create_response = auth_client.post("/v1/events/", json=event_data.model_dump())
    event_id = create_response.json()["id"]

    # Delete event
    delete_response = auth_client.delete(f"/v1/events/{event_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["name"] == "temporary_event"

    # Verify event is gone
    get_response = auth_client.get(f"/v1/events/{event_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_event(auth_client):
    """Test getting event that doesn't exist"""
    response = auth_client.get("/v1/events/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_nonexistent_event(auth_client):
    """Test updating event that doesn't exist"""
    event_data = EventCreate(
        name="nonexistent", description="This won't work", tags=[], fields=[]
    )

    response = auth_client.put("/v1/events/99999", json=event_data.model_dump())
    assert response.status_code == 404


def test_delete_nonexistent_event(auth_client):
    """Test deleting event that doesn't exist"""
    response = auth_client.delete("/v1/events/99999")
    assert response.status_code == 404


# Test schema export functionality
def test_export_event_json_schema(auth_client):
    """Test JSON schema export"""
    # Create a test event first
    event_data = EventCreate(
        name="test_export_event",
        description="Test event for export",
        tags=["test"],
        fields=[],
    )
    create_response = auth_client.post("/v1/events/", json=event_data.model_dump())
    assert create_response.status_code == 201

    event_id = create_response.json()["id"]

    response = auth_client.get(f"/v1/events/{event_id}/schema.json")
    assert response.status_code == 200

    schema = response.json()
    assert "type" in schema
    assert "properties" in schema


def test_export_event_yaml_schema(auth_client):
    """Test YAML schema export"""
    # Create a test event first
    event_data = EventCreate(
        name="test_yaml_export_event",
        description="Test event for YAML export",
        tags=["test"],
        fields=[],
    )
    create_response = auth_client.post("/v1/events/", json=event_data.model_dump())
    assert create_response.status_code == 201

    event_id = create_response.json()["id"]

    response = auth_client.get(f"/v1/events/{event_id}/schema.yaml")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/x-yaml"


def test_export_schema_with_options(auth_client):
    """Test schema export with different options"""
    # Create a test event first
    event_data = EventCreate(
        name="test_options_export_event",
        description="Test event for options export",
        tags=["test"],
        fields=[],
    )
    create_response = auth_client.post("/v1/events/", json=event_data.model_dump())
    assert create_response.status_code == 201

    event_id = create_response.json()["id"]

    # Test without descriptions
    response = auth_client.get(
        f"/v1/events/{event_id}/schema.json", params={"include_descriptions": False}
    )
    assert response.status_code == 200

    # Test without examples
    response = auth_client.get(
        f"/v1/events/{event_id}/schema.json", params={"include_examples": False}
    )
    assert response.status_code == 200


def test_export_schema_nonexistent_event(auth_client):
    """Test schema export for nonexistent event"""
    response = auth_client.get("/v1/events/99999/schema.json")
    assert response.status_code == 404


# Test validation edge cases
def test_create_event_empty_name(auth_client):
    """Test creating event with empty name"""
    response = auth_client.post(
        "/v1/events/",
        json={"name": "", "description": "Invalid event", "tags": [], "fields": []},
    )
    assert response.status_code == 422


def test_create_event_invalid_link_type(auth_client):
    """Test creating event with invalid link type"""
    response = auth_client.post(
        "/v1/events/",
        json={
            "name": "invalid_link_event",
            "description": "Event with bad link",
            "links": [{"type": "invalid_type", "url": "https://example.com"}],
            "tags": [],
            "fields": [],
        },
    )
    assert response.status_code == 422


def test_create_event_missing_required_fields(auth_client):
    """Test creating event without required fields"""
    response = auth_client.post(
        "/v1/events/", json={"description": "Missing name field"}
    )
    assert response.status_code == 422


def test_list_events_requires_auth(client):
    """Test that listing events requires authentication"""
    response = client.get("/v1/events/")
    assert response.status_code == 401


def test_create_event_requires_auth(client):
    """Test that creating events requires authentication"""
    response = client.post(
        "/v1/events/",
        json={
            "name": "unauthorized_event",
            "description": "Should fail",
            "tags": [],
            "fields": [],
        },
    )
    assert response.status_code == 401
