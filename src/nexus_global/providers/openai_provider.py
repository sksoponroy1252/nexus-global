"""OpenAI provider implementation.

Provides integration with OpenAI's API.
"""

import os
from typing import Optional

from openai import OpenAI, APIError, APIConnectionError, RateLimitError

from nexus_global.config import Config
from nexus_global.providers.base import BaseProvider


class OpenAIProviderError(Exception):
    """Raised when OpenAI provider encounters an error."""

    pass


class OpenAIProvider(BaseProvider):
    """OpenAI provider using official OpenAI Python SDK.

    Requires OPENAI_API_KEY environment variable or explicit configuration.
    """

    def __init__(self, config: Config) -> None:
        """Initialize OpenAI provider.

        Args:
            config: Configuration containing API key and model settings.

        Raises:
            OpenAIProviderError: If API key is missing or invalid.
        """
        if not config.openai_api_key:
            raise OpenAIProviderError(
                "OpenAI API key is required. Set OPENAI_API_KEY in environment or config."
            )

        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        self.model = config.ai_model
        self.temperature = config.ai_temperature

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using OpenAI API.

        Args:
            prompt: The input prompt.
            **kwargs: Additional parameters (e.g., temperature, max_tokens).
                      Overrides defaults from config.

        Returns:
            Generated response as a string.

        Raises:
            OpenAIProviderError: If API call fails.
        """
        try:
            temperature = kwargs.pop("temperature", self.temperature)
            model = kwargs.pop("model", self.model)
            max_tokens = kwargs.pop("max_tokens", None)

            params = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
            }

            if max_tokens is not None:
                params["max_tokens"] = max_tokens

            response = self.client.chat.completions.create(**params)

            if response.choices and len(response.choices) > 0:
                message_content = response.choices[0].message.content
                if message_content is None:
                    raise OpenAIProviderError("Received empty response from OpenAI.")
                return message_content
            else:
                raise OpenAIProviderError("No choices returned from OpenAI API.")

        except (APIError, APIConnectionError, RateLimitError) as e:
            raise OpenAIProviderError(f"OpenAI API error: {str(e)}") from e
        except Exception as e:
            raise OpenAIProviderError(f"Unexpected error in OpenAI provider: {str(e)}") from e
