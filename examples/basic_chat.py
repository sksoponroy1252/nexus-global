#!/usr/bin/env python3
"""Basic chat example using Nexus Global AI Core.

Demonstrates:
- Loading configuration
- Creating AICore
- Generating responses
- Error handling

Before running:
1. Create .env file with OPENAI_API_KEY
2. Install nexus-global: pip install -e .

Usage:
    python examples/basic_chat.py
"""

import sys

from nexus_global.config import ConfigError
from nexus_global.core.ai_core import AICore
from nexus_global.providers.openai_provider import OpenAIProviderError


def main() -> None:
    """Run basic chat example."""
    try:
        print("🚀 Nexus Global AI Core - Basic Chat Example")
        print("=" * 50)

        # Initialize AICore with default configuration
        print("\nInitializing AI Core...")
        core = AICore()
        print("✅ AI Core initialized")

        # Example prompts
        prompts = [
            "What is artificial intelligence in simple terms?",
            "Explain the concept of machine learning briefly.",
        ]

        # Generate responses
        for i, prompt in enumerate(prompts, 1):
            print(f"\n--- Prompt {i} ---")
            print(f"User: {prompt}")

            try:
                response = core.generate(prompt)
                print(f"\nAssistant: {response}")
            except OpenAIProviderError as e:
                print(f"❌ Provider Error: {e}")
                sys.exit(1)
            except Exception as e:
                print(f"❌ Unexpected Error: {e}")
                sys.exit(1)

        print("\n" + "=" * 50)
        print("✅ Example completed successfully!")

    except ConfigError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nMake sure to:")
        print("1. Copy .env.example to .env")
        print("2. Add your OPENAI_API_KEY to .env")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
