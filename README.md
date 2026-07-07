# Flask Blog

This is a small Flask blog application with PostgreSQL storage and Bootstrap templates.

Demo screenshot https://disk.yandex.ru/d/pgzNNJdUj9IusA

## Docker Compose setup

Copy the example environment file if you want to override local secrets:

```bash
cp .env.example .env
```

Start the app and PostgreSQL:

```bash
docker compose up --build
```

The app will create the database schema on startup and run at http://127.0.0.1:5000.

Stop the stack:

```bash
docker compose down
```

Remove the PostgreSQL volume as well:

```bash
docker compose down -v
```

## Local setup with uv

```bash
uv sync
uv run python create_db.py
uv run flask --app app --debug run
```

## Configuration

Create `app/.env` for local secrets:

```env
SECRET_KEY=change-me
DATABASE_URL=postgresql+psycopg://flask_blog:flask_blog@localhost:5432/flask_blog
```

The app falls back to a development key if `SECRET_KEY` is not set and to local SQLite if `DATABASE_URL` is not set. Docker Compose provides `DATABASE_URL` automatically.

## Tests

```bash
uv run pytest
```

Tests use a temporary SQLite database and cover basic page loading, article creation, editing, deletion, validation, and 404 handling.
