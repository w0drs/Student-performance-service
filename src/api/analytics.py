from fastapi import APIRouter, HTTPException
from src.schemas import StudentTwosResponse, ErrorResponse
from src.service.analytics import (
    get_students_more_than_3_twos,
    get_students_less_than_5_twos
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/students/more-than-3-twos",
    response_model=list[StudentTwosResponse],
    responses={500: {"model": ErrorResponse}}
)
def get_more_than_3_twos():
    """
    Возвращает студентов, у которых оценка 2 встречается больше 3 раз

    Returns:
    [
        { "full_name": "Иванов Иван Иванович", "count_twos": 4 },
        { "full_name": "Петров Петр Петрович", "count_twos": 5 }
    ]
    """
    try:
        result = get_students_more_than_3_twos()
        logger.info(f"Found {len(result)} students with >3 twos")
        return result

    except Exception as e:
        logger.error(f"Error in more-than-3-twos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/students/less-than-5-twos",
    response_model=list[StudentTwosResponse],
    responses={500: {"model": ErrorResponse}}
)
def get_less_than_5_twos():
    """
    Возвращает студентов, у которых оценка 2 встречается меньше 5 раз

    Returns:
    [
        { "full_name": "Сидоров Сидор Сидорович", "count_twos": 2 },
        { "full_name": "Кузнецов Алексей", "count_twos": 3 }
    ]
    """
    try:
        result = get_students_less_than_5_twos()
        logger.info(f"Found {len(result)} students with <5 twos")
        return result

    except Exception as e:
        logger.error(f"Error in less-than-5-twos: {e}")
        raise HTTPException(status_code=500, detail=str(e))
