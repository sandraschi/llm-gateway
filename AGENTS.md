# llm-gateway — Agent Guide

## Overview
Lightport-compatible AI provider gateway — 28 LLM providers through one OpenAI-compatible `/v1/chat/completions` endpoint. Standalone server or embeddable FastAPI router.

## Quick Start
```powershell
uv sync
uv run llm-gateway        # starts on http://127.0.0.1:10916
```

## Usage
```python
from openai import OpenAI
client = OpenAI(base_url="http://127.0.0.1:10916/v1", api_key="...")
client.default_headers["x-lightport-provider"] = "deepseek"
```

## Providers (28)
Local: Ollama, LM Studio, vLLM
Cloud: Anthropic, Anyscale, Azure, Bedrock, Cohere, DeepInfra, DeepSeek, Featherless, Fireworks, Gemini, Groq, Hyperbolic, Lepton, Mistral, Modal, Nebius, Novita, OpenAI, OpenRouter, Perplexity, Replicate, SambaNova, SiliconFlow, Together, xAI (Grok)

## Embedding
```python
from llm_gateway import gateway_router
app.include_router(gateway_router)
```
