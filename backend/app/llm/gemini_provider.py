"""
Gemini API provider implementation.
Uses Google's current google-genai SDK to fulfill the BaseLLMProvider contract.
"""
from google import genai
from app.llm.base import BaseLLMProvider
from app.core.config import get_settings

GEMINI_MODEL_NAME = "gemini-3.5-flash"


class GeminiProvider(BaseLLMProvider):
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. Add it to your .env file."
            )
        self._client = genai.Client(api_key=settings.gemini_api_key)

    async def generate(self, prompt: str) -> str:
        response = await self._client.aio.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=prompt,
        )
        return response.text