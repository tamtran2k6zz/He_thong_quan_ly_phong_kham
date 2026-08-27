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
        timeout: int = 20
    ):
        self.provider_type = provider_type.lower()
        self.api_key = api_key or (settings.GEMINI_API_KEY if self.provider_type == "gemini" else settings.OPENAI_API_KEY)
        
        if self.provider_type == "gemini":
            self.model_name = model_name or settings.GEMINI_MODEL or "gemini-3.6-flash"
        else:
            self.model_name = model_name or settings.OPENAI_MODEL or "gpt-4o-mini"
            
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

        if self.provider_type in ["gemini", "google"]:
            res = self._call_gemini(prompt, system_prompt, start_time)
            if res:
                return res
        elif self.provider_type in ["openai", "gpt"]:
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
        
        full_text = f"{system_prompt}\n\n[YÊU CẦU CỦA NGƯỜI DÙNG / DỮ LIỆU]:\n{prompt}" if system_prompt else prompt
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": full_text}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2048
            }
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
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        text = candidates[0]["content"]["parts"][0]["text"]
                        elapsed = int((time.time() - start_time) * 1000)
                        return AIProviderResponse(
                            content=text.strip(),
                            model=f"gemini:{self.model_name}",
                            latency_ms=elapsed,
                            raw_response=data
                        )
        except Exception as e:
            # Fallback to secondary model if 404
            if "404" in str(e) and self.model_name != "gemini-3.6-flash":
                self.model_name = "gemini-3.6-flash"
                return self._call_gemini(prompt, system_prompt, start_time)
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
            "temperature": 0.2,
            "max_tokens": 2048
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
