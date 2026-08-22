"""
Administrative AI Engine Package.
"""

from backend.app.ai_engine.anonymizer import PIIAnonymizer, pii_anonymizer
from backend.app.ai_engine.guardrails import (
    MEDICAL_DISCLAIMER,
    SAFE_REFUSAL_MESSAGE,
    AdminAIGuardrails,
    check_prompt_guardrails,
    BASE_ADMIN_SYSTEM_PROMPT,
    PRE_VISIT_SYSTEM_PROMPT,
    FAQ_CHATBOT_SYSTEM_PROMPT,
    DISCHARGE_SYSTEM_PROMPT,
)
from backend.app.ai_engine.knowledge_base import KnowledgeBase, knowledge_base
from backend.app.ai_engine.providers import (
    AIProvider,
    AIProviderResponse,
    MockDeterministicAIProvider,
    OllamaAIProvider,
    CloudAIProvider,
    get_ai_provider,
)
from backend.app.ai_engine.service import AdminAIService, admin_ai_service

__all__ = [
    "PIIAnonymizer",
    "pii_anonymizer",
    "MEDICAL_DISCLAIMER",
    "SAFE_REFUSAL_MESSAGE",
    "AdminAIGuardrails",
    "check_prompt_guardrails",
    "BASE_ADMIN_SYSTEM_PROMPT",
    "PRE_VISIT_SYSTEM_PROMPT",
    "FAQ_CHATBOT_SYSTEM_PROMPT",
    "DISCHARGE_SYSTEM_PROMPT",
    "KnowledgeBase",
    "knowledge_base",
    "AIProvider",
    "AIProviderResponse",
    "MockDeterministicAIProvider",
    "OllamaAIProvider",
    "CloudAIProvider",
    "get_ai_provider",
    "AdminAIService",
    "admin_ai_service",
]
