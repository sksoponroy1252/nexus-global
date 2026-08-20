"""Tests for provider implementations."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from nexus_global.config import Config
from nexus_global.providers.openai_provider import (
    OpenAIProvider,
    OpenAIProviderError,
)


class TestOpenAIProvider:
    """Test OpenAI provider."""

    @pytest.fixture
    def mock_config(self) -> Config:
        """Create a mock config."""
        return Config(
            openai_api_key="test-api-key-12345",
            ai_model="gpt-4",
            ai_temperature=0.7,
        )

    def test_initialization_with_valid_config(self, mock_config) -> None:
        """Test provider initialization with valid config."""
        with patch("nexus_global.providers.openai_provider.OpenAI"):
            provider = OpenAIProvider(mock_config)

            assert provider.config is mock_config
            assert provider.model == "gpt-4"
            assert provider.temperature == 0.7

    def test_initialization_missing_api_key(self) -> None:
        """Test that provider raises error for missing API key."""
        config = Config(openai_api_key="")

        with pytest.raises(OpenAIProviderError, match="API key is required"):
            OpenAIProvider(config)

    @patch("nexus_global.providers.openai_provider.OpenAI")
    def test_generate_successful_response(self, mock_openai_class, mock_config) -> None:
        """Test successful response generation."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Test response"))
        ]
        mock_client.chat.completions.create.return_value = mock_response

        provider = OpenAIProvider(mock_config)
        response = provider.generate("Test prompt")

        assert response == "Test response"
        mock_client.chat.completions.create.assert_called_once()

    @patch("nexus_global.providers.openai_provider.OpenAI")
    def test_generate_with_custom_temperature(self, mock_openai_class, mock_config) -> None:
        """Test generate with custom temperature parameter."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Response"))
        ]
        mock_client.chat.completions.create.return_value = mock_response

        provider = OpenAIProvider(mock_config)
        provider.generate("Test", temperature=0.3)

        call_args = mock_client.chat.completions.create.call_args
        assert call_args.kwargs["temperature"] == 0.3

    @patch("nexus_global.providers.openai_provider.OpenAI")
    def test_generate_with_max_tokens(self, mock_openai_class, mock_config) -> None:
        """Test generate with max_tokens parameter."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Response"))
        ]
        mock_client.chat.completions.create.return_value = mock_response

        provider = OpenAIProvider(mock_config)
        provider.generate("Test", max_tokens=500)

        call_args = mock_client.chat.completions.create.call_args
        assert call_args.kwargs["max_tokens"] == 500

    @patch("nexus_global.providers.openai_provider.OpenAI")
    def test_generate_empty_response(self, mock_openai_class, mock_config) -> None:
        """Test handling of empty response from API."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content=None))
        ]
        mock_client.chat.completions.create.return_value = mock_response

        provider = OpenAIProvider(mock_config)

        with pytest.raises(OpenAIProviderError, match="empty response"):
            provider.generate("Test")

    @patch("nexus_global.providers.openai_provider.OpenAI")
    def test_generate_no_choices(self, mock_openai_class, mock_config) -> None:
        """Test handling when API returns no choices."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = []
        mock_client.chat.completions.create.return_value = mock_response

        provider = OpenAIProvider(mock_config)

        with pytest.raises(OpenAIProviderError, match="No choices returned"):
            provider.generate("Test")

    @patch("nexus_global.providers.openai_provider.OpenAI")
    def test_generate_api_error(self, mock_openai_class, mock_config) -> None:
        """Test handling of API errors.
        
        Verifies that OpenAI APIError exceptions are caught and wrapped 
        in OpenAIProviderError. Uses patch to inject APIError into the 
        mocked API call without needing to instantiate APIError directly.
        """
        from openai import APIError
        
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Patch APIError at the point it's imported in the production module
        # to avoid constructor signature issues. Set it as the side_effect
        # so it's raised when create() is called.
        with patch("nexus_global.providers.openai_provider.APIError", APIError):
            # Create an instance with correct signature (message, response=None, body=None)
            test_error = APIError(message="Test API error")
            mock_client.chat.completions.create.side_effect = test_error
            
            provider = OpenAIProvider(mock_config)
            
            # Verify that APIError is caught and converted to OpenAIProviderError
            with pytest.raises(OpenAIProviderError, match="OpenAI API error"):
                provider.generate("Test")
