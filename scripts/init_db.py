import psycopg2
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def init_db():
    """Создает таблицы в БД"""
    try:
        logger.info("Connecting to database...")
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "db"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            database=os.getenv("POSTGRES_DB", "grade_db"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "12345")
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'students')")
        if not cursor.fetchone()[0]:
            logger.info("Creating tables...")

            migration_path = '/app/src/migrations/20260516_134900_create_table_students.sql'

            if not os.path.exists(migration_path):
                logger.error("Migration file not found at: %s", migration_path)
                return False

            with open(migration_path, 'r', encoding='utf-8') as f:
                cursor.execute(f.read())
            logger.info("Tables created")
        else:
            logger.info("Tables already exist")

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.error("Error creating tables: %s", e)
        return False


if __name__ == "__main__":
    if not init_db():
        sys.exit(1)
