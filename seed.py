import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

User = get_user_model()

print("Seeding database...")

if not User.objects.filter(email="admin@example.com").exists():
    User.objects.create_superuser(
        email="admin@symcomp.ime.usp.br",
        name="Administrador",
        password="symcompmelhorquesemcomp"
    )
if not User.objects.filter(email="jonathas@symcomp.ime.usp.br").exists():
    User.objects.create_user(
        email="jonathas@symcomp.ime.usp.br",
        name="Jonathas Castilho",
        password="jojotadinho"
    )
