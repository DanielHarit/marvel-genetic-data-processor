import boto3
from botocore.config import Config
from app.core.config import settings

class S3Service:
    def __init__(self):
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
            return url
        except Exception as e:
            print(f"Error generating presigned URL: {e}")
            return None

    def get_object(self, object_key: str) -> bytes:
        """
        Retrieve an object from S3.
        
        Args:
            object_key: The key (path) of the object in S3
            
        Returns:
            bytes: The object's content
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return response['Body'].read()
        except Exception as e:
            print(f"Error retrieving object from S3: {e}")
            return None

# Create a singleton instance
s3_service = S3Service() 