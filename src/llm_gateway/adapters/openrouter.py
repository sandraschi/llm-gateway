"""OpenRouter adapter — OpenAI-compatible."""

from typing import Any

from llm_gateway.adapters.openai import OpenAIAdapter
from llm_gateway.base import register_provider


@register_provider("openrouter")
class OpenRouterAdapter(OpenAIAdapter):
    provider = "openrouter"
    base_url = "https://openrouter.ai/api/v1"
    api_key_env = "OPENROUTER_API_KEY"

    async def list_models_async(self) -> list[dict[str, Any]]:
        return await self._fetch_models_via_api("https://openrouter.ai/api/v1/models")
