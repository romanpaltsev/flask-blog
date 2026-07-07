FROM ghcr.io/astral-sh/uv:0.5.11-python3.11-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 5000

CMD ["sh", "-c", "uv run python create_db.py && uv run flask --app app --debug run --host 0.0.0.0 --port 5000"]
