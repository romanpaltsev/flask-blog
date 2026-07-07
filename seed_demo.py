from datetime import datetime, timedelta

from app import create_app
from app.db import db
from app.models import Article


DEMO_ARTICLES = [
    {
        "title": "Как запустить Flask-блог локально",
        "intro": "Короткая инструкция по подготовке окружения, созданию базы и запуску сервера разработки.",
        "text": (
            "Для локального запуска проекта установите зависимости через uv, создайте схему базы "
            "данных и запустите Flask в debug-режиме. Если переменная DATABASE_URL не задана, "
            "приложение использует SQLite-файл app.db в корне проекта. Для разработки с PostgreSQL "
            "удобнее запускать стек через Docker Compose."
        ),
        "days_ago": 1,
    },
    {
        "title": "Зачем нужны шаблоны Jinja",
        "intro": "Jinja помогает собирать HTML-страницы из общих блоков и данных приложения.",
        "text": (
            "В этом блоге шаблоны наследуются от base.html, поэтому навигация, подключение CSS "
            "и базовая структура страницы описаны один раз. Страницы со списком статей, деталями "
            "и формами переиспользуют общий каркас, а внутрь подставляют только собственное "
            "содержимое."
        ),
        "days_ago": 3,
    },
    {
        "title": "Простая модель статьи на SQLAlchemy",
        "intro": "Модель Article описывает таблицу articles и основные поля публикации.",
        "text": (
            "SQLAlchemy позволяет работать с записями базы как с Python-объектами. В модели Article "
            "есть заголовок, краткое описание, основной текст и дата публикации. Такой набор полей "
            "достаточен для базового CRUD: создать статью, показать список, открыть детальную "
            "страницу, отредактировать или удалить запись."
        ),
        "days_ago": 5,
    },
    {
        "title": "Docker Compose для разработки",
        "intro": "Compose поднимает веб-приложение и PostgreSQL одной командой.",
        "text": (
            "Docker Compose полезен, когда приложение зависит от внешних сервисов. В этом проекте "
            "контейнер web ждет готовности PostgreSQL, создает таблицы и запускает Flask-сервер. "
            "Это делает окружение предсказуемым: всем разработчикам достаточно выполнить одну "
            "команду, чтобы получить одинаковую базу и приложение."
        ),
        "days_ago": 7,
    },
    {
        "title": "Проверяем блог через pytest",
        "intro": "Тесты используют временную SQLite-базу и Flask test client.",
        "text": (
            "Автотесты помогают быстро проверить основные сценарии: открытие публичных страниц, "
            "валидацию формы, создание, редактирование и удаление статей. Для тестов приложение "
            "получает отдельную конфигурацию, поэтому проверки не затрагивают локальную или "
            "Docker-базу разработчика."
        ),
        "days_ago": 10,
    },
]


def seed_demo_articles():
    db.create_all()

    created_count = 0
    now = datetime.utcnow()

    for article_data in DEMO_ARTICLES:
        existing_article = Article.query.filter_by(title=article_data["title"]).first()
        if existing_article:
            continue

        article = Article(
            title=article_data["title"],
            intro=article_data["intro"],
            text=article_data["text"],
            date=now - timedelta(days=article_data["days_ago"]),
        )
        db.session.add(article)
        created_count += 1

    db.session.commit()
    return created_count


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        created = seed_demo_articles()
        print(f"Added {created} demo articles.")
