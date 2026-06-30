"""Standalone FastAPI server for the LLM gateway."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from llm_gateway import gateway_router

logger = logging.getLogger(__name__)

HOST = "127.0.0.1"
PORT = 10916

app = FastAPI(
    title="LLM Gateway",
    description="28 LLM providers through one OpenAI-compatible endpoint",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gateway_router)


@app.get("/health")
async def health():
    providers = __import__("llm_gateway.base", fromlist=["list_providers"]).list_providers()
    return {"status": "ok", "service": "llm-gateway", "providers": len(providers)}


def main():
    import uvicorn

    logging.basicConfig(level=logging.INFO)
    logger.info("Starting LLM Gateway on %s:%s", HOST, PORT)
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


if __name__ == "__main__":
    main()
