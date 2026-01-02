# jokesTOUNSI API

A RESTful API that preserves and classifies Tunisian jokes as a cultural encyclopedia.

## Features

- CRUD operations for jokes with Tunisian dialect text and literal translations (French, English).
- Classification by age group, era, region, acceptability, delivery type, tone, rhythm.
- JWT authentication with roles: user, contributor, admin.
- Google OAuth2 login that issues JWT tokens.
- Search, filtering, and pagination for jokes.
- OpenAPI/Swagger docs at `/api/v1/docs`.
- Dockerized with Gunicorn and Flask-Migrate for database migrations.

## Tech stack

- Flask, Flask-Smorest (REST + Swagger)
- SQLAlchemy, Marshmallow
- Flask-JWT-Extended, Authlib (Google OAuth2)
- SQLite for development, PostgreSQL-ready via `DATABASE_URL`
- Docker + Gunicorn, Flask-Migrate, pytest

## Local setup

```bash
git clone <your-repo-url>
cd jokesTOUNSI

python -m venv venv
# Windows Git Bash:
source venv/Scripts/activate
# Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt

# create .env from example or manually
# (SECRET_KEY, JWT_SECRET_KEY, DATABASE_URL, Google keys, etc.)
cp .env.example .env  # if you have one

flask db upgrade      # apply migrations
python app.py         # run dev server

## Running with Docker

```bash
docker build -t jokestounsiapi .
docker run -d -p 5000:5000 --env-file .env --name jokestounsicontainer jokestounsiapi
docker exec -it jokestounsicontainer flask db upgrade
