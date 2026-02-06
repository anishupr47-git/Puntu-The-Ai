from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas import ModuleLogCreate, SongOut, MovieOut
from ..models import ModuleLog, Song, Movie


router = APIRouter()


@router.get('/songs', response_model=list[SongOut])
def songs(db: Session = Depends(get_db)):
    return db.query(Song).order_by(Song.id.asc()).all()


@router.get('/movies', response_model=list[MovieOut])
def movies(db: Session = Depends(get_db)):
    return db.query(Movie).order_by(Movie.id.asc()).all()


@router.post('/log')
def log_module(req: ModuleLogCreate, db: Session = Depends(get_db)):
    log = ModuleLog(user_id=req.user_id, module=req.module, input=req.input, output=req.output)
    db.add(log)
    db.commit()
    return {'status': 'ok'}
