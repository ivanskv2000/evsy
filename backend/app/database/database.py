from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import Settings

settings = Settings()

DATABASE_URL = settings.database_url

# Создаем движок для работы с базой данных
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

# Сессия для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
