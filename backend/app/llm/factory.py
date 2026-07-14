"""
Factory that returns the correct LLM provider based on configuration,
with automatic fallback from Gemini to GitHub Models on failure.
"""
import logging
from app.llm.base import BaseLLMProvider
from app.llm.gemini_provider import GeminiProvider
from app.llm.github_provider import GitHubModelsProvider
from app.core.config import get_settings

logger = logging.getLogger(__name__)


class FallbackLLMProvider(BaseLLMProvider):
    """
    Tries the primary provider first; on any exception, logs a warning
    and falls back to the secondary provider. If both fail, the
    secondary's exception propagates.
    """

    def __init__(self, primary: BaseLLMProvider, secondary: BaseLLMProvider | None):
        self._primary = primary
        self._secondary = secondary

    async def generate(self, prompt: str) -> str:
        try:
            return await self._primary.generate(prompt)
        except Exception as e:
            logger.warning(f"Primary LLM provider failed: {e}")
            if self._secondary is None:
                raise
            logger.info("Falling back to secondary LLM provider (GitHub Models)")
            return await self._secondary.generate(prompt)


def get_llm_provider() -> BaseLLMProvider:
    """
    Returns a provider with automatic fallback: Gemini -> GitHub Models.
    Not cached with @lru_cache anymore since we want fresh instantiation
    to respect any .env changes without a full process restart in dev.
    """
    settings = get_settings()

    primary = GeminiProvider()

    secondary = None
    if settings.github_models_token:
        try:
            secondary = GitHubModelsProvider()
        except ValueError:
            logger.warning("GITHUB_MODELS_TOKEN set but provider init failed; no fallback available")

    return FallbackLLMProvider(primary, secondary)