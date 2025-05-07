import re
from typing import List, Dict, Tuple, Any
import json
import base64
import zipfile
import io
from sqlalchemy.orm import Session
from app.crud import character as crud


def calculate_gc_content(sequence: str) -> float:
    """Calculate GC content of a genetic sequence."""
    gc_count = sequence.upper().count('G') + sequence.upper().count('C')
    return (gc_count / len(sequence)) * 100 if sequence else 0

def find_repeating_patterns(sequence: str, min_length: int = 2) -> List[Tuple[str, int]]:
    """Find all repeating patterns in a sequence, incrementally increasing pattern length."""
    patterns = []
    length = min_length
    found = True

    while found and length <= len(sequence) // 2:
        found = False
        seen = set()
        counts = {}
        
        for i in range(len(sequence) - length + 1):
            pattern = sequence[i:i + length]
            if pattern in seen:
                continue
            seen.add(pattern)
            count = sequence.count(pattern)
            if count > 1:
                found = True
                patterns.append((pattern, count))
        
        length += 1

    return patterns

def determine_power_level_group(power_level: int) -> str:
    """Determine power level group based on thresholds."""
    if power_level < 33:
        return "low"
    elif power_level < 66:
        return "medium"
    else:
        return "high"

def decode_base64_custom(encoded_data: str) -> str:
    """Custom decoder for base64-like encoded data."""
    reversed_string = encoded_data[::-1]  # Reverse the string
    base64_bytes = reversed_string.encode('utf-8')
    decoded_bytes = base64.b64decode(base64_bytes)
    return decoded_bytes.decode('utf-8')

def is_base64_like(content: str) -> bool:
    """Check if the content appears to be base64-like encoded."""
    # Check if the content contains only base64-like characters
    base64_pattern = re.compile(r'^[A-Za-z0-9+/=]+$')
    # Check if the content is not a regular text file (which would have key-value pairs)
    has_key_value = any(':' in line for line in content.split('\n'))
    
    # If it has key-value pairs, it's not base64
    if has_key_value:
        return False
    
    # Check if the content matches base64 pattern
    return all(base64_pattern.match(line.strip()) for line in content.split('\n') if line.strip())

def parse_genetic_file(content: str, filename: str = None) -> List[Dict]:
    """Parse genetic data from different file formats."""
    # Detect file format
    if not filename.endswith('.json'):
        if is_base64_like(content):
            file_format = "base64"
        else:
            file_format = "text"
    else:
        file_format = "json"

    if file_format == "json":
        return json.loads(content)
    elif file_format == "text":
        # Parse key-value pairs from text file
        characters_data = []
        current_character = {}
        
        # Split by empty lines for regular text files
        for block in content.split('\n\n'):
            if not block.strip():
                continue
                
            for line in block.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    current_character[key.strip()] = value.strip()
            
            if current_character:
                characters_data.append(current_character)
                current_character = {}
                
        return characters_data
    elif file_format == "base64":
        # Process each line as a separate character
        characters_data = []
        for line in content.split('\n'):
            if not line.strip():
                continue
                
            # Decode the base64-like data
            decoded_content = decode_base64_custom(line.strip())
            try:
                # Try to parse as JSON
                character_data = json.loads(decoded_content)
                characters_data.append(character_data)
            except json.JSONDecodeError:
                # If not JSON, try to parse as key-value pairs
                character_data = {}
                for kv_line in decoded_content.split('\n'):
                    if ':' in kv_line:
                        key, value = kv_line.split(':', 1)
                        character_data[key.strip()] = value.strip()
                if character_data:
                    characters_data.append(character_data)
        
        return characters_data
    else:
        raise ValueError(f"Unsupported file format: {file_format}")

def process_zip_file(zip_content: bytes, db: Session) -> None:
    """
    Process a ZIP file containing genetic data files.
    
    Args:
        zip_content: The ZIP file content as bytes
        db: SQLAlchemy database session
    """
    with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_ref:
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