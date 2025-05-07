from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.db.session import get_db
from app.services.processing import process_zip_file
from app.services.s3_service import s3_service

router = APIRouter()

@router.post("/generate-upload-url")
async def generate_upload_url():
    """
    Generate a presigned URL for uploading a file to S3.
    The URL will be valid for 1 hour.
    """
    # Generate a unique object key with proper path structure
    object_key = f"uploads/{datetime.utcnow().strftime('%Y/%m/%d')}/{uuid.uuid4()}.zip"
    
    # Generate the presigned URL with content type
    presigned_url = s3_service.generate_presigned_url(
        object_key,
        content_type="application/zip"
    )
    if not presigned_url:
        raise HTTPException(status_code=500, detail="Failed to generate upload URL")
    
    return {
        "upload_url": presigned_url,
        "object_key": object_key,
        "expires_in": "1 hour"
    }

@router.post("/upload")
async def upload_genetic_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only ZIP files are accepted")

    # Read the ZIP file
    contents = await file.read()
    
    # Process the ZIP file
    process_zip_file(contents, db)
    
    return {"message": "Data processed successfully"} 