import pytest

from app.modules.fields.schemas import FieldCreate, FieldType


@pytest.fixture
def sample_field_complete():
    """Complete field with all properties"""
    return FieldCreate(
        name="transaction_amount",
        description="Monetary amount of transaction in cents",
        field_type=FieldType.number,
        example=1299,
    )


@pytest.fixture
def sample_boolean_field():
    """Boolean field for testing"""
    return FieldCreate(
        name="is_premium_user",
        description="Whether user has premium subscription",
        field_type=FieldType.boolean,
        example=True,
    )


# Test different field types
def test_create_string_field(auth_client):
    """Test creating string field"""
    field_data = FieldCreate(
        name="user_email",
        description="User email address",
        field_type=FieldType.string,
        example="user@example.com",
    )

    response = auth_client.post("/v1/fields/", json=field_data.model_dump())
    assert response.status_code == 201

    data = response.json()
    assert data["field_type"] == "string"
    assert data["example"] == "user@example.com"


def test_create_number_field(auth_client, sample_field_complete):
    """Test creating number field"""
    response = auth_client.post("/v1/fields/", json=sample_field_complete.model_dump())
    assert response.status_code == 201

    data = response.json()
    assert data["field_type"] == "number"
    assert data["example"] == 1299


def test_create_boolean_field(auth_client, sample_boolean_field):
    """Test creating boolean field"""
    response = auth_client.post("/v1/fields/", json=sample_boolean_field.model_dump())
    assert response.status_code == 201

    data = response.json()
    assert data["field_type"] == "boolean"
    assert data["example"] is True


def test_create_array_field(auth_client):
    """Test creating array field"""
    field_data = FieldCreate(
        name="user_interests",
        description="List of user interests",
        field_type=FieldType.array,
        example=["sports", "technology", "music"],
    )

    response = auth_client.post("/v1/fields/", json=field_data.model_dump())
    assert response.status_code == 201

    data = response.json()
    assert data["field_type"] == "array"
    assert isinstance(data["example"], list)


def test_create_object_field(auth_client):
    """Test creating object field"""
    field_data = FieldCreate(
        name="user_profile",
        description="User profile object",
        field_type=FieldType.object,
        example={"name": "John", "age": 30},
    )

    response = auth_client.post("/v1/fields/", json=field_data.model_dump())
    assert response.status_code == 201

    data = response.json()
    assert data["field_type"] == "object"
    assert isinstance(data["example"], dict)


def test_create_integer_field(auth_client):
    """Test creating integer field"""
    field_data = FieldCreate(
        name="user_age",
        description="User age in years",
        field_type=FieldType.integer,
        example=25,
    )

    response = auth_client.post("/v1/fields/", json=field_data.model_dump())
    assert response.status_code == 201

    data = response.json()
    assert data["field_type"] == "integer"
    assert data["example"] == 25


# Test field operations
def test_list_fields_returns_all(auth_client):
    """Test that listing fields returns all created fields"""
    # Create some test fields first
    field1 = FieldCreate(name="test_field_1", field_type=FieldType.string)
    field2 = FieldCreate(name="test_field_2", field_type=FieldType.number)

    auth_client.post("/v1/fields/", json=field1.model_dump())
    auth_client.post("/v1/fields/", json=field2.model_dump())

    # Now test listing
    response = auth_client.get("/v1/fields/")
    assert response.status_code == 200

    fields = response.json()
    assert isinstance(fields, list)
    assert len(fields) >= 2  # Should have at least our created fields


def test_get_field_with_event_count(auth_client):
    """Test getting field with event count"""
    # Create a test field first
    field_data = FieldCreate(name="test_field_with_count", field_type=FieldType.string)
    create_response = auth_client.post("/v1/fields/", json=field_data.model_dump())
    assert create_response.status_code == 201

    field_id = create_response.json()["id"]

    response = auth_client.get(
        f"/v1/fields/{field_id}", params={"with_event_count": True}
    )
    assert response.status_code == 200

    data = response.json()
    assert "event_count" in data
    assert isinstance(data["event_count"], int)


