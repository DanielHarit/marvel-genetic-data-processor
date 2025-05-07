# Marvel Genetic Data Processor

A FastAPI-based service for processing genetic data of Marvel characters.

## Features

- Process genetic data from ZIP files containing JSON, text, or base64-encoded files
- Calculate GC-content for genetic sequences
- Find repeating patterns in genetic sequences
- Group characters by power level
- Generate statistics and patterns by character affiliation

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Service

Start the service with:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /upload

Upload a ZIP file containing genetic data files. The ZIP file can contain:

- JSON files (.json)
- Text files (.txt)
- Base64-encoded files (.b64)

Each file should contain the following metadata:

- character_name
- affiliation
- genetic_sequence
- power_level

### GET /stats

Returns statistics for all characters:

- GC-content per character
- Most common repeating patterns
- Distribution of characters by power level

### GET /affiliation/{affiliation}

Returns the same statistics as `/stats` but filtered for a specific affiliation.

## Example Usage

1. Create a ZIP file with genetic data files
2. Upload the ZIP file:

```bash
curl -X POST "http://localhost:8000/upload" -F "file=@data.zip"
```

3. Get statistics:

```bash
curl "http://localhost:8000/stats"
```

4. Get affiliation-specific statistics:

```bash
curl "http://localhost:8000/affiliation/Avengers"
```

## Data Format Examples

### JSON Format

```json
{
  "character_name": "Spider-Man",
  "affiliation": "Avengers",
  "genetic_sequence": "ATCGGCTA",
  "power_level": 75
}
```

### Text Format

```
character_name: Spider-Man
affiliation: Avengers
genetic_sequence: ATCGGCTA
power_level: 75
```

### Base64 Format

Base64-encoded JSON data
