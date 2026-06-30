"""xAI (Grok) adapter — OpenAI-compatible."""

from typing import Any

from llm_gateway.adapters.openai import OpenAIAdapter
from llm_gateway.base import register_provider


@register_provider("xai")
class XAIAdapter(OpenAIAdapter):
    provider = "xai"
    base_url = "https://api.x.ai/v1"
    api_key_env = "XAI_API_KEY"
    _models = ["grok-3", "grok-3-mini", "grok-3-latest", "grok-2-latest"]

    def list_models(self) -> list[dict[str, Any]]:
        return [{"id": m, "object": "model", "owned_by": "xai"} for m in self._models]
