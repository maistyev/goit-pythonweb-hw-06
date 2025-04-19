#!/bin/bash

pip install -r requirements.txt

if [ ! -f .env ]; then
    echo "Створення .env файлу з прикладу .env.example..."
    cp .env.example .env
    echo "Створено .env файл. Будь ласка, перевірте та оновіть налаштування, якщо потрібно."
fi

source .env

if ! docker ps | grep -q "postgres"; then
    echo "Запуск контейнера PostgreSQL..."
    docker run --name pg-student-db -p ${POSTGRES_PORT}:5432 -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -d postgres
    
    sleep 5
    
    docker exec -it pg-student-db psql -U ${POSTGRES_USER} -c "CREATE DATABASE ${POSTGRES_DB}"
else
    echo "PostgreSQL вже запущено"
fi

if [ ! -d "alembic" ]; then
    echo "Ініціалізація Alembic..."
    bash alembic_setup.sh
else
    echo "Alembic вже ініціалізовано"
    alembic upgrade head
fi

echo "Заповнення бази даних..."
python seed.py

echo "Виконання запитів..."
python my_select.py