## Getting started

Start the python environment

```bash
python -m venv venv
source venv/bin/activate
```

Then, install the dependencies

```bash
pip install django
pip install dotenv
pip install pytest
pip install pytest-bdd
pip install dj_rest_auth
pip install allauth
pip install dj-rest-auth django-allauth
pip install djangorestframework django-cors-headers
pip install requests
```

Run the migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
