"""Nexus Global AI Core - Main interface for AI operations.

Provides a clean, provider-agnostic interface for generating responses.
"""

from typing import Optional

from nexus_global.config import Config, load_config
from nexus_global.providers.base import BaseProvider
from nexus_global.providers.openai_provider import OpenAIProvider


class AICore:
    """Main AI Core for Nexus Global.

    Provides a clean interface for generating responses using pluggable providers.
    """

    def __init__(
        self,
        provider: Optional[BaseProvider] = None,
        config: Optional[Config] = None,
    ) -> None:
        """Initialize AICore.

        Args:
            provider: Optional provider instance. If None, creates default OpenAI provider.
            config: Optional configuration. If None, loads from environment.

        Raises:
            ConfigError: If configuration is invalid when creating default provider.
        """
        if config is None:
            config = load_config()

        self.config = config

        if provider is None:
            self.provider = OpenAIProvider(config)
        else:
            self.provider = provider

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response for the given prompt.

        Args:
            prompt: The input prompt to generate a response for.
            **kwargs: Additional arguments passed to the provider.

        Returns:
            Generated response as a string.

        Raises:
            ValueError: If prompt is empty or invalid.
            Exception: Provider-specific exceptions (API errors, etc.)
        """
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Prompt must be a non-empty string.")

        prompt = prompt.strip()
        if not prompt:
            raise ValueError("Prompt cannot be empty or whitespace-only.")

        return self.provider.generate(prompt, **kwargs)

    def set_provider(self, provider: BaseProvider) -> None:
        """Change the provider at runtime.

        Args:
            provider: New provider instance.
        """
        self.provider = provider
