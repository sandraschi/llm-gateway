"""OpenAI adapter — pass-through (already OpenAI format)."""

import os
from typing import Any

import httpx

from llm_gateway.base import BaseLLMAdapter, register_provider


@register_provider("openai")
class OpenAIAdapter(BaseLLMAdapter):
    provider = "openai"
    base_url = "https://api.openai.com/v1"
    api_key_env = "OPENAI_API_KEY"

    async def list_models_async(self) -> list[dict[str, Any]]:
        api_key = os.getenv(self.api_key_env)
        if not api_key:
            return self.list_models()
        headers = {"Authorization": f"Bearer {api_key}"}
        return await self._fetch_models_via_api("https://api.openai.com/v1/models", headers)

    def map_params(self, body: dict[str, Any]) -> dict[str, Any]:
        return body

    def transform_response(self, resp_data: dict[str, Any], model: str) -> dict[str, Any]:
        return resp_data

    async def complete(self, body: dict[str, Any], headers: dict[str, Any]) -> dict[str, Any]:
        api_key = self.get_api_key(headers)
        if not api_key:
            raise ValueError("OpenAI API key not set. Set OPENAI_API_KEY env var or pass Authorization header.")
        req_headers = self.build_headers(api_key)
        url = self.build_url(self.get_base_url(headers))

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(url, json=body, headers=req_headers)
            resp.raise_for_status()
            return resp.json()
