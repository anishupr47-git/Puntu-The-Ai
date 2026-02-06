from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas import MemoryCreate, MemoryOut, MemorySearch
from ..models import Memory
from ..services.embeddings import embed_texts
from ..utils import cosine_similarity


router = APIRouter()


@router.post('/', response_model=MemoryOut)
def create_memory(req: MemoryCreate, db: Session = Depends(get_db)):
    embedding = embed_texts([req.text])[0]
    memory = Memory(user_id=req.user_id, text=req.text, embedding=embedding)
    db.add(memory)
    db.commit()
    db.refresh(memory)
    return memory


@router.get('/', response_model=list[MemoryOut])
def list_memories(db: Session = Depends(get_db)):
    return db.query(Memory).order_by(Memory.created_at.desc()).limit(100).all()


@router.post('/search')
def search_memories(req: MemorySearch, db: Session = Depends(get_db)):
    query_vec = embed_texts([req.query])[0]
    memories = db.query(Memory).all()
    scored = [
        {
            'id': mem.id,
            'text': mem.text,
            'score': cosine_similarity(query_vec, mem.embedding)
        }
        for mem in memories
    ]
    scored.sort(key=lambda item: item['score'], reverse=True)
    return scored[:req.limit]
