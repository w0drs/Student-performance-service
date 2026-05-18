from src.database import db

def get_group_id_by_name(group_name: str) -> int:
    """
    Получить ID группы по названию
    """
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM groups "
                "WHERE group_name = %s",
                (group_name,)
            )
            row = cur.fetchone()
            return row[0] if row else None

def create_group(group_name: str) -> int:
    """
    Создать новую группу
    """
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO groups (group_name) "
                "VALUES (%s) RETURNING id",
                (group_name,)
            )
            return cur.fetchone()[0]
