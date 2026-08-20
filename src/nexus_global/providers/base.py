"""Base provider interface for AI services.

Defines the contract that all provider implementations must follow.
"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Abstract base class for AI service providers.

    All providers must implement this interface.
    """

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response for the given prompt.

        Args:
            prompt: The input prompt to generate a response for.
            **kwargs: Provider-specific parameters (temperature, max_tokens, etc.)

        Returns:
            Generated response as a string.

        Raises:
            ValueError: If prompt is invalid.
            Exception: Provider-specific exceptions.
        """
        pass
