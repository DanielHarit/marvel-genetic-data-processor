from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import zipfile
import io

from app.db.session import get_db
from app.crud import character as crud
from app.services.processing import (
    calculate_gc_content,
    find_repeating_patterns,
    determine_power_level_group,
    parse_genetic_file
)

router = APIRouter()

@router.post("/upload")
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
            if any(filename.startswith(ext) for ext in ['.', '..', '__MACOSX']):
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
                    character = crud.create_character(db, {
                        **char_data,
                        'gc_content': calculate_gc_content(char_data['genetic_sequence']),
                        'power_level_group': determine_power_level_group(char_data['power_level'])
                    })
                except Exception as e:
                    print(f"Error creating character {char_data['character_name']} with error: {e}")
                    continue

                try:
                    # Process patterns
                    patterns = find_repeating_patterns(char_data['genetic_sequence'])
                    for pattern, count in patterns:
                        crud.create_pattern(db, character.id, pattern, count)
                except Exception as e:
                    print(f"Error processing patterns for character {char_data['character_name']} with error: {e}")
                    continue

    db.commit()
    return {"message": "Data processed successfully"} 