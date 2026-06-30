import logging

from fastapi import APIRouter, HTTPException, Request

from llm_gateway.base import get_adapter, list_providers

logger = logging.getLogger(__name__)
gateway_router = APIRouter()


@gateway_router.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """OpenAI-compatible chat completions endpoint.

    Selects provider via x-lightport-provider header or model prefix.
    """
    body = await request.json()
    headers = dict(request.headers)

    provider_name = headers.get("x-lightport-provider", "")
    if not provider_name:
        model = body.get("model", "")
        provider_name = model.split("/")[0] if "/" in model else "openai"

    adapter = get_adapter(provider_name)
    if not adapter:
        available = list_providers()
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"Unknown provider '{provider_name}'. Available: {', '.join(available)}",
                "provider": provider_name,
                "available_providers": available,
            },
        )

    try:
        return await adapter.complete(body, headers)
    except Exception as e:
        logger.error("Gateway error for provider '%s': %s", provider_name, e)
        raise HTTPException(
            status_code=502,
            detail={"error": str(e), "provider": provider_name},
        )


@gateway_router.get("/v1/models")
async def list_models():
    """List available model IDs per registered provider."""
    providers = list_providers()
    return {
        "object": "list",
        "data": [
            {"id": f"{p}/default", "object": "model", "created": 0, "owned_by": p}
            for p in providers
        ],
    }


@gateway_router.get("/v1/gateway/providers")
async def gateway_providers():
    """List all registered provider names."""
    return {"providers": list_providers()}
