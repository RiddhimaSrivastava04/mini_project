"""Tests for application configuration."""

import pytest

from app.config.settings import ConfigurationError, load_settings


def test_load_settings_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "test-model")
    monkeypatch.setenv("TEMPERATURE", "0.7")

    settings = load_settings()

    assert settings.gemini_api_key == "test-key"
    assert settings.gemini_model == "test-model"
    assert settings.temperature == 0.7


def test_missing_api_key_raises_clear_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr("app.config.settings.load_dotenv", lambda: None)

    with pytest.raises(ConfigurationError, match="GEMINI_API_KEY"):
        load_settings()
