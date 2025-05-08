from pathlib import Path

import pytest

from app.settings import Settings


def write_temp_env(dir_path: Path, filename: str, content: str) -> Path:
    env_file = dir_path / filename
    env_file.write_text(content)
    return env_file


def test_dev_env_flags(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("ENV", "dev")
    write_temp_env(tmp_path, ".env.dev", "ENV=dev")

    monkeypatch.chdir(tmp_path)

    settings = Settings()
    assert settings.env == "dev"
    assert settings.is_dev is True
    assert settings.is_prod is False
    assert settings.is_demo is False


def test_invalid_env_rejected(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("ENV", "staging")
    write_temp_env(tmp_path, ".env.staging", "ENV=staging")

    monkeypatch.chdir(tmp_path)

    with pytest.raises(ValueError):
        Settings()


def test_fallback_to_dotenv(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("ENV", raising=False)
    write_temp_env(tmp_path, ".env", "ENV=demo")

    monkeypatch.chdir(tmp_path)

    settings = Settings()
    assert settings.env == "demo"
    assert settings.is_demo is True
