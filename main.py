from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import zipfile
import io
import os
from typing import List, Dict

from models import Base, Character, Pattern
from schemas import StatsResponse, AffiliationStatsResponse
from utils import (
    calculate_gc_content,
    find_repeating_patterns,
    determine_power_level_group,
    parse_genetic_file,
    is_base64_like
)

app = FastAPI(title="Marvel Genetic Data Processor")

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./marvel_genetics.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
async def upload_genetic_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only ZIP files are accepted")

    # Read the ZIP file
    contents = await file.read()
    with zipfile.ZipFile(io.BytesIO(contents)) as zip_ref:
        for filename in zip_ref.namelist():
            # Skip non-data files
            if not any(filename.endswith(ext) for ext in ['.json', '.txt', '.b64']):
                continue

            # Read file content
            content = zip_ref.read(filename).decode('utf-8')
            
            # Process the file content
            characters_data = parse_genetic_file(content, filename)

            for char_data in characters_data:
                # Validate required fields
                required_fields = ['character_name', 'affiliation', 'genetic_sequence', 'power_level']
                if not all(field in char_data for field in required_fields):
                    continue

                try:
                    # Create character record
                    character = Character(
                        character_name=char_data['character_name'],
                        affiliation=char_data['affiliation'],
                        genetic_sequence=char_data['genetic_sequence'],
                        power_level=char_data['power_level'],
                        gc_content=calculate_gc_content(char_data['genetic_sequence']),
                        power_level_group=determine_power_level_group(char_data['power_level'])
                    )
                    db.add(character)
                    db.flush()  # Get the character ID
                except Exception as e:
                    print(f"Error creating character {char_data['character_name']} with error: {e}")
                    continue

                try:
                    # Process patterns
                    patterns = find_repeating_patterns(char_data['genetic_sequence'])
                    for pattern, count in patterns:
                        pattern_record = Pattern(
                            character_id=character.id,
                            pattern=pattern,
                            count=count
                        )
                        db.add(pattern_record)
                except Exception as e:
                    print(f"Error processing patterns for character {char_data['character_name']} with error: {e}")
                    continue

    db.commit()
    return {"message": "Data processed successfully"}

@app.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    # Get GC content by character
    characters = db.query(Character).all()
    gc_content_by_character = {
        char.character_name: char.gc_content for char in characters
    }

    # Get common patterns
    patterns = db.query(Pattern.pattern, func.sum(Pattern.count).label('total_count'))\
        .group_by(Pattern.pattern)\
        .order_by(func.sum(Pattern.count).desc())\
        .limit(10)\
        .all()
    common_patterns = [{p[0]: p[1]} for p in patterns]

    # Get power level distribution
    power_level_distribution = {
        "low": db.query(Character).filter(Character.power_level_group == "low").count(),
        "medium": db.query(Character).filter(Character.power_level_group == "medium").count(),
        "high": db.query(Character).filter(Character.power_level_group == "high").count()
    }

    return StatsResponse(
        gc_content_by_character=gc_content_by_character,
        common_patterns=common_patterns,
        power_level_distribution=power_level_distribution
    )

@app.get("/affiliation/{affiliation}", response_model=AffiliationStatsResponse)
def get_affiliation_stats(affiliation: str, db: Session = Depends(get_db)):
    # Get GC content by character for the affiliation
    characters = db.query(Character).filter(Character.affiliation == affiliation).all()
    gc_content_by_character = {
        char.character_name: char.gc_content for char in characters
    }

    # Get common patterns for the affiliation
    patterns = db.query(Pattern.pattern, func.sum(Pattern.count).label('total_count'))\
        .join(Character)\
        .filter(Character.affiliation == affiliation)\
        .group_by(Pattern.pattern)\
        .order_by(func.sum(Pattern.count).desc())\
        .limit(10)\
        .all()
    common_patterns = [{p[0]: p[1]} for p in patterns]

    # Get power level distribution for the affiliation
    power_level_distribution = {
        "low": db.query(Character).filter(
            Character.affiliation == affiliation,
            Character.power_level_group == "low"
        ).count(),
        "medium": db.query(Character).filter(
            Character.affiliation == affiliation,
            Character.power_level_group == "medium"
        ).count(),
        "high": db.query(Character).filter(
            Character.affiliation == affiliation,
            Character.power_level_group == "high"
        ).count()
    }

    return AffiliationStatsResponse(
        gc_content_by_character=gc_content_by_character,
        common_patterns=common_patterns,
        power_level_distribution=power_level_distribution
    ) 