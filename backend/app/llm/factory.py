"""
Factory that returns the correct LLM provider based on configuration.
This is the ONLY place in the codebase that should decide which
provider implementation gets instantiated.
"""
from functools import lru_cache
from app.llm.base import BaseLLMProvider
from app.llm.gemini_provider import GeminiProvider
from app.core.config import get_settings


@lru_cache
def get_llm_provider() -> BaseLLMProvider:
    """
    Returns a cached LLM provider instance.
    Currently defaults to Gemini. GitHub Models support will be added
    here in a later phase without touching any agent code.
    """
    settings = get_settings()

    provider_name = "gemini"  # hardcoded for now; will read from settings later

    if provider_name == "gemini":
        return GeminiProvider()

    raise ValueError(f"Unknown LLM provider: {provider_name}")