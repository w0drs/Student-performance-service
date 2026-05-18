# Student Performance Service

Сервис для загрузки и анализа успеваемости студентов.

## Цель  
- Разработать REST-сервис на FastAPI для загрузки и анализа успеваемости студентов.  
- Сервис должен принимать .csv файл, сохранять данные в БД и предоставлять ручки для анализа.  

## Сервис должен:
1. Принимать CSV-файл и сохранять данные в PostgreSQL.
2. Выполнять валидацию данных.
3. Предоставлять две аналитические ручки.
4. Работать строго через SQL-запросы (без ORM)
5. Возвращать данные в формате JSON.

## Структура проекта
```text
src/
├── api/                                           # REST эндпоинты
│   ├── upload.py                                  # POST /upload-grades
│   └── analytics.py                               # GET /students/...
├── db/                                            # работа с БД
│   ├── students_db.py
│   ├── groups_db.py
│   └── grades_db.py
├── service/                                       # бизнес-логика
│   ├── upload_file.py
│   └── analytics.py
├── utils/                                         # утилиты
│   ├── csv_parser.py
│   └── fullname_parser.py
├── migrations/                                    # SQL миграции
│   └── 20260516_134900_create_table_students.sql
├── logging_config.py                              # настройка логирования
├── database.py                                    # подключение к БД
├── config.py                                      # переменные окружения
├── validation.py                                  # валидация данных
├── schemas.py                                     # Pydantic схемы
└── main.py                                        # входная точка
```

## Настройка переменных окружения
Для работы сервиса требуется файл `.env` с параметрами подключения к БД:
```bash
# Скопируйте пример конфигурации
cp .env_example .env

# Отредактируйте .env, если надо
```

`.env_example`:
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=grade_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345
```

- Для локального запуска используйте POSTGRES_HOST=localhost.  
- Для запуска через Docker используйте POSTGRES_HOST=db.  

## Запуск через Docker

```bash
# Клонировать репозиторий
git clone https://github.com/w0drs/Student-performance-service
cd Student-performance-service

# Скопировать и настроить переменные окружения
cp .env_example .env

# Запустить сервис
docker-compose up --build
```
Сервис будет доступен по адресу: `http://localhost:8000`

## Локальный запуск 
1. Установить PostgreSQL и создать базу данных grade_db
2. Выполнить миграцию из src/migrations/20260516_134900_create_table_students.sql
3. Создать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```
4. Установить зависимости:
```bash
pip install -r requirements.txt
```
5. Настроить переменные окружения
```bash
cp .env_example .env
```
Убедитесь, что в .env указано:
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=grade_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=ваш_пароль
```

6. Запустить сервер:
```bash
uvicorn src.main:app --reload
```
Сервис будет доступен по адресу: `http://localhost:8000`

## API Эндпоинты
### Загрузить CSV файл

```bash
POST /upload-grades
```
- Формат CSV: Дата;Номер группы;ФИО;Оценка

Пример запроса:
```bash
curl -X POST "http://localhost:8000/upload-grades" \
  -F "file=@grades.csv"
```

Пример ответа:
```json
{
    "status": "ok",
    "records_loaded": 2000,
    "students": 40
}
```

### Студенты с более чем 3 двойками
```bash
GET /students/more-than-3-twos
```

Пример ответа:
```json
[
    {
        "full_name": "Иванов Иван Иванович",
        "count_twos": 4
    }
]
```

### Студенты с менее чем 5 двойками
```bash
GET /students/less-than-5-twos
```
Пример ответа:
```json
[
    {
        "full_name": "Петров Петр Петрович",
        "count_twos": 1
    }
]
```

## Запуск тестов
```bash
pytest tests/ -v
```

## Репозиторий
[https://github.com/w0drs/Student-performance-service](https://github.com/w0drs/Student-performance-service)
