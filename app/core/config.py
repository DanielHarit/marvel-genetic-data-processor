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
    
    # Genetic Analysis Settings
    MIN_PATTERN_LENGTH: int = 2
    TOP_PATTERNS_COUNT: int = 5
    
    # Power Level Thresholds
    POWER_LEVEL_LOW_THRESHOLD: int = 33
    POWER_LEVEL_MEDIUM_THRESHOLD: int = 66
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 