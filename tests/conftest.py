import pytest
from src.database import db
from src.config import config
import psycopg2
import logging

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Создает таблицы в тестовой БД"""

    logger.info("Настройка тестовой БД...")
    logger.debug(f"Хост: {config.POSTGRES_HOST}")
    logger.debug(f"Порт: {config.POSTGRES_PORT}")
    logger.debug(f"БД: test_db")
    logger.debug(f"Пользователь: {config.POSTGRES_USER}")

    try:
        conn = psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            database="test_db",
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD
        )
        conn.close()
        logger.info("Подключение к test_db успешно")
    except Exception as e:
        logger.error(f"Не могу подключиться к test_db: {e}")
        logger.error("Создайте БД вручную: CREATE DATABASE test_db;")
        raise

    original_db_name = config.POSTGRES_DB

    config.POSTGRES_DB = "test_db"
    logger.info(f"Переключение на тестовую БД: {config.POSTGRES_DB}")

    if db.pool:
        db.pool.closeall()
        db.pool = None
    db.connect()

    try:
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                with open('src/migrations/20260516_134900_create_table_students.sql', 'r', encoding='utf-8') as f:
                    sql = f.read()
                    cur.execute(sql)
        logger.info("Таблицы успешно созданы в test_db")
    except Exception as e:
        logger.error(f"Ошибка создания таблиц: {e}")
        raise

    yield

    config.POSTGRES_DB = original_db_name
    logger.info(f"Возврат к рабочей БД: {config.POSTGRES_DB}")

    if db.pool:
        db.pool.closeall()
        db.pool = None
    db.connect()
    logger.info("Соединение с рабочей БД восстановлено")


@pytest.fixture
def clean_db():
    """Очищает таблицы перед каждым тестом"""
    logger.debug("Очистка таблиц перед тестом")
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE students, groups, grades RESTART IDENTITY CASCADE")
    yield
    logger.debug("Очистка таблиц после теста")
