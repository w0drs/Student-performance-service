from pydantic import BaseModel, Field, field_validator
from typing import Optional


class UploadResponse(BaseModel):
    """
    Ответ на загрузку CSV файла
    """
    status: str = Field(..., description="Статус операции (ok/error)")
    records_loaded: int = Field(..., description="Количество загруженных записей")
    students: int = Field(..., description="Количество уникальных студентов")


class StudentTwosResponse(BaseModel):
    """
    Студент с количеством двоек
    """
    full_name: str = Field(..., description="Полное имя студента (Фамилия Имя Отчество)")
    count_twos: int = Field(..., ge=0, description="Количество двоек")


class ErrorResponse(BaseModel):
    """
    Ответ с ошибкой
    """
    detail: str = Field(..., description="Описание ошибки")


class HealthResponse(BaseModel):
    """
    Ответ на проверку здоровья сервиса
    """
    status: str = Field(..., description="Статус сервиса (healthy/unhealthy)")


class RootResponse(BaseModel):
    """
    Корневой ответ с информацией о сервисе
    """
    service: str = Field(..., description="Название сервиса")
    version: str = Field(..., description="Версия сервиса")
    endpoints: dict = Field(..., description="Доступные эндпоинты")


class GradeRequest(BaseModel):
    """
    Запрос на добавление оценки (для документации)
    """
    student_id: int = Field(..., gt=0, description="ID студента")
    group_id: int = Field(..., gt=0, description="ID группы")
    grade_date: str = Field(..., pattern=r"^\d{2}\.\d{2}\.\d{4}$", description="Дата в формате DD.MM.YYYY")
    grade: int = Field(..., ge=2, le=5, description="Оценка от 2 до 5")


class StudentInfo(BaseModel):
    """
    Информация о студенте
    """
    id: int = Field(..., description="ID студента")
    first_name: str = Field(..., min_length=1, description="Имя")
    last_name: str = Field(..., min_length=1, description="Фамилия")
    patronymic: Optional[str] = Field(None, description="Отчество")


class GroupInfo(BaseModel):
    """
    Информация о группе
    """
    id: int = Field(..., description="ID группы")
    group_name: str = Field(..., min_length=1, description="Название группы (например: 101Б)")


class GradeInfo(BaseModel):
    """
    Информация об оценке
    """
    id: int = Field(..., description="ID записи")
    student_id: int = Field(..., description="ID студента")
    group_id: int = Field(..., description="ID группы")
    grade: int = Field(..., ge=2, le=5, description="Оценка")
    grade_date: str = Field(..., description="Дата получения оценки")
    created_at: str = Field(..., description="Дата создания записи")
    updated_at: str = Field(..., description="Дата последнего обновления")