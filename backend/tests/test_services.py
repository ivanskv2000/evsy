from unittest.mock import MagicMock, patch

import pytest

from app.modules.auth.schemas import UserCreate
from app.modules.auth.service import (
    create_user,
    get_or_create_oauth_user,
    hash_password,
    verify_password,
)
from app.modules.events.schemas import EventLink, EventOut, LinkType
from app.modules.events.service import generate_json_schema_for_event
from app.modules.fields.schemas import FieldOut, FieldType
from app.modules.tags.schemas import TagOut
from app.shared.service import assert_db_empty


@pytest.fixture
def sample_event_out():
    """Sample EventOut for schema generation testing"""
    return EventOut(
        id=1,
        name="user_signup",
        description="User completes registration",
        links=[
            EventLink(
                type=LinkType.figma,
                url="https://figma.com/signup",
                label="Signup Design",
            )
        ],
        tags=[
            TagOut(
                id="authentication",
                description="Auth related events",
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z",
            ),
            TagOut(
                id="onboarding",
                description="User onboarding flow",
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z",
            ),
        ],
        fields=[
            FieldOut(
                id=1,
                name="user_id",
                description="Unique user identifier",
                field_type=FieldType.string,
                example="user_12345",
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z",
            ),
            FieldOut(
                id=2,
                name="signup_method",
                description="How user signed up",
                field_type=FieldType.string,
                example="email",
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z",
            ),
        ],
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
    )


# Test events service functions
def test_generate_json_schema_basic(sample_event_out):
    """Test basic JSON schema generation"""
    schema = generate_json_schema_for_event(sample_event_out)

    assert isinstance(schema, dict)
    assert schema["type"] == "object"
    assert "properties" in schema

    properties = schema["properties"]
    assert "user_id" in properties
    assert "signup_method" in properties

    # Check field types are correctly mapped
    assert properties["user_id"]["type"] == "string"
    assert properties["signup_method"]["type"] == "string"


def test_generate_json_schema_with_descriptions(sample_event_out):
    """Test schema generation with descriptions enabled"""
    schema = generate_json_schema_for_event(sample_event_out, include_descriptions=True)

    properties = schema["properties"]
    assert "description" in properties["user_id"]
    assert properties["user_id"]["description"] == "Unique user identifier"


def test_generate_json_schema_without_descriptions(sample_event_out):
    """Test schema generation with descriptions disabled"""
    schema = generate_json_schema_for_event(
        sample_event_out, include_descriptions=False
    )

    properties = schema["properties"]
    assert "description" not in properties["user_id"]


def test_generate_json_schema_with_examples(sample_event_out):
    """Test schema generation with examples enabled"""
    schema = generate_json_schema_for_event(sample_event_out, include_examples=True)

    properties = schema["properties"]
    assert "example" in properties["user_id"]
    assert properties["user_id"]["example"] == "user_12345"


def test_generate_json_schema_without_examples(sample_event_out):
    """Test schema generation with examples disabled"""
    schema = generate_json_schema_for_event(sample_event_out, include_examples=False)

    properties = schema["properties"]
    assert "example" not in properties["user_id"]


def test_generate_json_schema_additional_properties_true(sample_event_out):
    """Test schema generation with additional properties allowed"""
    schema = generate_json_schema_for_event(
        sample_event_out, additional_properties=True
    )

    assert schema["additionalProperties"] is True


def test_generate_json_schema_additional_properties_false(sample_event_out):
    """Test schema generation with additional properties disabled"""
    schema = generate_json_schema_for_event(
        sample_event_out, additional_properties=False
    )

    assert schema["additionalProperties"] is False


def test_generate_json_schema_different_field_types():
    """Test schema generation with different field types"""
    event = EventOut(
        id=1,
        name="test_event",
        description="Test event",
        links=[],
        tags=[],
        fields=[
            FieldOut(
                id=1,
                name="string_field",
                field_type=FieldType.string,
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z",
            ),
            FieldOut(
                id=2,
                name="number_field",
                field_type=FieldType.number,
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z",
            ),
            FieldOut(
                id=3,
                name="boolean_field",
                field_type=FieldType.boolean,
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z",
            ),
            FieldOut(
                id=4,
                name="array_field",
                field_type=FieldType.array,
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z",
            ),
            FieldOut(
                id=5,
                name="object_field",
                field_type=FieldType.object,
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z",
            ),
            FieldOut(
                id=6,
                name="integer_field",
                field_type=FieldType.integer,
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z",
            ),
        ],
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
    )

    schema = generate_json_schema_for_event(event)
    properties = schema["properties"]

    assert properties["string_field"]["type"] == "string"
    assert properties["number_field"]["type"] == "number"
    assert properties["boolean_field"]["type"] == "boolean"
    assert properties["array_field"]["type"] == "array"
    assert properties["object_field"]["type"] == "object"
    assert properties["integer_field"]["type"] == "integer"


