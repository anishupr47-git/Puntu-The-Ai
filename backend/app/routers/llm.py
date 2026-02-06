from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ..schemas import LLMRequest, LLMWarmRequest
from ..services.ollama import OllamaClient


router = APIRouter()
ollama = OllamaClient()


@router.post('/generate')
async def generate(req: LLMRequest):
    text = await ollama.generate(prompt=req.prompt, system=req.system, temperature=req.temperature)
    return {'response': text}


@router.post('/stream')
async def stream(req: LLMRequest):
    async def generator():
        async for chunk in ollama.stream(prompt=req.prompt, system=req.system, temperature=req.temperature):
            yield chunk

    return StreamingResponse(generator(), media_type='text/plain')


@router.post('/warm')
async def warm(req: LLMWarmRequest):
    text = await ollama.generate(prompt=req.prompt, system='Warm the model.', temperature=0.2)
    return {'status': 'warmed', 'sample': text[:120]}
