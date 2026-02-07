from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .routers import llm, agent, memory, entries, modules, football, vision


app = FastAPI(title='PUNTU API', version='0.1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins(),
    allow_origin_regex=settings.cors_origin_regex(),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/api/health')
def health():
    return {'status': 'ok'}


app.include_router(llm.router, prefix='/api/llm', tags=['llm'])
app.include_router(agent.router, prefix='/api/agent', tags=['agent'])
app.include_router(memory.router, prefix='/api/memories', tags=['memories'])
app.include_router(entries.router, prefix='/api/entries', tags=['entries'])
app.include_router(modules.router, prefix='/api/modules', tags=['modules'])
app.include_router(football.router, prefix='/api/football', tags=['football'])
app.include_router(vision.router, prefix='/api/vision', tags=['vision'])
