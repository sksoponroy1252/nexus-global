"""Configuration module for Nexus Global.

Loads environment variables and provides configuration validation.
"""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


class ConfigError(Exception):
    """Raised when configuration is invalid or incomplete."""

    pass


@dataclass
class Config:
    """Application configuration."""

    openai_api_key: str
    ai_model: str = "gpt-4"
    ai_temperature: float = 0.7
    environment: str = "development"

    def validate(self) -> None:
        """Validate configuration.

        Raises:
            ConfigError: If required configuration is missing or invalid.
        """
        if not self.openai_api_key:
            raise ConfigError(
                "OPENAI_API_KEY is required. Set it in .env or environment."
            )

        if not isinstance(self.ai_temperature, (int, float)):
            raise ConfigError("NEXUS_AI_TEMPERATURE must be a number.")

        if not (0 <= self.ai_temperature <= 2):
            raise ConfigError("NEXUS_AI_TEMPERATURE must be between 0 and 2.")


def load_config(env_file: Optional[str] = None) -> Config:
    """Load configuration from environment.

    Args:
        env_file: Optional path to .env file. If None, looks for .env in current directory.

    Returns:
        Config: Application configuration.

    Raises:
        ConfigError: If configuration is invalid or incomplete.
    """
    if env_file is None:
        env_file = ".env"

    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    ai_model = os.getenv("NEXUS_AI_MODEL", "gpt-4").strip()
    ai_temperature_str = os.getenv("NEXUS_AI_TEMPERATURE", "0.7").strip()
    environment = os.getenv("NEXUS_ENV", "development").strip()

    try:
        ai_temperature = float(ai_temperature_str)
    except ValueError:
        raise ConfigError(
            f"NEXUS_AI_TEMPERATURE must be a valid number, got: {ai_temperature_str}"
        )

    config = Config(
        openai_api_key=openai_api_key,
        ai_model=ai_model,
        ai_temperature=ai_temperature,
        environment=environment,
    )

    config.validate()
    return config
