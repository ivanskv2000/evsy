from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    debug: bool = False
    secret_key: Optional[str] = None
    frontend_url: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
