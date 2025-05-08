import os
from pathlib import Path
from typing import Literal, Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


def resolve_env_file(base_dir: str = ".") -> str:
    env_mode = os.getenv("ENV", "dev")
    path = Path(base_dir) / f".env.{env_mode}"
    return str(path) if path.exists() else str(Path(base_dir) / ".env")


class Settings(BaseSettings):
    env: Literal["dev", "prod", "demo"] = "dev"
    database_url: str = "sqlite:///./test.db"
    frontend_url: Optional[str] = None

    secret_key: Optional[str] = None

    model_config = ConfigDict(
        env_file=resolve_env_file(),
        env_file_encoding="utf-8",
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
