from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from ..services.vision import analyze_image


router = APIRouter()


@router.post('/analyze')
async def analyze(file: UploadFile = File(...), prompt: str = Form('')):
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail='Only image uploads are supported.')

    image_bytes = await file.read()
    if len(image_bytes) > 6 * 1024 * 1024:
        raise HTTPException(status_code=400, detail='Image too large. Max 6MB.')

    result = await analyze_image(image_bytes, prompt.strip() or None)
    return {'summary': result}