def test_update_field(auth_client):
    """Test updating field"""
    # Create field first
    create_data = FieldCreate(
        name="update_test_field",
        description="Field to be updated",
        field_type=FieldType.string,
        example="original",
    )

    create_response = auth_client.post("/v1/fields/", json=create_data.model_dump())
    field_id = create_response.json()["id"]

    # Update field
    update_data = FieldCreate(
        name="update_test_field",  # Name should stay same due to unique constraint
        description="Updated description",
        field_type=FieldType.string,
        example="updated",
    )

    update_response = auth_client.put(
        f"/v1/fields/{field_id}", json=update_data.model_dump()
    )
    assert update_response.status_code == 200

    data = update_response.json()
    assert data["description"] == "Updated description"
    assert data["example"] == "updated"


def test_delete_field(auth_client):
    """Test deleting field"""
    # Create field to delete
    field_data = FieldCreate(
        name="delete_test_field",
        description="Field to be deleted",
        field_type=FieldType.string,
    )

    create_response = auth_client.post("/v1/fields/", json=field_data.model_dump())
    field_id = create_response.json()["id"]

    # Delete field
    delete_response = auth_client.delete(f"/v1/fields/{field_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["name"] == "delete_test_field"

    # Verify field is gone
    get_response = auth_client.get(f"/v1/fields/{field_id}")
    assert get_response.status_code == 404


# Test error cases
def test_get_nonexistent_field(auth_client):
    """Test getting field that doesn't exist"""
    response = auth_client.get("/v1/fields/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_nonexistent_field(auth_client):
    """Test updating field that doesn't exist"""
    field_data = FieldCreate(
        name="nonexistent", description="This won't work", field_type=FieldType.string
    )

    response = auth_client.put("/v1/fields/99999", json=field_data.model_dump())
    assert response.status_code == 404


def test_delete_nonexistent_field(auth_client):
    """Test deleting field that doesn't exist"""
    response = auth_client.delete("/v1/fields/99999")
    assert response.status_code == 404


def test_create_duplicate_field_name(auth_client):
    """Test creating field with duplicate name (should fail due to unique constraint)"""
    field_data = FieldCreate(
        name="duplicate_name_test",
        description="First field",
        field_type=FieldType.string,
    )

    # Create first field
    response1 = auth_client.post("/v1/fields/", json=field_data.model_dump())
    assert response1.status_code == 201

    # Try to create second field with same name
    field_data2 = FieldCreate(
        name="duplicate_name_test",  # Same name
        description="Second field",
        field_type=FieldType.number,
    )

    response2 = auth_client.post("/v1/fields/", json=field_data2.model_dump())
    assert response2.status_code == 400  # Should fail


# Test validation edge cases
def test_create_field_empty_name(auth_client):
    """Test creating field with empty name"""
    response = auth_client.post(
        "/v1/fields/",
        json={"name": "", "description": "Invalid field", "field_type": "string"},
    )
    assert response.status_code == 422


def test_create_field_invalid_type(auth_client):
    """Test creating field with invalid type"""
    response = auth_client.post(
        "/v1/fields/",
        json={
            "name": "invalid_type_field",
            "description": "Field with bad type",
            "field_type": "invalid_type",
        },
    )
    assert response.status_code == 422


def test_create_field_missing_required_fields(auth_client):
    """Test creating field without required fields"""
    response = auth_client.post(
        "/v1/fields/", json={"description": "Missing name and type"}
    )
    assert response.status_code == 422


def test_create_field_without_description(auth_client):
    """Test creating field without optional description"""
    field_data = FieldCreate(name="no_description_field", field_type=FieldType.string)

    response = auth_client.post("/v1/fields/", json=field_data.model_dump())
    assert response.status_code == 201

    data = response.json()
    assert data["description"] is None


def test_create_field_without_example(auth_client):
    """Test creating field without optional example"""
    field_data = FieldCreate(
        name="no_example_field",
        description="Field without example",
        field_type=FieldType.string,
    )

    response = auth_client.post("/v1/fields/", json=field_data.model_dump())
    assert response.status_code == 201

    data = response.json()
    assert data["example"] is None


# Test authentication
def test_list_fields_requires_auth(client):
    """Test that listing fields requires authentication"""
    response = client.get("/v1/fields/")
    assert response.status_code == 401


def test_create_field_requires_auth(client):
    """Test that creating fields requires authentication"""
    response = client.post(
        "/v1/fields/",
        json={
            "name": "unauthorized_field",
            "description": "Should fail",
            "field_type": "string",
        },
    )
    assert response.status_code == 401
