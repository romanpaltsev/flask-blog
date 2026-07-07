# Repository Guidelines

## Project Structure & Module Organization

This is a small Flask blog application. Application code lives in `app/`: `__init__.py` creates the Flask app and registers blueprints, `db.py` owns the SQLAlchemy instance, `models.py` contains database models, `config.py` contains configuration, and `app/posts/` contains article routes. HTML templates are in `app/templates/`, and CSS assets are in `app/static/css/`. Docker Compose runs PostgreSQL for development; local SQLite is only a fallback when `DATABASE_URL` is unset.

## Build, Test, and Development Commands

- `docker compose up --build` starts Flask and PostgreSQL locally.
- `docker compose down` stops the stack.
- `uv sync` creates/updates the local environment from `pyproject.toml`.
- `uv run python create_db.py` creates the schema for the configured database.
- `uv run flask --app app --debug run` runs the app locally.

## Coding Style & Naming Conventions

Use Python 3 with 4-space indentation and PEP 8 naming: `snake_case` for functions and variables, `PascalCase` for model classes, and lowercase module names. Keep route handlers short and place shared database state in `app/db.py`. Template files should use descriptive lowercase names such as `post_detail.html`; static files should stay under `app/static/`.

## Testing Guidelines

Tests live in `tests/` and use `pytest` with Flask’s test client. Name files `test_<feature>.py` and test functions `test_<expected_behavior>()`. Cover route status codes, redirects, form submissions, and database changes for article creation, editing, and deletion.

## Commit & Pull Request Guidelines

Recent commit history uses short imperative or descriptive messages, for example `Update README.md` and `minor edits to the template`. Keep commits focused and explain user-visible behavior when relevant. Pull requests should include a concise summary, setup or migration notes, linked issues if any, and screenshots for template or CSS changes. Mention any manual checks performed, such as running `python create_db.py` and opening `/posts`.

## Security & Configuration Tips

Keep `.env`, `app.db`, virtual environments, and `__pycache__/` out of version control. Set `SECRET_KEY` and `DATABASE_URL` through the environment rather than hard-coding them. Docker Compose uses `postgresql+psycopg://flask_blog:flask_blog@db:5432/flask_blog` inside the network.
