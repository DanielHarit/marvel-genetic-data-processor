from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.db.session import get_db
from app.services.processing import process_zip_file
from app.services.s3_service import s3_service
from app.utils.logger import logger
from app.core.security import get_current_user

router = APIRouter()

@router.post("/generate-upload-url")
async def generate_upload_url(current_user: str = Depends(get_current_user)):
    """
    Generate a presigned URL for uploading a file to S3.
    The URL will be valid for 1 hour.
    """
    logger.info("Generating upload URL")
    try:
        # Generate a unique object key with proper path structure
        object_key = f"uploads/{datetime.utcnow().strftime('%Y/%m/%d')}/{uuid.uuid4()}.zip"
        logger.debug(f"Generated object key: {object_key}")
        
        # Generate the presigned URL with content type
        presigned_url = s3_service.generate_presigned_url(
            object_key,
            content_type="application/zip"
        )
        if not presigned_url:
            logger.error("Failed to generate presigned URL")
            raise HTTPException(status_code=500, detail="Failed to generate upload URL")
        
        logger.info("Successfully generated upload URL")
        return {
            "upload_url": presigned_url,
            "object_key": object_key,
            "expires_in": "1 hour"
        }
    except Exception as e:
        logger.exception("Unexpected error generating upload URL")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.post("/upload")
async def upload_genetic_data(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    logger.info(f"Processing upload request for file: {file.filename}")
    
    if not file.filename.endswith('.zip'):
        logger.warning(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Only ZIP files are accepted")

    try:
        # Read the ZIP file
        contents = await file.read()
        logger.debug(f"Read {len(contents)} bytes from file")
        
        # Process the ZIP file
        process_zip_file(contents, db)
        
        logger.info("Successfully processed upload")
        return {"message": "Data processed successfully"}
    except Exception as e:
        logger.exception("Error processing upload")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the file") 