import pytest
import logging
from src.db import students_db, groups_db, grades_db

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("clean_db")
class TestGradesDB:

    def test_insert_grade(self):
        """Тест вставки оценки"""

        student_id = students_db.create_student("Иван", "Иванов", "Иванович")
        group_id = groups_db.create_group("101Б")
        logger.info(f"Создан student_id={student_id}, group_id={group_id}")

        grades_db.insert_grade(
            student_id=student_id,
            group_id=group_id,
            grade_date="11.03.2025",
            grade=5
        )

        # Получаем оценки
        grades = grades_db.get_student_grades(student_id)
        logger.debug(f"Получены оценки: {grades}")
        logger.debug(f"Тип: {type(grades)}")
        logger.debug(f"Длина: {len(grades)}")

        assert len(grades) == 1
        assert grades[0][0] == 5

    def test_insert_duplicate_grade(self):
        """Тест вставки дубликата"""

        student_id = students_db.create_student("Петр", "Петров", "Петрович")
        group_id = groups_db.create_group("102Б")

        grades_db.insert_grade(student_id, group_id, "11.03.2025", 5)

        grades_db.insert_grade(student_id, group_id, "11.03.2025", 4)

        grades = grades_db.get_student_grades(student_id)
        logger.info(f"оценки: {grades}")

        assert len(grades) == 1
        assert grades[0][0] == 5

    def test_get_student_grades_multiple(self):
        """Тест получения всех оценок студента"""

        student_id = students_db.create_student("Сергей", "Сергеев", "Сергеевич")
        group_id = groups_db.create_group("103М")

        grades_db.insert_grade(student_id, group_id, "11.03.2025", 5)
        grades_db.insert_grade(student_id, group_id, "12.03.2025", 4)
        grades_db.insert_grade(student_id, group_id, "13.03.2025", 3)

        grades = grades_db.get_student_grades(student_id)
        logger.debug(f"Получены оценки: {grades}")

        assert len(grades) == 3
        # Проверяем что оценки на месте (порядок: grade, date, group_id). Учитываем сортировку в sql запросе
        assert grades[0][0] == 3
        assert grades[1][0] == 4
        assert grades[2][0] == 5
