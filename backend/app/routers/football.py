from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import FootballRequest
from ..services.football import predict_match, list_clubs, list_national_teams
from ..core.database import get_db


router = APIRouter()


@router.get('/teams')
def teams(db: Session = Depends(get_db)):
    return {
        'clubs': list_clubs(db),
        'national_teams': list_national_teams(db),
    }


@router.post('/predict')
def predict(req: FootballRequest, db: Session = Depends(get_db)):
    return predict_match(db, req.home_team, req.away_team)
