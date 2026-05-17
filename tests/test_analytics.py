import pytest
from src.db import students_db, groups_db, grades_db
from src.service.analytics import get_students_less_than_5_twos, get_students_more_than_3_twos


@pytest.mark.usefixtures("clean_db")
class TestAnalytics:

    def test_more_than_3_twos(self):
        """Студент с 4 двойками попадает в результат"""
        group_id = groups_db.create_group("101Б")
        student_id = students_db.create_student("Двоечник", "Двоечников", None)

        for i in range(4):
            grades_db.insert_grade(student_id, group_id, f"0{i + 1}.03.2025", 2)

        result = get_students_more_than_3_twos()

        assert len(result) == 1
        assert result[0]["count_twos"] == 4

    def test_more_than_3_twos_empty(self):
        """Нет студентов с >3 двоек"""
        group_id = groups_db.create_group("101Б")
        student_id = students_db.create_student("Ученик", "Учеников", None)

        for i in range(2):
            grades_db.insert_grade(student_id, group_id, f"0{i + 1}.03.2025", 2)

        result = get_students_more_than_3_twos()

        assert len(result) == 0

    def test_less_than_5_twos(self):
        """Студент с 3 двойками попадает в результат"""
        group_id = groups_db.create_group("101Б")
        student_id = students_db.create_student("Ученик", "Учеников", None)

        for i in range(3):
            grades_db.insert_grade(student_id, group_id, f"0{i + 1}.03.2025", 2)

        result = get_students_less_than_5_twos()

        assert len(result) == 1
        assert result[0]["count_twos"] == 3
