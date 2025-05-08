import sys

from pydantic import ValidationError

from app.database.database import init_db
from app.factory import create_app
from app.settings import Settings

try:
    settings = Settings()
except ValidationError as e:
    print("❌ Invalid ENV value in configuration:", e)
    sys.exit(1)

engine, SessionLocal = init_db(settings)
app = create_app(settings)
