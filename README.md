# Symcomp Server

## Before you get started

It is imperative the use of Docker to guarantee the consistency throught the development. So, it is necessary that you have in your computer softwares bellow:

- **Docker version 28.3.3** or later
- **Docker Compose version v2.39.1** or later

## Getting Started

In the project root execute

```bash
chmod +x ./backend/entrypoint.sh
chmod +x ./backend/entrypoint-test.sh
docker compose build --no-cache
docker compose up -d
```

Then, you can access the urls below to check it running

**Backend:** localhost:8000

There is a auto docs for the api. You can check it at:

**Redocs:** localhost:8000/redocs

If you want to drop the containers, make sure you do:

```bash
docker compose down -v
```

To make sure the docker is working properly you can do

```bash
docker ps
```

## Compiling each project individually (not recommended)

If you really need to test something up, make sure to follow below.

However, it is high recommended that you use the docker file to test the application.

In all cases, make sure that the project also work in the docker compose, for the deploy will be done in that very environment.

Becareful to never introduce new bugs in the systems because you are developing locally in your machine. Never use the old excuse: "It works in my computer" in case the application that fails to be deployed.

### Backend

Start the python environment

```bash
python -m venv venv
source venv/bin/activate
```

Then, install the dependencies

```bash
pip install -r requirements.txt
```
