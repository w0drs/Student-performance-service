def parse_full_name(full_name: str) -> tuple:
    """
    Парсит ФИО из строки
    """
    parts = full_name.strip().split()

    if len(parts) == 3:
        last_name, first_name, patronymic = parts
    elif len(parts) == 2:
        last_name, first_name = parts
        patronymic = None
    else:
        raise ValueError(f"Invalid full name format: {full_name}")

    return first_name, last_name, patronymic