from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    debug: bool = False
    secret_key: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
