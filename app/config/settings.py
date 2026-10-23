"""Environment-backed application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


class ConfigurationError(RuntimeError):
    """Raised when required application configuration is unavailable."""


@dataclass(frozen=True)
class Settings:
    """Runtime configuration for the application."""

    gemini_api_key: str
    gemini_model: str = "gemini-flash-latest"
    temperature: float = 0.2


def load_settings() -> Settings:
    """Load and validate settings from the environment and ``.env`` file."""
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ConfigurationError(
            "GEMINI_API_KEY is not configured. Create a .env file from "
            ".env.example and add your Gemini API key."
        )

    model = os.getenv("GEMINI_MODEL", "gemini-flash-latest").strip() or "gemini-flash-latest"
    temperature_value = os.getenv("TEMPERATURE", "0.2").strip()
    try:
        temperature = float(temperature_value)
    except ValueError as exc:
        raise ConfigurationError(
            "TEMPERATURE must be a number between 0 and 2."
        ) from exc

    if not 0 <= temperature <= 2:
        raise ConfigurationError("TEMPERATURE must be between 0 and 2.")

    return Settings(
        gemini_api_key=api_key,
        gemini_model=model,
        temperature=temperature,
    )
