"""
AI Provider Package and Factory.
"""

from typing import Optional
from backend.app.ai_engine.providers.base import AIProvider, AIProviderResponse
from backend.app.ai_engine.providers.mock_provider import MockDeterministicAIProvider
from backend.app.ai_engine.providers.ollama_provider import OllamaAIProvider
from backend.app.ai_engine.providers.cloud_provider import CloudAIProvider
from backend.app.config import settings


def get_ai_provider(provider_type: Optional[str] = None) -> AIProvider:
    """
    Factory function returning the configured AI Provider instance.
    Prioritizes real Cloud LLM (Gemini / OpenAI) whenever keys are provided.
    """
    p_type = (provider_type or settings.AI_PROVIDER or "").lower()

    if p_type in ["mock", "mock_deterministic", "offline"]:
        return MockDeterministicAIProvider()
    elif p_type == "ollama":
        return OllamaAIProvider()
    elif p_type in ["gemini", "google"]:
        return CloudAIProvider(provider_type="gemini")
    elif p_type in ["openai", "gpt"]:
        return CloudAIProvider(provider_type="openai")
    
    # Auto-detection: If Gemini Key exists, use Gemini
    if settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY) > 10:
        return CloudAIProvider(provider_type="gemini")
    
    # If OpenAI Key exists, use OpenAI
    if settings.OPENAI_API_KEY and len(settings.OPENAI_API_KEY) > 10:
        return CloudAIProvider(provider_type="openai")

    # Default fallback
    return MockDeterministicAIProvider()


__all__ = [
    "AIProvider",
    "AIProviderResponse",
    "MockDeterministicAIProvider",
    "OllamaAIProvider",
    "CloudAIProvider",
    "get_ai_provider",
]
