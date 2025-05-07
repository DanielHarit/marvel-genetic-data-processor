from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud import character as crud
from app.schemas.character import StatsResponse, AffiliationStatsResponse, CharacterStatsResponse
from app.core.security import get_current_user
from app.services.visualization import visualization_service

router = APIRouter()

@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Get all characters for visualization
    characters = crud.get_characters(db)
    
    # Generate visualizations
    visualizations = visualization_service.get_visualizations(characters)
    
    # Get stats
    stats = crud.get_characters_stats(db)
    
    # Add visualizations to the response
    stats["visualizations"] = visualizations
    
    return stats

@router.get("/affiliation/{affiliation}", response_model=AffiliationStatsResponse)
def get_affiliation_stats(affiliation: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    characters = crud.get_characters_by_affiliation(db, affiliation)
    visualizations = visualization_service.get_visualizations(characters)
    stats = crud.get_affiliation_stats(db, affiliation)
    stats["visualizations"] = visualizations
    return stats

@router.get("/character/{name}", response_model=CharacterStatsResponse)
def get_character_stats(name: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    character = crud.get_character_stats(db, name) 
    if not character:
        raise HTTPException(status_code=404, detail=f"Character {name} not found")
    return character