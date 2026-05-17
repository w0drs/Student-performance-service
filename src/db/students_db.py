from src.database import db

def get_student_id_by_name(first_name: str,
                           last_name: str,
                           patronymic: str) -> int:
    """
    Получить ID студента по ФИО
    """
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM students "
                "WHERE first_name = %s AND last_name = %s AND patronymic = %s",
                (first_name, last_name, patronymic)
            )
            row = cur.fetchone()
            return row[0] if row else None

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
            return cur.fetchone()[0]
