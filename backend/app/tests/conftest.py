import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base, get_db
from app.main import app
from app.settings import Settings

# Загружаем настройки специально для тестов
test_settings = Settings(_env_file=".env.test")

# Создаем отдельный engine для тестов
test_engine = create_engine(test_settings.database_url)

# Создаем отдельный SessionLocal для тестов
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def override_get_db():
    def _override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    return _override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database(override_get_db):
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
