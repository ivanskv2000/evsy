import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """Создаем таблицы перед запуском тестов"""
    Base.metadata.create_all(bind=engine)
    yield
    # Если нужно очистить БД после тестов — можно добавить drop
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    """Создаем и возвращаем клиент для тестов"""
    client = TestClient(app)
    return client
