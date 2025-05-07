from app.settings import Settings
from app.factory import create_app
from app.database.database import init_db

settings = Settings()
engine, SessionLocal = init_db(settings)
app = create_app(settings)
