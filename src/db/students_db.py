from src.database import db
import logging

logger = logging.getLogger(__name__)

def get_student_id_by_name(first_name: str, last_name: str, patronymic: str = None) -> int | None:
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, first_name, last_name FROM students")
            all_students = cur.fetchall()
            logger.debug("DEBUG: All students in DB: %s", all_students)

            cur.execute(
                "SELECT id FROM students WHERE first_name = %s AND last_name = %s",
                (first_name, last_name)
            )
            row = cur.fetchone()
            if row:
                logger.debug("Found student: id=%s, first_name=%s, last_name=%s",
                             row[0], first_name, last_name)
                return row[0]

            logger.debug("NOT FOUND: first_name=%s, last_name=%s", first_name, last_name)
            return None

def create_student(first_name: str,
                   last_name: str,
                   patronymic: str | None) -> int:
    """
    Создать нового студента
    """
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO students (first_name, last_name, patronymic) "
                "VALUES (%s, %s, %s) RETURNING id",
                (first_name, last_name, patronymic)
            )
            student_id = cur.fetchone()[0]
            logger.debug("Created student: id=%s, name=%s %s", student_id, last_name, first_name)
            return student_id
