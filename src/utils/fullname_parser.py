def parse_full_name(full_name: str) -> tuple:
    """Парсит ФИО. Формат: 'Фамилия Имя Отчество' или 'Фамилия Имя'"""
    parts = full_name.strip().split()

    if len(parts) == 3:
        last_name, first_name, patronymic = parts
        return first_name, last_name, patronymic
    elif len(parts) == 2:
        last_name, first_name = parts
        return first_name, last_name, None
    else:
        raise ValueError(f"Invalid full name format: {full_name}")
