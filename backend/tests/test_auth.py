import pytest


@pytest.fixture
def auth_data():
    return {
        "email": "user@example.com",
        "password": "securepassword123",
    }


def test_signup_returns_token(client, auth_data):
    response = client.post("/v1/auth/signup", json=auth_data)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_signup_duplicate_email(client, auth_data):
    # Repeat signup to trigger duplicate error
    response = client.post("/v1/auth/signup", json=auth_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_login_with_valid_credentials(client, auth_data):
    response = client.post("/v1/auth/login", json=auth_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_invalid_password(client, auth_data):
    response = client.post(
        "/v1/auth/login",
        json={"email": auth_data["email"], "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "invalid credentials" in response.json()["detail"].lower()


def test_login_with_unknown_email(client):
    response = client.post(
        "/v1/auth/login",
        json={"email": "unknown@example.com", "password": "irrelevant"},
    )
    assert response.status_code == 401
    assert "invalid credentials" in response.json()["detail"].lower()


def test_me_requires_auth(client):
    response = client.get("/v1/auth/me")
    assert response.status_code == 401


def test_me_with_valid_token(auth_client, auth_data):
    response = auth_client.get("/v1/auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert "id" in response.json()


def test_login_for_access_token(client, auth_data):
    form_data = {
        "username": auth_data["email"],
        "password": auth_data["password"],
    }
    response = client.post("/v1/auth/token", data=form_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
