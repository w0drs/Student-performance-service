import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import db
from src.config import config


@pytest.fixture(scope="session")
def test_client_and_db():
    """Создает тестовую бд и тестовый клиент FastAPI"""
    original_db_name = config.POSTGRES_DB

    config.POSTGRES_DB = "test_db"

    if db.pool:
        db.pool.closeall()
    db.connect()

    with TestClient(app) as client:
        yield client

    config.POSTGRES_DB = original_db_name
    if db.pool:
        db.pool.closeall()
    db.connect()


@pytest.fixture
def clean_db():
    """Очищает таблицы перед каждым тестом"""
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE students, groups, grades RESTART IDENTITY CASCADE")
    yield
