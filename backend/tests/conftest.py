import bcrypt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.database import Base, get_db, init_db
from app.factory import create_app
from app.modules.auth.crud import create_user
from app.modules.auth.token import create_access_token
from app.settings import Settings

# Load test settings from .env.test
test_settings = Settings(_env_file=".env.test")

# Initialize DB objects for test (engine + SessionLocal)
test_engine, TestingSessionLocal = init_db(test_settings)

# Create the test app
app = create_app(test_settings, TestingSessionLocal)


# Override FastAPI's get_db dependency
@pytest.fixture(scope="session")
def override_get_db():
    def _override_get_db():
        db: Session = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    return _override_get_db


# Set up and tear down the database
@pytest.fixture(scope="session", autouse=True)
def setup_database(override_get_db):
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=test_engine)


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
    return create_access_token({"sub": str(test_user.email)})


# FastAPI test client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_client(client, access_token):
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client
