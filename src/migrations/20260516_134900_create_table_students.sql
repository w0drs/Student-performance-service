CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    patronymic VARCHAR(255),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    group_name VARCHAR(10) NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS grades (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    grade INTEGER NOT NULL CHECK (grade >= 2 AND grade <= 5),
    grade_date DATE NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, grade_date)
);

-- Индексы для таблицы студентов
CREATE INDEX IF NOT EXISTS idx_students_first_name ON students(first_name);
CREATE INDEX IF NOT EXISTS idx_students_full_name ON students(last_name, first_name, patronymic);
-- Индексы для групп
CREATE INDEX IF NOT EXISTS idx_groups_group_name ON groups(group_name);
-- Индексы для оценок
CREATE INDEX IF NOT EXISTS idx_grades_group_id ON grades(group_id);
CREATE INDEX IF NOT EXISTS idx_grades_grade ON grades(grade);
CREATE INDEX IF NOT EXISTS idx_grades_student_grade ON grades(student_id, grade);
CREATE INDEX IF NOT EXISTS idx_grades_date_grade ON grades(grade_date, grade);
CREATE INDEX IF NOT EXISTS idx_grades_student_date ON grades(student_id, grade_date);
