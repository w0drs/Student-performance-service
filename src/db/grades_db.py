from src.database import db
import logging

logger = logging.getLogger(__name__)

def insert_grade(student_id: int,
                 group_id: int,
                 grade_date: str,
                 grade: int) -> None:
    """
    Вставить оценку студента
    """
    # Конвертируем дату из DD.MM.YYYY в YYYY-MM-DD
    day, month, year = grade_date.split('.')
    sql_date = f"{year}-{month}-{day}"

    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO grades (student_id, group_id, grade_date, grade)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (student_id, grade_date) DO NOTHING
                """,
                (student_id, group_id, sql_date, grade)
            )
            logger.debug("Inserted: student=%s, grade=%s, rows affected=%s",
                         student_id, grade, cur.rowcount)


def get_student_grades(student_id: int) -> list:
    """
    Получить все оценки студента
    """
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT grade, grade_date, group_id 
                FROM grades 
                WHERE student_id = %s 
                ORDER BY grade_date DESC
                """,
                (student_id,)
            )
            return cur.fetchall()


def get_students_by_twos_count(operator: str,
                               value: int) -> list[dict]:
    """
    Получить студентов по количеству двоек и услловию

    Args:
        operator: '>' or '<' or '>=' or '<='
        value: число двоек для сравнения
    """
    allowed_operators = {'>', '<', '>=', '<='}
    if operator not in allowed_operators:
        raise ValueError(f"Unsupported operator: {operator}. Allowed: {allowed_operators}")

    with db.get_connection() as conn:
        with conn.cursor() as cur:
            query = f"""
                SELECT 
                    s.last_name,
                    s.first_name,
                    s.patronymic,
                    COUNT(g.id) as twos_count
                FROM students s
                JOIN grades g ON s.id = g.student_id
                WHERE g.grade = 2
                GROUP BY s.id, s.last_name, s.first_name, s.patronymic
                HAVING COUNT(g.id) {operator} %s
                ORDER BY twos_count DESC
            """
            cur.execute(query, (value,))
            rows = cur.fetchall()
            return [
                {
                    "full_name": f"{row[0]} {row[1]} {row[2] or ''}".strip(),
                    "count_twos": row[3]
                }
                for row in rows
            ]
