from datetime import datetime
import re


def validate_date(date_str: str) -> bool:
    """Проверка формата даты DD.MM.YYYY"""
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def validate_group_number(group: str) -> bool:
    """Проверка формата группы: 3 цифры и буква (например: 101Б)"""
    return bool(re.match(r'^\d{3}[А-Я]$', group))


def validate_grade(grade: int) -> bool:
    """Оценка в пределах от 2 до 5"""
    return 2 <= grade <= 5


def validate_full_name(full_name: str) -> bool:
    """
    Проверка формата ФИО
    Допустимые форматы:
    - "Шмель Дмитрий" (фамилия + имя)
    - "Шмель Дмитрий Антонович" (фамилия + имя + отчество)
    """
    parts = full_name.strip().split()

    if len(parts) not in (2, 3):
        return False

    # Проверяем что все части не пустые и длиной больше 1 символа
    return all(len(part) > 1 for part in parts)


def parse_full_name(full_name: str) -> tuple:
    """
    Парсит ФИО. Формат: 'Фамилия Имя' или 'Фамилия Имя Отчество'

    Returns:
        (first_name, last_name, patronymic)
    """
    parts = full_name.strip().split()

    if len(parts) == 3:
        last_name, first_name, patronymic = parts
        return first_name, last_name, patronymic
    elif len(parts) == 2:
        last_name, first_name = parts
        return first_name, last_name, None
    else:
        raise ValueError(f"Invalid full name format: {full_name}")


def validate_csv_row(row: dict) -> None:
    """Валидация строки CSV"""
    if not validate_date(row['Дата']):
        raise ValueError(f"Invalid date: {row['Дата']}")

    if not validate_group_number(row['Номер группы']):
        raise ValueError(f"Invalid group number: {row['Номер группы']}")

    if not validate_grade(int(row['Оценка'])):
        raise ValueError(f"Invalid grade: {row['Оценка']}")

    if not validate_full_name(row['ФИО']):
        raise ValueError(f"Invalid full name format: {row['ФИО']}. Expected 'Фамилия Имя' or 'Фамилия Имя Отчество'")
