## Getting started

Start the python environment

```bash
python -m venv venv
source venv/bin/activate
```

Then, install the dependencies

```bash
pip install -r requirements.txt
```

Run the migrations

```bash
python manage.py makemigrations api
python manage.py migrate
```

Run the server

```bash
python manage.py runserver
```
