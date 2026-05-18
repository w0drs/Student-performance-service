import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import db
from src.config import config
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from logging import getLogger
import logging

logger = getLogger(__name__)


def create_test_database():
    """Создает тестовую БД если она не существует"""
    conn = psycopg2.connect(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        database="postgres",
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'test_db'")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute("CREATE DATABASE test_db")
        logging.debug("Тестовая БД 'test_db' создана")
    else:
        logging.debug("Тестовая БД 'test_db' уже существует")

    cursor.close()
    conn.close()


def init_test_db_tables():
    """Создает таблицы в тестовой БД если их нет"""
    conn = psycopg2.connect(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        database="test_db",
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables 
            WHERE table_name = 'students'
        )
    """)
    tables_exist = cursor.fetchone()[0]

    if not tables_exist:
        with open('src/migrations/20260516_134900_create_table_students.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
            cursor.execute(sql)
        logging.debug("Таблицы в test_db созданы")
    else:
        logging.debug("Таблицы в test_db уже существуют")

    cursor.close()
    conn.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Автоматически создает тестовую БД и таблицы перед запуском тестов"""
    create_test_database()
    init_test_db_tables()
    yield


@pytest.fixture(scope="session")
def test_client():
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