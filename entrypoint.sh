#!/bin/sh
set -e

echo "Making sure dependencies are up to date..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "Waiting for database to be ready..."
python wait-for-db.py

echo "Automatically generating migrations..."
python manage.py makemigrations --noinput
python manage.py makemigrations desafio --noinput

echo "Applying migrations..."
python manage.py migrate --noinput
python manage.py migrate desafio --noinput

echo "Seeding database..."
python seed.py

echo "Running server..."
exec python manage.py runserver 0.0.0.0:8000
