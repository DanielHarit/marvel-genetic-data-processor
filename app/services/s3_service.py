import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from app.core.config import settings
from app.utils.logger import logger

class S3Service:
    def __init__(self):
        logger.info("Initializing S3 service")
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION,
                config=Config(
                    signature_version='s3v4',
                    s3={'addressing_style': 'path'}
                )
            )
            self.bucket_name = settings.AWS_S3_BUCKET
            logger.info(f"S3 service initialized with bucket: {self.bucket_name}")
        except Exception as e:
            logger.exception("Failed to initialize S3 service")
            raise

    def generate_presigned_url(self, object_key: str, content_type: str = None, expiration: int = 3600) -> str:
        """
        Generate a presigned URL for uploading a file to S3.
        
        Args:
            object_key: The key (path) where the file will be stored in S3
            content_type: The content type of the file (e.g., 'application/zip')
            expiration: URL expiration time in seconds (default: 1 hour)
            
        Returns:
            str: The presigned URL for uploading
        """
        logger.info(f"Generating presigned URL for object: {object_key}")
        try:
            params = {
                'Bucket': self.bucket_name,
                'Key': object_key,
            }
            
            if content_type:
                params['ContentType'] = content_type

            url = self.s3_client.generate_presigned_url(
                'put_object',
                Params=params,
                ExpiresIn=expiration
            )
            logger.info(f"Successfully generated presigned URL for {object_key}")
            return url
        except ClientError as e:
            logger.error(f"AWS ClientError generating presigned URL: {e}")
            return None
        except Exception as e:
            logger.exception(f"Unexpected error generating presigned URL: {e}")
            return None

    def get_object(self, object_key: str) -> bytes:
        """
        Retrieve an object from S3.
        
        Args:
            object_key: The key (path) of the object in S3
            
        Returns:
            bytes: The object's content
        """
        logger.info(f"Retrieving object from S3: {object_key}")
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            content = response['Body'].read()
            logger.info(f"Successfully retrieved object: {object_key}")
            return content
        except ClientError as e:
            logger.error(f"AWS ClientError retrieving object: {e}")
            return None
        except Exception as e:
            logger.exception(f"Unexpected error retrieving object: {e}")
            return None

# Create a singleton instance
s3_service = S3Service() 