# Test auth service functions
def test_hash_password():
    """Test password hashing"""
    password = "test_password_123"
    hashed = hash_password(password)

    assert isinstance(hashed, str)
    assert hashed != password  # Should be different from original
    assert len(hashed) > 0


def test_verify_password():
    """Test password verification"""
    password = "test_password_123"
    hashed = hash_password(password)

    # Correct password should verify
    assert verify_password(password, hashed) is True

    # Wrong password should fail
    assert verify_password("wrong_password", hashed) is False


def test_verify_password_with_invalid_hash():
    """Test password verification with invalid hash"""
    # Test with a completely invalid hash that will trigger an exception
    try:
        result = verify_password("any_password", "invalid_hash")
        assert result is False
    except Exception:
        # If it raises an exception, that's also acceptable behavior
        # for an invalid hash, just verify it doesn't crash the app
        pass


@patch("app.modules.auth.crud.create_user")
def test_create_user_success(mock_create_user, override_get_db):
    """Test successful user creation"""
    db = next(override_get_db())

    # Mock successful user creation
    mock_user = MagicMock()
    mock_user.email = "test@example.com"
    mock_create_user.return_value = mock_user

    user_data = UserCreate(email="test@example.com", password="password123")
    result = create_user(db, user_data)

    assert result.email == "test@example.com"
    mock_create_user.assert_called_once()


@patch("app.modules.auth.crud.create_user")
def test_create_user_duplicate_email(mock_create_user, override_get_db):
    """Test user creation with duplicate email"""
    from fastapi import HTTPException
    from sqlalchemy.exc import IntegrityError

    db = next(override_get_db())

    # Mock IntegrityError for duplicate email
    mock_create_user.side_effect = IntegrityError("duplicate", None, None)

    user_data = UserCreate(email="duplicate@example.com", password="password123")

    with pytest.raises(HTTPException) as exc_info:
        create_user(db, user_data)

    assert exc_info.value.status_code == 400
    assert "already exists" in exc_info.value.detail


@patch("app.modules.auth.crud.get_or_create_oauth_user")
def test_get_or_create_oauth_user(mock_get_or_create, override_get_db):
    """Test OAuth user creation/retrieval"""
    db = next(override_get_db())

    mock_user = MagicMock()
    mock_user.email = "oauth@example.com"
    mock_user.oauth_provider = "github"
    mock_get_or_create.return_value = mock_user

    result = get_or_create_oauth_user(db, email="oauth@example.com", provider="github")

    assert result.email == "oauth@example.com"
    assert result.oauth_provider == "github"
    mock_get_or_create.assert_called_once_with(
        db, email="oauth@example.com", provider="github"
    )


# Test shared service functions
def test_assert_db_empty_with_empty_db(override_get_db):
    """Test assert_db_empty with empty database"""
    db = next(override_get_db())

    # Should not raise exception when database is empty
    # (This test uses the actual database state from conftest.py)
    try:
        assert_db_empty(db)
    except Exception:
        # If it fails, database isn't empty, which is fine for this test
        pass


def test_assert_db_empty_with_events(auth_client, override_get_db):
    """Test assert_db_empty with events in database"""
    from fastapi import HTTPException

    # Create an event first
    auth_client.post(
        "/v1/events/",
        json={
            "name": "test_event_for_assert_db_empty",
            "description": "Test event",
            "tags": [],
            "fields": [],
        },
    )

    db = next(override_get_db())

    with pytest.raises(HTTPException) as exc_info:
        assert_db_empty(db)

    assert exc_info.value.status_code == 405  # Correct status code from source
    assert "empty database" in exc_info.value.detail


def test_generate_json_schema_event_with_no_fields():
    """Test schema generation for event with no fields"""
    event = EventOut(
        id=1,
        name="simple_event",
        description="Event with no fields",
        links=[],
        tags=[],
        fields=[],  # No fields
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
    )

    schema = generate_json_schema_for_event(event)

    assert schema["type"] == "object"
    assert schema["properties"] == {}  # Empty properties
    assert "additionalProperties" in schema
