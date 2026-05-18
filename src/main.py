from fastapi import FastAPI
from src.api import upload, analytics
from src.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Student performance Service",
    description="Сервис для загрузки и анализа успеваемости студентов",
    version="1.0.0"
)

app.include_router(upload.router, tags=["Upload"])
app.include_router(analytics.router, tags=["Analytics"])


@app.get("/")
def root():
    """Корневой эндпоинт"""
    return {
        "service": "Student performance service",
        "version": "1.0.0",
        "endpoints": {
            "upload": "POST /upload-grades",
            "more_than_3_twos": "GET /students/more-than-3-twos",
            "less_than_5_twos": "GET /students/less-than-5-twos"
        }
    }


@app.get("/health")
def health():
    """Проверка здоровья сервиса"""
    return {"status": "healthy"}
