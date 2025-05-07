import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.character import Character, Pattern

def delete_patterns(db: Session) -> None:
    patterns = db.query(Pattern).all()
    for pattern in patterns:
        db.delete(pattern)
    db.commit()

    print("Patterns deleted successfully!")

def delete_characters(db: Session) -> None:
    characters = db.query(Character).all()
    for character in characters:
        db.delete(character)
    db.commit()

    print("Characters deleted successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        delete_patterns(db)
        delete_characters(db)
        characters = db.query(Character).all()
        for character in characters:
            print(character.name)
            print(character.affiliation)
            print(character.power_level)
            print(character.genetic_sequence)
            print("--------------------------------")
    finally:
        db.close() 