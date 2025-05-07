from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Marvel Genetic Data Processor"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./marvel_genetics.db"

    # AWS settings
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str
    AWS_SQS_QUEUE_URL: str

    # S3 Upload Settings
    S3_UPLOAD_EXPIRATION: int = 3600  # URL expiration time in seconds
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 