FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

COPY . /app

RUN chmod +x /app/entrypoint-test.sh /app/entrypoint.sh

EXPOSE 8000
