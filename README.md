# LLM Gateway

28 LLM providers through one OpenAI-compatible endpoint. Lightport-compatible proxy.

```powershell
uv sync
uv run llm-gateway
```

```python
from openai import OpenAI
client = OpenAI(base_url="http://127.0.0.1:10916/v1", api_key="...")
client.default_headers["x-lightport-provider"] = "anthropic"
```

| Local | Cloud |
|-------|-------|
| Ollama, LM Studio, vLLM | Anthropic, Azure, Bedrock, Cohere, DeepInfra, DeepSeek, Featherless, Fireworks, Gemini, Groq, Hyperbolic, Lepton, Mistral, Modal, Nebius, Novita, OpenAI, OpenRouter, Perplexity, Replicate, SambaNova, SiliconFlow, Together, xAI (Grok), Anyscale |

Also embeddable: `from llm_gateway import gateway_router`
