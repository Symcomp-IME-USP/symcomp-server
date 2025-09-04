import os
import socket
import time
import subprocess

host = os.environ.get("DATABASE_HOST", "postgres")
port = int(os.environ.get("DATABASE_PORT", 5432))

cmd = ["python", "manage.py", "runserver", "0.0.0.0:8000"]

print(f"Aguardando Postgres em {host}:{port}...")

while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            break
    except OSError:
        print(f"Postgres ainda não está pronto em {host}:{port}, aguardando...")
        time.sleep(2)

print("Postgres está pronto! Iniciando Django...")
subprocess.run(cmd)
