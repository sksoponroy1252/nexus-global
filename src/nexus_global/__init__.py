"""Nexus Global - Open-source AI, automation, and developer infrastructure."""

__version__ = "0.1.0"
__author__ = "Sk Sopon Roy"
__license__ = "MIT"

from nexus_global.core.ai_core import AICore
from nexus_global.providers.base import BaseProvider

__all__ = ["AICore", "BaseProvider", "__version__"]
