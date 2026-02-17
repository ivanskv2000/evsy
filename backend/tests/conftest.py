import bcrypt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.database import Base, get_db, init_db
from app.factory import create_app
from app.modules.auth.crud import create_user
from app.modules.auth.token import create_access_token
from app.settings import Settings


@pytest.fixture(scope="session")
def test_settings():
    """Session-scoped fixture for test settings, using a file-based SQLite DB."""
    settings = Settings(_env_file=".env.test")
    settings.database_url = "sqlite:///./test.db"
    return settings


@pytest.fixture(scope="session")
def db_engine_session(test_settings: Settings):
    """Session-scoped fixture for the database engine and session factory."""
    engine, session_local = init_db(test_settings)
    return engine, session_local


@pytest.fixture(scope="session")
def app(test_settings: Settings, db_engine_session):
    """Session-scoped fixture for the FastAPI application instance."""
    _, session_local = db_engine_session
    return create_app(test_settings, session_local)


@pytest.fixture(scope="session")
def override_get_db(db_engine_session):
    """Session-scoped fixture to override the `get_db` dependency."""
    _, session_local = db_engine_session

    def _override_get_db():
        db: Session = session_local()
        try:
            yield db
        finally:
            db.close()

    return _override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database(app, db_engine_session, override_get_db):
    """
    Session-scoped, autouse fixture to set up the database schema and dependency overrides.
    """
    engine, _ = db_engine_session
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def test_user(override_get_db):
    """Create a test user in the DB"""
    db = next(override_get_db())
    user = create_user(
        db,
        email="test@example.com",
        hashed_pw=bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode("utf-8"),
    )

    return user


@pytest.fixture(scope="session")
def access_token(test_user):
    """Create an access token for the test user."""
    return create_access_token({"sub": str(test_user.email)})


@pytest.fixture(scope="module")
def client(app):
    """Module-scoped test client for unauthenticated requests."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_client(app, access_token):
    """Function-scoped test client for authenticated requests."""
    with TestClient(app) as auth_client:
        auth_client.headers.update({"Authorization": f"Bearer {access_token}"})
        yield auth_client
