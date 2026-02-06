from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas import EntryCreate, EntryOut
from ..models import Entry


router = APIRouter()


@router.post('/', response_model=EntryOut)
def create_entry(req: EntryCreate, db: Session = Depends(get_db)):
    entry = Entry(user_id=req.user_id, content=req.content)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get('/', response_model=list[EntryOut])
def list_entries(db: Session = Depends(get_db)):
    return db.query(Entry).order_by(Entry.created_at.desc()).limit(100).all()
