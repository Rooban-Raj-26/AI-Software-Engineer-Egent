"""
Abstract interface all LLM providers must implement.
Agents (Planner, Reviewer, Debugger, etc.) will depend on this
interface only — never on a concrete provider class directly.
"""
from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Contract every LLM provider (Gemini, GitHub Models, etc.) must follow."""

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """
        Send a prompt to the LLM and return its text response.
        Must be implemented by every concrete provider.
        """
        raise NotImplementedError