import pytest
from src.db import students_db

@pytest.mark.usefixtures("clean_db")
class TestStudentsDB:
    def test_create_student(self):
        """Тест создания студента"""
        student_id = students_db.create_student("Иван", "Иванов", "Иванович")

        assert student_id > 0

    def test_get_student_by_name(self):
        """Тест поиска студента по ФИО"""
        expected_id = students_db.create_student("Петр", "Петров", "Петрович")
        found_id = students_db.get_student_id_by_name("Петр", "Петров", "Петрович")

        assert found_id == expected_id

    def test_get_student_not_found(self):
        """Тест поиска несуществующего студента"""
        student_id = students_db.get_student_id_by_name("Не", "Существует", "Не")

        assert student_id is None
