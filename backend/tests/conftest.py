import bcrypt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from dotenv import load_dotenv
import os

from app.core.database import Base, get_db
from app.factory import create_app
from app.modules.auth.crud import create_user
from app.modules.auth.token import create_access_token
from app.settings import Settings

# No need for manual load_dotenv, Settings() will handle it via resolve_env_file()
# or we can pass it explicitly for maximum clarity in tests.

@pytest.fixture(scope="session")
def test_settings():
    """Session-scoped fixture for test settings, using a Postgres DB."""
    # We explicitly pass the env file to ensure we use exactly what we want
    return Settings(_env_file=".env.test")


@pytest.fixture(scope="session")
def db_engine(test_settings: Settings):
    """Session-scoped engine for the Postgres database."""
    engine = create_engine(test_settings.database_url)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def app(test_settings: Settings, db_engine):
    """Session-scoped fixture for the FastAPI application instance."""
    # We use a dummy session_local here because we'll override get_db at the request level
    dummy_session_local = sessionmaker(bind=db_engine)
    return create_app(test_settings, dummy_session_local)


@pytest.fixture
def db(db_engine):
    """
    Function-scoped fixture that provides a transactional database session.
    Everything is rolled back at the end of the test.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def override_get_db(app, db):
    """Fixture to override the get_db dependency for every test."""
    def _get_db():
        yield db

    app.dependency_overrides[get_db] = _get_db
    yield _get_db  # Yield the function so it can be called if needed
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(autouse=True)
def auto_override_get_db(override_get_db):
    """Automatically apply the get_db override for every test."""
    pass


@pytest.fixture
def test_user(db):
    """Create a test user in the DB for the current transaction."""
    user = create_user(
        db,
        email="test@example.com",
        hashed_pw=bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode("utf-8"),
    )
    return user


@pytest.fixture
def access_token(test_user):
    """Create an access token for the test user."""
    return create_access_token({"sub": str(test_user.email)})


@pytest.fixture
def client(app):
    """Test client for unauthenticated requests."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_client(app, access_token):
    """Test client for authenticated requests."""
    with TestClient(app) as auth_client:
        auth_client.headers.update({"Authorization": f"Bearer {access_token}"})
        yield auth_client
