from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud import character as crud
from app.schemas.character import StatsResponse, AffiliationStatsResponse, CharacterStatsResponse
from app.core.security import get_current_user

router = APIRouter()

@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return crud.get_characters_stats(db)

@router.get("/affiliation/{affiliation}", response_model=AffiliationStatsResponse)
def get_affiliation_stats(affiliation: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return crud.get_affiliation_stats(db, affiliation) 

@router.get("/character/{name}", response_model=CharacterStatsResponse)
def get_character_stats(name: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    character = crud.get_character_stats(db, name) 
    if not character:
        raise HTTPException(status_code=404, detail=f"Character {name} not found")
    return character