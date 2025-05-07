import boto3
import json
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.config import settings
from app.services.processing import process_zip_file
from app.services.s3_service import s3_service
from app.db.session import SessionLocal
from app.utils.logger import logger

class SQSService:
    def __init__(self):
        self.sqs_client = boto3.client(
            'sqs',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.queue_url = settings.AWS_SQS_QUEUE_URL

    def process_messages(self):
        """
        Poll the SQS queue and process messages.
        Creates a new database session for each message to avoid locks.
        """
        while True:
            try:
                # Receive messages from the queue
                response = self.sqs_client.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=1,
                    WaitTimeSeconds=20
                )

                messages = response.get('Messages', [])
                for message in messages:
                    # Create a new database session for each message
                    db = SessionLocal()
                    try:
                        # Parse the message body
                        body = json.loads(message['Body'])
                        
                        # Get the S3 object key from the message
                        s3_key = body.get('Records', [{}])[0].get('s3', {}).get('object', {}).get('key')
                        if not s3_key:
                            continue

                        # Get the file from S3
                        file_content = s3_service.get_object(s3_key)
                        if not file_content:
                            continue

                        # Process the ZIP file
                        process_zip_file(file_content, db)

                        # Delete the processed message from SQS
                        self.sqs_client.delete_message(
                            QueueUrl=self.queue_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )

                        # Delete the processed file from S3
                        if s3_service.delete_object(s3_key):
                            logger.info(f"Successfully processed and cleaned up file: {s3_key}")
                        else:
                            logger.warning(f"File processed but failed to delete from S3: {s3_key}")

                    except Exception as e:
                        logger.exception(f"Error processing message: {e}")
                    finally:
                        # Always close the database session
                        db.close()

            except Exception as e:
                logger.exception(f"Error polling queue: {e}")
                continue

sqs_service = SQSService() 