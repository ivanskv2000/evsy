import logging
import sys

from pydantic import ValidationError

from app.core.database import init_db
from app.factory import create_app
from app.settings import get_settings

settings = get_settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

try:
    engine, SessionLocal = init_db(settings)
except ValidationError as e:
    print("❌ Invalid ENV value in configuration:", e)
    sys.exit(1)

app = create_app(settings, engine, SessionLocal)
