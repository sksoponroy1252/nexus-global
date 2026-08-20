# Nexus Global AI Core - Architecture

## Overview

The Nexus Global AI Core is designed with a clean, modular architecture that separates concerns and allows for flexible provider integration.

## Architecture Diagram

```
┌─────────────────────────────┐
│       Application Layer     │
│  (examples/basic_chat.py)   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      AICore                 │
│  - Validation              │
│  - Provider Management     │
│  - Interface               │
└──────────────┬──────────────┘
               │
     ┌─────────┴─────────┐
     │                   │
     ▼                   ▼
┌──────────────┐  ┌─────────────────────┐
│BaseProvider  │  │  Configuration      │
│  (abstract)  │  │  - API Key          │
└──────┬───────┘  │  - Model            │
       │          │  - Temperature      │
       ▼          └─────────────────────┘
┌─────────────────────┐
│ OpenAIProvider      │
│  - Chat API         │
│  - Error Handling   │
│  - Response Parsing │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │ OpenAI API   │
    └──────────────┘
```

## Components

### 1. Configuration (`src/nexus_global/config.py`)

- **Purpose**: Load and validate environment configuration
- **Responsibilities**:
  - Load environment variables from `.env` or OS
  - Validate required settings
  - Provide defaults where appropriate
  - Raise clear errors for invalid configuration

### 2. AICore (`src/nexus_global/core/ai_core.py`)

- **Purpose**: Main interface for AI operations
- **Responsibilities**:
  - Accept pluggable providers
  - Validate user input (prompts)
  - Delegate to provider for actual generation
  - Provide clean, simple API

### 3. BaseProvider (`src/nexus_global/providers/base.py`)

- **Purpose**: Define provider contract
- **Responsibilities**:
  - Abstract base class for all providers
  - Define required `generate()` method
  - Ensure consistent interface

### 4. OpenAIProvider (`src/nexus_global/providers/openai_provider.py`)

- **Purpose**: OpenAI-specific implementation
- **Responsibilities**:
  - Manage OpenAI client initialization
  - Implement `generate()` method
  - Handle API-specific errors
  - Support configuration parameters (temperature, model, etc.)

## Design Principles

### 1. Provider Abstraction

The `BaseProvider` interface decouples AICore from specific implementations. New providers can be added without modifying AICore.

```python
from nexus_global.providers.base import BaseProvider

class MyCustomProvider(BaseProvider):
    def generate(self, prompt: str, **kwargs) -> str:
        # Implementation
        pass

core = AICore(provider=MyCustomProvider())
```

### 2. Configuration Management

Configuration is centralized and validated at load time, preventing runtime surprises.

```python
from nexus_global.config import load_config

config = load_config()  # Raises ConfigError if invalid
```

### 3. Error Handling

Custom exceptions provide clear, actionable error messages without exposing sensitive data.

```python
from nexus_global.providers.openai_provider import OpenAIProviderError

try:
    response = core.generate(prompt)
except OpenAIProviderError as e:
    # Handle API-specific errors
    pass
```

### 4. Type Hints

Full type annotations support IDE autocomplete and type checking with mypy.

## Future Extensions

The architecture supports adding:

- **Additional Providers**: Anthropic, Google, Groq, etc.
- **Provider Features**: Streaming, async operations, token counting
- **Middleware**: Logging, caching, rate limiting
- **Agents**: Higher-level orchestration (future phase)
- **Memory**: Context persistence (future phase)

## Testing Strategy

- **Unit Tests**: Test each component in isolation using mocks
- **Integration Tests**: Test provider integration with mocked APIs
- **Configuration Tests**: Validate configuration loading and validation

No tests make real API requests. All external dependencies are mocked.
