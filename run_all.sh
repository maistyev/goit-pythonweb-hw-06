#!/bin/bash

# Встановлення залежностей
pip install -r requirements.txt

# Запуск Docker-контейнера з PostgreSQL (якщо ще не запущено)
if ! docker ps | grep -q "postgres"; then
    echo "Запуск контейнера PostgreSQL..."
    docker run --name pg-student-db -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
    
    # Почекати, поки PostgreSQL повністю запуститься
    sleep 5
    
    # Створення бази даних
    docker exec -it pg-student-db psql -U postgres -c "CREATE DATABASE student_db"
else
    echo "PostgreSQL вже запущено"
fi

# Ініціалізація Alembic (якщо ще не ініціалізовано)
if [ ! -d "alembic" ]; then
    echo "Ініціалізація Alembic..."
    bash alembic_setup.sh
else
    echo "Alembic вже ініціалізовано"
    # Виконання міграцій
    alembic upgrade head
fi

# Заповнення бази даних випадковими даними
echo "Заповнення бази даних..."
python seed.py

# Виконання запитів
echo "Виконання запитів..."
python my_select.py