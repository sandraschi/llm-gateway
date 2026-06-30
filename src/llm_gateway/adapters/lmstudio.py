"""LM Studio adapter — OpenAI-compatible local server."""

from typing import Any

from llm_gateway.adapters.openai import OpenAIAdapter
from llm_gateway.base import register_provider


@register_provider("lmstudio")
class LMStudioAdapter(OpenAIAdapter):
    provider = "lmstudio"
    base_url = "http://127.0.0.1:1234/v1"
    api_key_env = ""

    async def list_models_async(self) -> list[dict[str, Any]]:
        return await self._fetch_models_via_api("http://127.0.0.1:1234/v1/models")
