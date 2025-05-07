from app.database.database import init_db
from app.factory import create_app
from app.settings import Settings

settings = Settings()
engine, SessionLocal = init_db(settings)
app = create_app(settings)
