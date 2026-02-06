import asyncio
import base64
import httpx
from typing import Optional
from ..core.config import settings


async def analyze_image(image_bytes: bytes, prompt: Optional[str] = None) -> str:
    prompt = prompt or 'Describe and summarize this image.'
    payload = {
        'model': settings.OLLAMA_VISION_MODEL,
        'prompt': prompt,
        'stream': False,
        'images': [base64.b64encode(image_bytes).decode('utf-8')],
    }

    for attempt in range(3):
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/generate", json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get('response', '')
        except httpx.HTTPError:
            if attempt == 2:
                raise
            await asyncio.sleep(1.5 * (attempt + 1))

    return ''
