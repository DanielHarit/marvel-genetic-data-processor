# Marvel Genetic Data Processor

A FastAPI-based service for processing and analyzing genetic data of Marvel characters. The service includes secure file uploads via AWS S3, asynchronous processing using AWS SQS, and JWT authentication.

## Features

- **Secure File Upload**: Files are uploaded directly to AWS S3 using pre-signed URLs
- **Asynchronous Processing**: File processing is handled asynchronously using AWS SQS
- **Authentication**: JWT-based authentication system
- **Data Analysis**: Genetic sequence analysis with power level calculations
- **Visualizations**: Automatic generation of data visualizations
- **Database**: SQLite database with connection pooling for concurrent operations
- **API Documentation**: Interactive API documentation via Swagger UI

## Prerequisites

- Python 3.8+
- AWS Account with S3 and SQS services
- SQLite (included with Python)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd marvel-genetic-data-processor
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following variables:

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
AWS_S3_BUCKET=your_bucket_name
AWS_SQS_QUEUE_URL=your_queue_url

# JWT Settings
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# S3 Upload Settings
S3_UPLOAD_EXPIRATION=3600

# Genetic Analysis Settings
MIN_PATTERN_LENGTH=2
TOP_PATTERNS_COUNT=5
POWER_LEVEL_LOW_THRESHOLD=33
POWER_LEVEL_MEDIUM_THRESHOLD=66
```

## Database Setup

1. Initialize the database:

```bash
python -c "from app.db.base_class import Base; from app.db.session import engine; Base.metadata.create_all(bind=engine)"
```

2. Create test users:

```bash
python scripts/create_test_users.py
```

This will create three test users:

- Admin: admin@example.com / admin123
- Regular User: user@example.com / user123
- Inactive User: inactive@example.com / inactive123

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

- `POST /api/v1/login`: Login and get access token
- `GET /api/v1/me`: Get current user information

### File Upload

- `POST /api/v1/generate-upload-url`: Get a pre-signed URL for file upload
- Files should be uploaded directly to the provided S3 URL

### Statistics

- `GET /api/v1/stats`: Get overall statistics with visualizations
- `GET /api/v1/affiliation/{affiliation}`: Get statistics for a specific affiliation
- `GET /api/v1/character/{name}`: Get statistics for a specific character

## Visualizations

The `/stats` endpoint returns URLs to three visualizations:

1. Power Level Distribution (histogram)
2. GC Content Distribution (histogram)
3. Affiliation Distribution (pie chart)

Visualizations are automatically generated and served from the `/static/graphs` directory.

## Architecture

### Components

- **FastAPI**: Web framework
- **SQLAlchemy**: Database ORM
- **AWS S3**: File storage
- **AWS SQS**: Message queue for asynchronous processing
- **JWT**: Authentication
- **Matplotlib/Seaborn**: Data visualization

### Flow

1. User requests a pre-signed URL for file upload
2. File is uploaded directly to S3
3. S3 event triggers SQS message
4. Background processor:
   - Retrieves file from S3
   - Processes genetic data
   - Stores results in database
   - Deletes processed file from S3
5. User can access statistics and visualizations via API

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
|   |── static/          # Static assets
|   |── utils/           # Utilities
|── scripts/             # useful scripts for developers
├── requirements.txt
└── README.md
```

## Example Upload

1. Create a ZIP file with genetic data files

2. Get JWT

```bash
curl -X POST "http://localhost:8000/api/v1/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=user123"
```

3. Upload the ZIP file:

```bash
curl -X POST -H "Authorization: Bearer <YOUR_JWT>" "http://localhost:8000/api/v1/upload" -F "file=@data.zip"
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
