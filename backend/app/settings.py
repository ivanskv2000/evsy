import os
from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def resolve_env_file() -> Optional[str]:
    # 1. Check if ENV is set (e.g., ENV=test)
    env_mode = os.getenv("ENV")

    # Priority: current working directory (for tests)
    cwd = Path.cwd()
    if env_mode and (cwd / f".env.{env_mode}").exists():
        return str(cwd / f".env.{env_mode}")
    if (cwd / ".env").exists():
        return str(cwd / ".env")

    # Fallback: Absolute paths relative to this file
    backend_root = Path(__file__).parent.parent
    if env_mode:
        test_path = backend_root / f".env.{env_mode}"
        if test_path.exists():
            return str(test_path)

    local_env = backend_root / ".env"
    if local_env.exists():
        return str(local_env)

    root_env = backend_root.parent / ".env"
    if root_env.exists():
        return str(root_env)

    return None


class Settings(BaseSettings):
    def __init__(self, _env_file: Optional[str] = None, **kwargs):
        # Dynamically resolve env file if not provided
        if _env_file is None:
            _env_file = resolve_env_file()

        if _env_file:
            load_dotenv(_env_file, override=True)

        super().__init__(**kwargs)

    env: Literal["dev", "prod", "demo", "test"] = Field(default="dev", alias="ENV")
    database_url: str = "sqlite:///./test.db"
    frontend_url: Optional[str] = None
    backend_url: str = "http://localhost:8000"

    secret_key: str = "your_secret_key_here"

    github_client_id: Optional[str] = None
    github_client_secret: Optional[str] = None

    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def is_dev(self):
        return self.env == "dev"

    @property
    def is_prod(self):
        return self.env == "prod"

    @property
    def is_demo(self):
        return self.env == "demo"

    @property
    def available_oauth_providers(self) -> list[str]:
        providers = []
        if self.github_client_id and self.github_client_secret:
            providers.append("github")
        if self.google_client_id and self.google_client_secret:
            providers.append("google")
        return providers


@lru_cache()
def get_settings() -> Settings:
    return Settings()
