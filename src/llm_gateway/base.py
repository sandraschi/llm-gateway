import os
import time
import uuid
from abc import ABC, abstractmethod
from typing import Any

import httpx

_openai_compat_providers: dict[str, type["BaseLLMAdapter"]] = {}


def register_provider(name: str):
    """Decorator to register a provider adapter."""
    def wrapper(cls):
        _openai_compat_providers[name] = cls
        return cls
    return wrapper


def get_adapter(provider: str) -> "BaseLLMAdapter | None":
    cls = _openai_compat_providers.get(provider)
    return cls() if cls else None


def list_providers() -> list[str]:
    return list(_openai_compat_providers.keys())


class BaseLLMAdapter(ABC):
    provider: str = ""
    base_url: str = ""
    api_key_env: str = ""

    def get_base_url(self, headers: dict[str, str]) -> str:
        return self.base_url

    def get_api_key(self, headers: dict[str, str]) -> str:
        env_key = self.api_key_env
        key = os.getenv(env_key, "")
        if not key:
            key = headers.get("authorization", "").replace("Bearer ", "")
        return key

    @abstractmethod
    def map_params(self, body: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    def transform_response(self, resp_data: dict[str, Any], model: str) -> dict[str, Any]:
        ...

    def list_models(self) -> list[dict[str, Any]]:
        """Return available models for this provider. Override for live listing."""
        return [{"id": f"{self.provider}/default", "object": "model", "owned_by": self.provider}]

    async def list_models_async(self) -> list[dict[str, Any]]:
        """Async variant — default calls sync list_models(). Override for API-based listing."""
        return self.list_models()

    async def _fetch_models_via_api(self, url: str, headers: dict | None = None) -> list[dict[str, Any]]:
        """Helper: fetch model list from an OpenAI-compatible /v1/models endpoint."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, headers=headers or {})
                resp.raise_for_status()
                data = resp.json()
                return data.get("data", [])
        except Exception:
            return self.list_models()

    def build_headers(self, api_key: str) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    def build_url(self, base_url: str) -> str:
        return f"{base_url.rstrip('/')}/v1/chat/completions"

    async def complete(self, body: dict[str, Any], headers: dict[str, Any]) -> dict[str, Any]:
        model = body.get("model", "")
        mapped = self.map_params(body)
        api_key = self.get_api_key(headers)
        req_headers = self.build_headers(api_key)
        url = self.build_url(self.get_base_url(headers))

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(url, json=mapped, headers=req_headers)
            resp.raise_for_status()
            data = resp.json()

        return self.transform_response(data, model)

    def _openai_chunk(self, model: str, choice: dict[str, Any], usage: dict[str, Any] | None = None) -> dict[str, Any]:
        return {
            "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [choice],
            "usage": usage or {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }
