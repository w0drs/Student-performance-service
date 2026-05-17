from src.db import grades_db
from src.utils.fullname_parser import parse_full_name
from src.utils.csv_parser import parse_csv
from src.validation import validate_csv_row
from src.db.students_db import get_student_id_by_name, create_student
from src.db.groups_db import get_group_id_by_name, create_group

def process_upload(file_content: bytes) -> dict:
    rows: list[dict] = parse_csv(file_content)
    students_set = set()
    records_loaded = 0

    for row in rows:
        validate_csv_row(row)

        # Парсим ФИО
        first_name, last_name, patronymic = parse_full_name(row['ФИО'])

        # Получаем или создаем студента
        student_id = get_student_id_by_name(first_name, last_name, patronymic)
        if not student_id:
            student_id = create_student(first_name, last_name, patronymic)

        # Получаем или создаем группу
        group_id = get_group_id_by_name(row['Номер группы'])
        if not group_id:
            group_id = create_group(row['Номер группы'])

        # Вставляем оценку
        grades_db.insert_grade(
            student_id=student_id,
            group_id=group_id,
            grade_date=row['Дата'],
            grade=int(row['Оценка'])
        )

        students_set.add(row['ФИО'])
        records_loaded += 1

    return {
        "status": "ok",
        "records_loaded": records_loaded,
        "students": len(students_set)
    }
