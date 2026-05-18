from fastapi import APIRouter, UploadFile, File, HTTPException
from src.service.upload_file import process_upload
from src.schemas import UploadResponse, ErrorResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/upload-grades",
    response_model=UploadResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def upload_grades(file: UploadFile = File(...)):
    """
    Загрузить CSV файл с оценками студентов

    Args:
        file: CSV файл с колонками: Дата, Номер группы, ФИО, Оценка
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )

    try:
        content = await file.read()

        result = process_upload(content)

        logger.info(f"Upload successful: {result['records_loaded']} records, {result['students']} students")

        return result

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")