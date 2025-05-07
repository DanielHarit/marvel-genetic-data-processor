from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import threading
import logging

from app.core.config import settings
from app.api.v1.endpoints import upload, stats
from app.db.base_class import Base
from app.db.session import engine, SessionLocal
from app.services.sqs_service import sqs_service
from app.utils.logger import logger

# Create database tables
Base.metadata.create_all(bind=engine)

# Set up SQS processing
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()

    # Start SQS processor in a background thread
    thread = threading.Thread(target=sqs_service.process_messages, args=(db,),daemon=True)
    thread.start()
    logger.info("SQS background processor started.")

    # Yield control to FastAPI app
    yield

    db.close()
    logger.info("SQS background processor stopped.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix=settings.API_V1_STR)
app.include_router(stats.router, prefix=settings.API_V1_STR) 

# Get uvicorn access and error loggers
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_error_logger = logging.getLogger("uvicorn.error")

uvicorn_access_logger.addHandler(logger.handlers[1])
uvicorn_error_logger.addHandler(logger.handlers[1])