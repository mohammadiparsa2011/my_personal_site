#!/bin/sh

# منتظر شدن برای دیتابیس
while ! nc -z db 5432; do
  echo "Waiting for Postgres..."
  sleep 1
done

# migrate
python manage.py migrate

# runserver
exec "$@"
