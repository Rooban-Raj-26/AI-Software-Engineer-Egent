"""
GitHub Models provider implementation.
Free via GitHub Student Developer Pack / GitHub Models access.
Uses the OpenAI-compatible SDK since GitHub Models exposes an
OpenAI-compatible inference endpoint.
"""
from openai import AsyncOpenAI
from app.llm.base import BaseLLMProvider
from app.core.config import get_settings

GITHUB_MODELS_ENDPOINT = "https://models.inference.ai.azure.com"
GITHUB_MODEL_NAME = "gpt-4o-mini"  # widely available on GitHub Models free tier


class GitHubModelsProvider(BaseLLMProvider):
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.github_models_token:
            raise ValueError(
                "GITHUB_MODELS_TOKEN is not set. Add it to your .env file."
            )
        self._client = AsyncOpenAI(
            base_url=GITHUB_MODELS_ENDPOINT,
            api_key=settings.github_models_token,
        )

    async def generate(self, prompt: str) -> str:
        response = await self._client.chat.completions.create(
            model=GITHUB_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content