"""Tests for the Gemini service without network calls."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from google.genai.errors import APIError

from app.config.settings import Settings
from app.services.gemini_service import GeminiService, GeminiServiceError


def test_service_initializes_client_with_api_key() -> None:
    settings = Settings(gemini_api_key="test-key")

    with patch("app.services.gemini_service.genai.Client") as gemini_client:
        service = GeminiService(settings)

    assert service is not None
    gemini_client.assert_called_once_with(api_key="test-key")


def test_service_returns_response_content() -> None:
    client = Mock()
    client.models.generate_content.return_value = SimpleNamespace(
        text="  A useful answer.  "
    )
    service = GeminiService(Settings(gemini_api_key="test-key"), client=client)

    answer = service.generate_answer(
        [
            {"role": "system", "content": "Be helpful."},
            {"role": "user", "content": "What is Python?"},
        ]
    )

    assert answer == "A useful answer."
    client.models.generate_content.assert_called_once()


def test_service_hides_api_errors() -> None:
    client = Mock()
    client.models.generate_content.side_effect = APIError(
        code=400, response_json={"error": {"message": "provider error"}}
    )
    service = GeminiService(Settings(gemini_api_key="test-key"), client=client)

    with pytest.raises(GeminiServiceError, match="could not generate an answer"):
        service.generate_answer([{"role": "user", "content": "Hello"}])
