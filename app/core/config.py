from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Marvel Genetic Data Processor"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./marvel_genetics.db"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 