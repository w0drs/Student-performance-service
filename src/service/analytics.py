from src.db.grades_db import get_students_by_twos_count

def get_students_more_than_3_twos():
    """
    Возвращает ФИО студентов, у которых оценка 2 встречается больше 3 раз.
    """
    return get_students_by_twos_count('>', 3)

def get_students_less_than_5_twos():
    """
    Возвращает ФИО студентов, у которых оценка 2 встречается меньше 5 раз.
    """
    return get_students_by_twos_count('<', 5)
