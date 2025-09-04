#!/bin/sh
set -e

echo "Waiting for database to be ready..."
python wait-for-db.py

echo "Making sure dependencies are up to date..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "Automatically generating migrations..."
python manage.py makemigrations --noinput

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Running server..."
exec python manage.py runserver 0.0.0.0:8000
