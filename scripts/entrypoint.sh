#!/bin/bash
set -e

echo "Waiting for database..."
while ! pg_isready -h db -p 5432 -U postgres; do
    sleep 1
done

echo "Running migrations..."
python scripts/init_db.py

echo "Starting app..."
uvicorn src.main:app --host 0.0.0.0 --port 8000