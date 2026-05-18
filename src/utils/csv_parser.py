import pandas as pd
import io


def parse_csv(content: bytes) -> list[dict]:
    required_columns = ['Дата', 'Номер группы', 'ФИО', 'Оценка']

    df = None
    for encoding in ['utf-8', 'cp1251', 'utf-8-sig']:
        try:
            df = pd.read_csv(
                io.BytesIO(content),
                encoding=encoding,
                sep=';',
                dtype=str,
                usecols=required_columns,
                skipinitialspace=True
            )
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError("Unable to decode file")

    # Заменяем NaN на пустые строки и удаляем полностью пустые строки
    df = df.fillna('').replace(r'^\s*$', '', regex=True)
    df = df[df.ne('').any(axis=1)]

    return df.to_dict('records')
