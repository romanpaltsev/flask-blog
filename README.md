# Flask Blog

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3-111111?style=flat-square&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Tests](https://img.shields.io/badge/tests-pytest-0A7F64?style=flat-square)

A small, polished Flask blog application with PostgreSQL storage, SQLAlchemy models,
Bootstrap templates, CSRF-protected forms, demo content, and pytest coverage.

The app is intentionally compact: it is easy to read, easy to run, and useful as a
starter project for learning Flask CRUD flows.

## Features

- Article list, detail page, creation, editing, and deletion.
- SQLAlchemy model with PostgreSQL in Docker Compose.
- SQLite fallback for quick local development.
- Responsive Bootstrap-based UI with custom styling.
- CSRF token validation for mutating forms.
- Idempotent demo data seeding via `seed_demo.py`.
- Pytest coverage for public pages, validation, CRUD, and 404 behavior.

## Preview

The app runs locally at:

```text
http://127.0.0.1:5000
```

Main pages:

- `/` - landing page
- `/posts` - article list
- `/posts/add` - create article

Demo screenshot: https://disk.yandex.ru/d/pgzNNJdUj9IusA

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy
- **Database:** PostgreSQL 16 in Docker, SQLite fallback locally
- **Frontend:** Jinja templates, Bootstrap 5, Bootstrap Icons, custom CSS
- **Tooling:** uv, Docker Compose, pytest

## Quick Start With Docker

Start Flask and PostgreSQL:

```bash
docker compose up --build
```

The web container waits for PostgreSQL, creates the database schema, and serves the
app at http://127.0.0.1:5000.

Seed demo articles into the Docker PostgreSQL database:

```bash
docker compose exec web uv run python seed_demo.py
```

Stop the stack:

```bash
docker compose down
```

Stop the stack and remove the PostgreSQL volume:

```bash
docker compose down -v
```

## Local Development

Install dependencies:

```bash
uv sync
```

Create the database schema:

```bash
uv run python create_db.py
```

Add demo articles:

```bash
uv run python seed_demo.py
```

Run the Flask development server:

```bash
uv run flask --app app --debug run
```

`seed_demo.py` can be run multiple times. It checks existing article titles and
does not create duplicates.

## Configuration

Create `app/.env` for local secrets:

```env
SECRET_KEY=change-me
DATABASE_URL=postgresql+psycopg://flask_blog:flask_blog@localhost:5432/flask_blog
```

If `DATABASE_URL` is not set, the app uses local SQLite at `app.db`. Docker Compose
sets `DATABASE_URL` automatically for the `web` service.

## Tests

Run the test suite:

```bash
uv run pytest
```

Tests use a temporary SQLite database and cover:

- public page loading
- required-field validation
- article creation
- article editing
- article deletion
- missing article 404 responses

## Project Structure

```text
.
├── app/
│   ├── posts/
│   │   └── routes.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── img/hero-workspace.png
│   ├── templates/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── models.py
│   └── security.py
├── tests/
│   └── test_posts.py
├── create_db.py
├── seed_demo.py
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```

## Notes

`create_db.py` uses `db.create_all()`, which is enough for this small demo app.
For a growing production project, replace it with database migrations such as
Flask-Migrate/Alembic.
