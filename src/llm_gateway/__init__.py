"""llm-gateway — 28 LLM providers through one OpenAI-compatible endpoint.

Usage (standalone):
    uv run llm-gateway

Usage (embedded):
    from llm_gateway import gateway_router
    app.include_router(gateway_router)
"""

# Import adapters first to trigger @register_provider decorators
import llm_gateway.adapters  # noqa: F401

from llm_gateway.router import gateway_router

__all__ = ["gateway_router"]
