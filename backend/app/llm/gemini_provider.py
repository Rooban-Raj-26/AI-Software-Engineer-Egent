"""
Gemini API provider implementation.
Uses Google's current google-genai SDK to fulfill the BaseLLMProvider contract.
Model name is configurable via .env (GEMINI_MODEL_NAME) since free-tier
quotas and model availability change over time.
"""
from google import genai
from app.llm.base import BaseLLMProvider
from app.core.config import get_settings


class GeminiProvider(BaseLLMProvider):
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. Add it to your .env file."
            )
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._model_name = settings.gemini_model_name

    async def generate(self, prompt: str) -> str:
        response = await self._client.aio.models.generate_content(
            model=self._model_name,
            contents=prompt,
        )
        return response.text