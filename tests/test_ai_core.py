"""Tests for AICore."""

import pytest
from unittest.mock import Mock, patch

from nexus_global.config import Config
from nexus_global.core.ai_core import AICore
from nexus_global.providers.base import BaseProvider


class MockProvider(BaseProvider):
    """Mock provider for testing."""

    def __init__(self, response: str = "Mock response") -> None:
        self.response = response
        self.last_prompt = None

    def generate(self, prompt: str, **kwargs) -> str:
        self.last_prompt = prompt
        return self.response


class TestAICore:
    """Test AICore class."""

    @pytest.fixture
    def mock_config(self) -> Config:
        """Create a mock config."""
        return Config(
            openai_api_key="test-key",
            ai_model="gpt-4",
            ai_temperature=0.7,
        )

    def test_aicore_initialization_with_provider(self, mock_config) -> None:
        """Test AICore initialization with explicit provider."""
        mock_provider = MockProvider()
        core = AICore(provider=mock_provider, config=mock_config)

        assert core.provider is mock_provider
        assert core.config is mock_config

    @patch("nexus_global.core.ai_core.OpenAIProvider")
    @patch("nexus_global.core.ai_core.load_config")
    def test_aicore_initialization_default_provider(self, mock_load_config, mock_openai_provider) -> None:
        """Test AICore initialization creates default OpenAI provider."""
        mock_config = Config(openai_api_key="test-key")
        mock_load_config.return_value = mock_config

        core = AICore()

        mock_load_config.assert_called_once()
        mock_openai_provider.assert_called_once_with(mock_config)

    def test_generate_with_valid_prompt(self, mock_config) -> None:
        """Test generate with valid prompt."""
        mock_provider = MockProvider(response="Test response")
        core = AICore(provider=mock_provider, config=mock_config)

        response = core.generate("Hello, AI!")

        assert response == "Test response"
        assert mock_provider.last_prompt == "Hello, AI!"

    def test_generate_with_empty_prompt(self, mock_config) -> None:
        """Test generate raises error for empty prompt."""
        mock_provider = MockProvider()
        core = AICore(provider=mock_provider, config=mock_config)

        with pytest.raises(ValueError, match="non-empty string"):
            core.generate("")

    def test_generate_with_whitespace_only_prompt(self, mock_config) -> None:
        """Test generate raises error for whitespace-only prompt."""
        mock_provider = MockProvider()
        core = AICore(provider=mock_provider, config=mock_config)

        with pytest.raises(ValueError, match="empty or whitespace-only"):
            core.generate("   \n  \t  ")

    def test_generate_with_non_string_prompt(self, mock_config) -> None:
        """Test generate raises error for non-string prompt."""
        mock_provider = MockProvider()
        core = AICore(provider=mock_provider, config=mock_config)

        with pytest.raises(ValueError, match="non-empty string"):
            core.generate(123)  # type: ignore

    def test_generate_strips_whitespace(self, mock_config) -> None:
        """Test generate strips leading/trailing whitespace from prompt."""
        mock_provider = MockProvider()
        core = AICore(provider=mock_provider, config=mock_config)

        core.generate("  Hello, AI!  ")

        assert mock_provider.last_prompt == "Hello, AI!"

    def test_set_provider(self, mock_config) -> None:
        """Test changing provider at runtime."""
        mock_provider_1 = MockProvider(response="Response 1")
        mock_provider_2 = MockProvider(response="Response 2")

        core = AICore(provider=mock_provider_1, config=mock_config)
        assert core.generate("Test") == "Response 1"

        core.set_provider(mock_provider_2)
        assert core.generate("Test") == "Response 2"

    def test_generate_passes_kwargs_to_provider(self, mock_config) -> None:
        """Test that generate passes kwargs to provider."""
        mock_provider = Mock(spec=BaseProvider)
        mock_provider.generate.return_value = "Test response"

        core = AICore(provider=mock_provider, config=mock_config)
        core.generate("Test prompt", temperature=0.5, max_tokens=100)

        mock_provider.generate.assert_called_once_with(
            "Test prompt", temperature=0.5, max_tokens=100
        )
