from pathlib import Path

import pytest

from app.settings import Settings


def write_temp_env(dir_path: Path, filename: str, content: str) -> Path:
    env_file = dir_path / filename
    env_file.write_text(content)
    return env_file


def test_dev_env_flags(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("ENV", "dev")
    url = "postgresql://user:pass@localhost/db"
    monkeypatch.setenv("DATABASE_URL", url)
    env_file = write_temp_env(tmp_path, ".env.dev", f"ENV=dev\nDATABASE_URL={url}")

    settings = Settings(_env_file=str(env_file))
    assert settings.env == "dev"
    assert settings.is_dev is True
    assert settings.is_prod is False
    assert settings.is_demo is False
    assert settings.log_level == "DEBUG"
    assert "http://localhost:3000" in settings.cors_origins


def test_settings_masked_db_url():
    """Test that database password is masked in masked_database_url."""
    url = "postgresql+psycopg2://user:secret_pass@localhost:5432/db"
    settings = Settings.model_construct(database_url=url)
    
    masked = settings.masked_database_url
    assert "secret_pass" not in masked
    assert "******" in masked
    assert "user:******@localhost:5432/db" in masked


def test_settings_masked_db_url_no_pass():
    """Test masked_database_url when no password is present."""
    url = "postgresql://localhost/db"
    settings = Settings.model_construct(database_url=url)
    assert settings.masked_database_url == url


def test_invalid_env_rejected(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("ENV", "staging")
    url = "postgresql://localhost/db"
    monkeypatch.setenv("DATABASE_URL", url)
    env_file = write_temp_env(tmp_path, ".env.staging", f"ENV=staging\nDATABASE_URL={url}")

    with pytest.raises(ValueError):
        Settings(_env_file=str(env_file))


def test_fallback_to_dotenv(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("ENV", raising=False)
    url = "postgresql://localhost/db"
    monkeypatch.setenv("DATABASE_URL", url)
    env_file = write_temp_env(tmp_path, ".env", f"ENV=demo\nDATABASE_URL={url}")

    settings = Settings(_env_file=str(env_file))
    assert settings.env == "demo"
    assert settings.is_demo is True
