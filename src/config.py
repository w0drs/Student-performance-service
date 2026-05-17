import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Конфигурация приложения: загружает настройки из переменных окружения или использует значения по умолчанию
    """
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "database")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "12345")

    @property
    def database_url(self):
        """URL подключения к PostgreSQL (DSN)"""
        return (f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}")


config = Config()
