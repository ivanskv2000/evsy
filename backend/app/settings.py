import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal, Optional

from dotenv import load_dotenv
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def resolve_env_file() -> Optional[str]:
    env_mode = os.getenv("ENV")
    cwd = Path.cwd()

    candidates = []
    if env_mode:
        candidates.append(cwd / f".env.{env_mode}")
    candidates.append(cwd / ".env")

    backend_root = Path(__file__).parent.parent
    if env_mode:
        candidates.append(backend_root / f".env.{env_mode}")
    candidates.append(backend_root / ".env")

    for path in candidates:
        if path.exists():
            return str(path)
    return None


class Settings(BaseSettings):
    def __init__(self, _env_file: Optional[str] = None, **kwargs: Any):
        if _env_file is None:
            _env_file = resolve_env_file()
        if _env_file:
            load_dotenv(_env_file, override=True)
        super().__init__(**kwargs)

    env: Literal["dev", "prod", "demo", "test"] = Field(default="dev", alias="ENV")
    database_url: str = Field(default="", alias="DATABASE_URL")
    frontend_url: str = Field(default="http://localhost:3000", alias="FRONTEND_URL")
    backend_url: str = Field(default="http://localhost:8000", alias="BACKEND_URL")

    secret_key: str = Field(default="your_secret_key_here", alias="SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    github_client_id: Optional[str] = Field(default=None, alias="GITHUB_CLIENT_ID")
    github_client_secret: Optional[str] = Field(
        default=None, alias="GITHUB_CLIENT_SECRET"
    )

    google_client_id: Optional[str] = Field(default=None, alias="GOOGLE_CLIENT_ID")
    google_client_secret: Optional[str] = Field(
        default=None, alias="GOOGLE_CLIENT_SECRET"
    )

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    @model_validator(mode="after")
    def validate_infrastructure(self) -> "Settings":
        if not self.database_url:
            raise ValueError(
                "DATABASE_URL must be provided in the environment or a .env file"
            )
        return self

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
    def log_level(self) -> str:
        if self.is_dev or self.env == "test":
            return "DEBUG"
        return "INFO"

    @property
    def cors_origins(self) -> list[str]:
        origins = [self.frontend_url]
        if self.is_dev:
            origins.extend(["http://localhost:5173", "http://localhost:3000"])
        return list(set(filter(None, origins)))

    @property
    def masked_database_url(self) -> str:
        from urllib.parse import urlparse, urlunparse

        if not self.database_url:
            return ""
        parsed = urlparse(self.database_url)
        if not parsed.password:
            return self.database_url
        host_port = parsed.hostname or ""
        if parsed.port:
            host_port = f"{host_port}:{parsed.port}"
        user_part = f"{parsed.username}:******@" if parsed.username else "******@"
        return urlunparse(parsed._replace(netloc=f"{user_part}{host_port}"))

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
