"""
Abstract AI Provider Interface and Response Schema.
Defines common contract across Mock, Ollama, and Cloud AI implementations.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from pydantic import BaseModel


class AIProviderResponse(BaseModel):
    content: str
    model: str
    latency_ms: int = 0
    raw_response: Optional[Dict[str, Any]] = None
    success: bool = True
    error_message: Optional[str] = None

    def __str__(self) -> str:
        return self.content

    def __contains__(self, item: Any) -> bool:
        return item in self.content

    def lower(self) -> str:
        return self.content.lower()

    def upper(self) -> str:
        return self.content.upper()

    def strip(self) -> str:
        return self.content.strip()

    def startswith(self, prefix: str) -> bool:
        return self.content.startswith(prefix)

    def endswith(self, suffix: str) -> bool:
        return self.content.endswith(suffix)

    def replace(self, old: str, new: str) -> str:
        return self.content.replace(old, new)


class AIProvider(ABC):
    """Abstract Base Class for AI Engine Providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AIProviderResponse:
        """
        Executes text generation on the target model.
        Args:
            prompt: User/Task prompt with anonymized PII.
            system_prompt: System instructions and guardrails.
            **kwargs: Extra parameters (temperature, max_tokens, etc.)
        Returns:
            AIProviderResponse containing content, model name, and latency.
        """
        pass
