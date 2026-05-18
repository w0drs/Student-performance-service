import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from src.config import config
from logging import getLogger

logger = getLogger(__name__)


class Database:
    """
    Класс подключения к бд
    """
    def __init__(self) -> None:
        self.pool = None

    def connect(self) -> None:
        try:
            self.pool = psycopg2.pool.SimpleConnectionPool(
                1, 10,
                host=config.POSTGRES_HOST,
                port=config.POSTGRES_PORT,
                database=config.POSTGRES_DB,
                user=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD
            )
            logger.info("Database connected successfully")
        except Exception as e:
            logger.error(f"Database connection error: {e}")

    @contextmanager
    def get_connection(self):

        if self.pool is None:
            self.connect()

        #if not self.pool:
        #    raise Exception("Database not connected. Call connect() first.")

        conn = self.pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.pool.putconn(conn)


db = Database()
