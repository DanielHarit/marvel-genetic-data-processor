# Marvel Genetic Data Processor

A FastAPI-based service for processing genetic data of Marvel characters.

## Features

- Process genetic data from ZIP files containing JSON, text, or base64-encoded files
- Calculate GC-content for genetic sequences
- Find repeating patterns in genetic sequences
- Group characters by power level
- Generate statistics and patterns by character affiliation

## Project Structure

```
my_service/
├── app/
│   ├── api/               # API endpoints
│   ├── core/             # Core functionality
│   ├── models/           # SQLAlchemy models
│   ├── crud/            # Database operations
│   ├── schemas/         # Pydantic models
│   ├── services/        # Business logic
│   ├── db/             # Database setup
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository
2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Service

Start the service with:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /api/v1/upload

Upload a ZIP file containing genetic data files. The ZIP file can contain:

- JSON files (.json)
- Text files (.txt)
- Base64-encoded files (.b64)

Each file should contain the following metadata for one or more characters:

- character_name
- affiliation
- genetic_sequence
- power_level

### GET /api/v1/stats

Returns statistics for all characters:

- GC-content per character
- Most common repeating patterns across all sequences
- Distribution of characters by power level

### GET /api/v1/affiliation/{affiliation}

Returns the same statistics as `/stats` but filtered for a specific affiliation.

## Example Usage

1. Create a ZIP file with genetic data files
2. Upload the ZIP file:

```bash
curl -X POST "http://localhost:8000/api/v1/upload" -F "file=@data.zip"
```

3. Get statistics:

```bash
curl "http://localhost:8000/api/v1/stats"
```

4. Get affiliation-specific statistics:

```bash
curl "http://localhost:8000/api/v1/affiliation/Avengers"
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
