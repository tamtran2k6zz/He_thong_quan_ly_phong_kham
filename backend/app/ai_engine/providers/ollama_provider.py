"""
Ollama Local LLM Provider.
Integrates with local Ollama service (default http://localhost:11434).
Includes deterministic fallback if local server is unreachable.
"""

import time
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any
from backend.app.ai_engine.providers.base import AIProvider, AIProviderResponse
from backend.app.ai_engine.providers.mock_provider import MockDeterministicAIProvider
from backend.app.config import settings


class OllamaAIProvider(AIProvider):
    """Local LLM Provider via Ollama REST API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        timeout: int = 15
    ):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model_name = model_name or settings.OLLAMA_MODEL
        self.timeout = timeout
        self.fallback_provider = MockDeterministicAIProvider(model_name="ollama-fallback-mock")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AIProviderResponse:
        start_time = time.time()
        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt or "",
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.2),
                "num_predict": kwargs.get("max_tokens", 1024),
            }
        }

        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                endpoint,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                if response.status == 200:
                    resp_body = json.loads(response.read().decode("utf-8"))
                    content = resp_body.get("response", "")
                    elapsed = int((time.time() - start_time) * 1000)
                    return AIProviderResponse(
                        content=content.strip(),
                        model=f"ollama:{self.model_name}",
                        latency_ms=elapsed,
                        raw_response=resp_body,
                        success=True
                    )
        except Exception as exc:
            # Gracefully fallback to deterministic provider when Ollama is offline
            pass

        # Execute fallback
        fallback_resp = self.fallback_provider.generate(prompt, system_prompt=system_prompt, **kwargs)
        elapsed = int((time.time() - start_time) * 1000)
        return AIProviderResponse(
            content=fallback_resp.content,
            model=f"ollama-offline-fallback:{self.model_name}",
            latency_ms=elapsed,
            raw_response={"fallback": True},
            success=True
        )
