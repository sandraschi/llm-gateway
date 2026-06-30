"""Novita AI adapter — OpenAI-compatible."""

from llm_gateway.adapters.openai import OpenAIAdapter
from llm_gateway.base import register_provider


@register_provider("novita")
class NovitaAdapter(OpenAIAdapter):
    provider = "novita"
    base_url = "https://api.novita.ai/v3/openai"
    api_key_env = "NOVITA_API_KEY"
