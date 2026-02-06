import asyncio
import json
import httpx
from typing import AsyncGenerator, Optional
from ..core.config import settings


class OllamaClient:
    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip('/')
        self.model = model or settings.OLLAMA_MODEL

    async def generate(self, prompt: str, system: Optional[str] = None, temperature: float = 0.6) -> str:
        payload = {
            'model': self.model,
            'prompt': prompt,
            'stream': False,
            'options': {'temperature': temperature},
        }
        if system:
            payload['system'] = system

        for attempt in range(3):
            try:
                async with httpx.AsyncClient(timeout=60) as client:
                    response = await client.post(f'{self.base_url}/api/generate', json=payload)
                    response.raise_for_status()
                    data = response.json()
                    return data.get('response', '')
            except httpx.HTTPError:
                if attempt == 2:
                    return 'AI is resting. It will be back soon.'
                await asyncio.sleep(1.5 * (attempt + 1))

        return 'AI is resting. It will be back soon.'

    async def stream(self, prompt: str, system: Optional[str] = None, temperature: float = 0.6) -> AsyncGenerator[str, None]:
        payload = {
            'model': self.model,
            'prompt': prompt,
            'stream': True,
            'options': {'temperature': temperature},
        }
        if system:
            payload['system'] = system

        for attempt in range(3):
            try:
                async with httpx.AsyncClient(timeout=None) as client:
                    async with client.stream('POST', f'{self.base_url}/api/generate', json=payload) as response:
                        response.raise_for_status()
                        async for line in response.aiter_lines():
                            if not line:
                                continue
                            data = json.loads(line)
                            if data.get('done') is True:
                                return
                            chunk = data.get('response')
                            if chunk:
                                yield chunk
                return
            except httpx.HTTPError:
                if attempt == 2:
                    yield 'AI is resting. It will be back soon.'
                    return
                await asyncio.sleep(1.5 * (attempt + 1))
