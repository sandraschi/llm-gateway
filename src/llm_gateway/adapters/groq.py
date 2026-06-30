"""Groq adapter — OpenAI-compatible."""

import os
from typing import Any

from llm_gateway.adapters.openai import OpenAIAdapter
from llm_gateway.base import register_provider


@register_provider("groq")
class GroqAdapter(OpenAIAdapter):
    provider = "groq"
    base_url = "https://api.groq.com/openai/v1"
    api_key_env = "GROQ_API_KEY"

    async def list_models_async(self) -> list[dict[str, Any]]:
        api_key = os.getenv(self.api_key_env)
        if not api_key:
            return self.list_models()
        headers = {"Authorization": f"Bearer {api_key}"}
        return await self._fetch_models_via_api("https://api.groq.com/openai/v1/models", headers)
