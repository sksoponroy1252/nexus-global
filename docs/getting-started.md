# Getting Started with Nexus Global AI Core

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- An OpenAI API key

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sksoponroy1252/nexus-global.git
cd nexus-global
```

### 2. Create a Python Virtual Environment

**On macOS/Linux:**

```bash
python3.11 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

To also install development tools (for testing and code quality):

```bash
pip install -e ".[dev]"
```

## Configuration

### 1. Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

### 2. Add Your API Key

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
NEXUS_AI_MODEL=gpt-4
NEXUS_AI_TEMPERATURE=0.7
```

**Important**: Never commit `.env` to version control. It's in `.gitignore` by default.

## Running the Example

```bash
python examples/basic_chat.py
```

You should see output like:

```
🚀 Nexus Global AI Core - Basic Chat Example
==================================================

Initializing AI Core...
✅ AI Core initialized

--- Prompt 1 ---
User: What is artificial intelligence in simple terms?

Assistant: Artificial intelligence (AI) is...
```

## Running Tests

Run all tests with pytest:

```bash
pytest
```

With coverage report:

```bash
pytest --cov=src/nexus_global --cov-report=html
```

View the coverage report:

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Basic Usage

### Simple Text Generation

```python
from nexus_global.core.ai_core import AICore

# Create AI Core (uses config from .env)
core = AICore()

# Generate a response
response = core.generate("Explain quantum computing in simple terms.")
print(response)
```

### With Custom Configuration

```python
from nexus_global.core.ai_core import AICore
from nexus_global.config import Config

config = Config(
    openai_api_key="your-api-key",
    ai_model="gpt-3.5-turbo",
    ai_temperature=0.5,
)

core = AICore(config=config)
response = core.generate("What is machine learning?")
```

### With Custom Provider

```python
from nexus_global.core.ai_core import AICore
from nexus_global.providers.openai_provider import OpenAIProvider
from nexus_global.config import load_config

config = load_config()
provider = OpenAIProvider(config)
core = AICore(provider=provider)

response = core.generate("Your prompt here")
```

### Generate with Custom Parameters

```python
response = core.generate(
    "Write a creative story.",
    temperature=0.9,  # More creative
    max_tokens=500,
)
```

## Error Handling

```python
from nexus_global.core.ai_core import AICore
from nexus_global.config import ConfigError
from nexus_global.providers.openai_provider import OpenAIProviderError

try:
    core = AICore()
    response = core.generate("Your prompt")
except ConfigError as e:
    print(f"Configuration error: {e}")
except OpenAIProviderError as e:
    print(f"API error: {e}")
except ValueError as e:
    print(f"Input error: {e}")
```

## Troubleshooting

### "OPENAI_API_KEY is required"

- Check that `.env` file exists
- Verify `OPENAI_API_KEY` is set in `.env`
- Ensure the `.env` file is in the correct directory

### "ModuleNotFoundError: No module named 'nexus_global'"

- Install in development mode: `pip install -e .`
- Verify virtual environment is activated

### "OpenAI API error: Incorrect API key provided"

- Verify your OpenAI API key is correct
- Check that the key hasn't been revoked
- Ensure you have API quota available

## Next Steps

- Read [Architecture Documentation](./architecture.md)
- Explore the [examples/](../examples/) directory
- Check the [API Documentation](../README.md#api-reference)
- Contribute: See [CONTRIBUTING.md](../CONTRIBUTING.md)

## Support

For issues and questions:
- Open an issue on [GitHub Issues](https://github.com/sksoponroy1252/nexus-global/issues)
- Join discussions on [GitHub Discussions](https://github.com/sksoponroy1252/nexus-global/discussions)
