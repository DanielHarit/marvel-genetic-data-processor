from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.character import Character, Pattern
from app.schemas.character import CharacterCreate

def create_character(db: Session, character_data: dict):
    character = Character(
        character_name=character_data['character_name'],
        affiliation=character_data['affiliation'],
        genetic_sequence=character_data['genetic_sequence'],
        power_level=character_data['power_level'],
        gc_content=character_data.get('gc_content', 0),
        power_level_group=character_data.get('power_level_group', 'low')
    )
    db.add(character)
    db.flush()
    return character

def create_pattern(db: Session, character_id: int, pattern: str, count: int):
    pattern_record = Pattern(
        character_id=character_id,
        pattern=pattern,
        count=count
    )
    db.add(pattern_record)
    return pattern_record

def get_character_stats(db: Session):
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

    return {
        "gc_content_by_character": gc_content_by_character,
        "common_patterns": common_patterns,
        "power_level_distribution": power_level_distribution
    }

def get_affiliation_stats(db: Session, affiliation: str):
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

    return {
        "gc_content_by_character": gc_content_by_character,
        "common_patterns": common_patterns,
        "power_level_distribution": power_level_distribution
    } 