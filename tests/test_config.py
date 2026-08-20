"""Tests for configuration module."""

import os
import tempfile
from pathlib import Path

import pytest

from nexus_global.config import Config, ConfigError, load_config


class TestConfig:
    """Test Config dataclass."""

    def test_config_creation(self) -> None:
        """Test creating a valid config."""
        config = Config(
            openai_api_key="test-key-123",
            ai_model="gpt-4",
            ai_temperature=0.7,
        )
        assert config.openai_api_key == "test-key-123"
        assert config.ai_model == "gpt-4"
        assert config.ai_temperature == 0.7

    def test_config_validation_missing_api_key(self) -> None:
        """Test that validation fails when API key is missing."""
        config = Config(
            openai_api_key="",
            ai_model="gpt-4",
        )
        with pytest.raises(ConfigError, match="OPENAI_API_KEY is required"):
            config.validate()

    def test_config_validation_invalid_temperature(self) -> None:
        """Test that validation fails for invalid temperature."""
        config = Config(
            openai_api_key="test-key",
            ai_temperature=3.5,  # Out of range
        )
        with pytest.raises(ConfigError, match="must be between 0 and 2"):
            config.validate()

    def test_config_validation_temperature_as_string(self) -> None:
        """Test that validation fails for non-numeric temperature."""
        config = Config(
            openai_api_key="test-key",
            ai_temperature="not-a-number",  # type: ignore
        )
        with pytest.raises(ConfigError, match="must be a number"):
            config.validate()


class TestLoadConfig:
    """Test load_config function."""

    def test_load_config_from_env(self, monkeypatch) -> None:
        """Test loading config from environment variables."""
        monkeypatch.setenv("OPENAI_API_KEY", "env-test-key")
        monkeypatch.setenv("NEXUS_AI_MODEL", "gpt-3.5-turbo")
        monkeypatch.setenv("NEXUS_AI_TEMPERATURE", "0.5")

        config = load_config(env_file="/nonexistent/.env")

        assert config.openai_api_key == "env-test-key"
        assert config.ai_model == "gpt-3.5-turbo"
        assert config.ai_temperature == 0.5

    def test_load_config_defaults(self, monkeypatch) -> None:
        """Test that defaults are used when env vars are not set."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("NEXUS_AI_MODEL", raising=False)
        monkeypatch.delenv("NEXUS_AI_TEMPERATURE", raising=False)
        monkeypatch.setenv("OPENAI_API_KEY", "test-key-for-defaults")

        config = load_config(env_file="/nonexistent/.env")

        assert config.openai_api_key == "test-key-for-defaults"
        assert config.ai_model == "gpt-4"  # default
        assert config.ai_temperature == 0.7  # default

    def test_load_config_missing_api_key(self, monkeypatch) -> None:
        """Test that loading config fails when API key is missing."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.setenv("OPENAI_API_KEY", "")

        with pytest.raises(ConfigError, match="OPENAI_API_KEY is required"):
            load_config(env_file="/nonexistent/.env")

    def test_load_config_invalid_temperature(self, monkeypatch) -> None:
        """Test that loading config fails for invalid temperature."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        monkeypatch.setenv("NEXUS_AI_TEMPERATURE", "not-a-number")

        with pytest.raises(ConfigError, match="must be a valid number"):
            load_config(env_file="/nonexistent/.env")

    def test_load_config_from_file(self, tmp_path) -> None:
        """Test loading config from .env file."""
        env_file = tmp_path / ".env"
        env_file.write_text(
            "OPENAI_API_KEY=file-test-key\n"
            "NEXUS_AI_MODEL=gpt-4-turbo\n"
            "NEXUS_AI_TEMPERATURE=0.9\n"
        )

        config = load_config(env_file=str(env_file))

        assert config.openai_api_key == "file-test-key"
        assert config.ai_model == "gpt-4-turbo"
        assert config.ai_temperature == 0.9
