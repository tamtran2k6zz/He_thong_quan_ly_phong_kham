"""
Cloud AI Provider (Gemini / OpenAI Adapter).
Handles cloud LLM API calls with deterministic fallback support when keys/internet are unavailable.
"""

import time
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any
from backend.app.ai_engine.providers.base import AIProvider, AIProviderResponse
from backend.app.ai_engine.providers.mock_provider import MockDeterministicAIProvider
from backend.app.config import settings


class CloudAIProvider(AIProvider):
    """Cloud LLM Adapter supporting Google Gemini and OpenAI APIs."""

    def __init__(
        self,
        provider_type: str = "gemini",
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        timeout: int = 15
    ):
        self.provider_type = provider_type.lower()
        self.api_key = api_key or (settings.GEMINI_API_KEY if self.provider_type == "gemini" else settings.OPENAI_API_KEY)
        self.model_name = model_name or ("gemini-1.5-flash" if self.provider_type == "gemini" else "gpt-3.5-turbo")
        self.timeout = timeout
        self.fallback_provider = MockDeterministicAIProvider(model_name=f"cloud-fallback-mock:{self.model_name}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AIProviderResponse:
        start_time = time.time()

        # If no API key provided, immediately use fallback
        if not self.api_key:
            fb = self.fallback_provider.generate(prompt, system_prompt=system_prompt, **kwargs)
            elapsed = int((time.time() - start_time) * 1000)
            return AIProviderResponse(
                content=fb.content,
                model=f"{self.provider_type}-local-fallback",
                latency_ms=max(1, elapsed),
                raw_response={"no_api_key": True}
            )

        if self.provider_type == "gemini":
            res = self._call_gemini(prompt, system_prompt, start_time)
            if res:
                return res
        elif self.provider_type == "openai":
            res = self._call_openai(prompt, system_prompt, start_time)
            if res:
                return res

        # Fallback if cloud call fails
        fb = self.fallback_provider.generate(prompt, system_prompt=system_prompt, **kwargs)
        elapsed = int((time.time() - start_time) * 1000)
        return AIProviderResponse(
            content=fb.content,
            model=f"{self.provider_type}-network-fallback",
            latency_ms=max(1, elapsed),
            raw_response={"call_failed_fallback": True}
        )

    def _call_gemini(self, prompt: str, system_prompt: Optional[str], start_time: float) -> Optional[AIProviderResponse]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{system_prompt}\n\n{prompt}" if system_prompt else prompt}
                    ]
                }
            ]
        }
        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    elapsed = int((time.time() - start_time) * 1000)
                    return AIProviderResponse(
                        content=text.strip(),
                        model=f"gemini:{self.model_name}",
                        latency_ms=elapsed,
                        raw_response=data
                    )
        except Exception:
            return None

    def _call_openai(self, prompt: str, system_prompt: Optional[str], start_time: float) -> Optional[AIProviderResponse]:
        url = "https://api.openai.com/v1/chat/completions"
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.3
        }
        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    text = data["choices"][0]["message"]["content"]
                    elapsed = int((time.time() - start_time) * 1000)
                    return AIProviderResponse(
                        content=text.strip(),
                        model=f"openai:{self.model_name}",
                        latency_ms=elapsed,
                        raw_response=data
                    )
        except Exception:
            return None
