"""DeepSeek adapter — OpenAI-compatible."""

from typing import Any

from llm_gateway.adapters.openai import OpenAIAdapter
from llm_gateway.base import register_provider


@register_provider("deepseek")
class DeepSeekAdapter(OpenAIAdapter):
    provider = "deepseek"
    base_url = "https://api.deepseek.com/v1"
    api_key_env = "DEEPSEEK_API_KEY"
    _models = ["deepseek-chat", "deepseek-reasoner"]

    def list_models(self) -> list[dict[str, Any]]:
        return [{"id": m, "object": "model", "owned_by": "deepseek"} for m in self._models]
