"""Gemini-backed answer generation service."""

from __future__ import annotations

import logging
import time
from collections.abc import Sequence

from google import genai
from google.genai import types
from google.genai.errors import APIError, ClientError, ServerError

from app.config.settings import Settings

logger = logging.getLogger(__name__)


class GeminiServiceError(RuntimeError):
    """Raised when an answer cannot be generated safely."""


class GeminiService:
    """Encapsulates all communication with the Gemini API."""

    def __init__(
        self, settings: Settings, client: genai.Client | None = None
    ) -> None:
        self._settings = settings
        self._client = client or genai.Client(api_key=settings.gemini_api_key)

    def generate_answer(
        self, messages: Sequence[dict[str, str]], *, temperature: float | None = None
    ) -> str:
        """Generate an answer for a conversation represented by chat messages."""
        system_instruction = next(
            (message["content"] for message in messages if message["role"] == "system"),
            None,
        )
        contents = [
            {
                "role": "model" if message["role"] == "assistant" else "user",
                "parts": [{"text": message["content"]}],
            }
            for message in messages
            if message["role"] != "system"
        ]

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=(
                self._settings.temperature if temperature is None else temperature
            ),
        )

        try:
            response = None
            for attempt in range(2):
                try:
                    response = self._client.models.generate_content(
                        model=self._settings.gemini_model,
                        contents=contents,
                        config=config,
                    )
                    break
                except ServerError as exc:
                    if attempt == 1:
                        raise exc
                    time.sleep(1)
            answer = response.text
        except ServerError as exc:
            logger.error("Gemini server error (%s).", exc.code)
            raise GeminiServiceError(
                "Gemini is temporarily unavailable. Please wait a moment and try again."
            ) from exc
        except ClientError as exc:
            logger.error("Gemini client error (%s).", exc.code)
            if exc.code in (401, 403):
                message = (
                    "Gemini rejected the API key. Check GEMINI_API_KEY and try again."
                )
            elif exc.code == 429:
                message = (
                    "Gemini usage is temporarily limited. Check your API quota "
                    "and try again later."
                )
            else:
                message = (
                    "Gemini could not process the request. Check the model and "
                    "API configuration, then try again."
                )
            raise GeminiServiceError(message) from exc
        except (APIError, AttributeError, IndexError, TypeError, ValueError) as exc:
            logger.error("Gemini answer generation failed (%s).", type(exc).__name__)
            raise GeminiServiceError(
                "We could not generate an answer right now. Please try again."
            ) from exc

        if not answer or not answer.strip():
            logger.error("Gemini returned an empty answer.")
            raise GeminiServiceError(
                "The model returned an empty answer. Please try asking again."
            )

        return answer.strip()
