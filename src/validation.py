from datetime import datetime
import re

def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def validate_group_number(group: str) -> bool:
    return bool(re.match(r'^\d{3}[А-Я]$', group))

def validate_grade(grade: int) -> bool:
    """Оценка в пределах от 2 до 5"""
    return 2 <= grade <= 5

def validate_csv_row(row: dict) -> None:
    if not validate_date(row['Дата']):
        raise ValueError(f"Invalid date: {row['Дата']}")
    if not validate_group_number(row['Номер группы']):
        raise ValueError(f"Invalid group: {row['Номер группы']}")
    if not validate_grade(int(row['Оценка'])):
        raise ValueError(f"Invalid grade: {row['Оценка']}")
    if not row['ФИО'] or len(row['ФИО'].strip()) < 3:
        raise ValueError(f"Invalid name: {row['ФИО']}")
