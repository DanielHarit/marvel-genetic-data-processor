from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud import character as crud
from app.schemas.character import StatsResponse, AffiliationStatsResponse

router = APIRouter()

@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    return crud.get_character_stats(db)

@router.get("/affiliation/{affiliation}", response_model=AffiliationStatsResponse)
def get_affiliation_stats(affiliation: str, db: Session = Depends(get_db)):
    return crud.get_affiliation_stats(db, affiliation) 