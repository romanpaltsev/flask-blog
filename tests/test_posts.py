import re

import pytest

from app import create_app
from app.db import db
from app.models import Article


def csrf_token(response):
    match = re.search(rb'name="csrf_token" value="([^"]+)"', response.data)
    assert match is not None
    return match.group(1).decode()


@pytest.fixture()
def app(tmp_path):
    test_app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}",
        }
    )

    with test_app.app_context():
        db.create_all()

    yield test_app

    with test_app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_public_pages_load(client):
    for path in ["/", "/about", "/posts"]:
        response = client.get(path)
        assert response.status_code == 200


def test_add_post_validates_required_fields(client, app):
    response = client.get("/posts/add")
    token = csrf_token(response)

    response = client.post(
        "/posts/add",
        data={"csrf_token": token, "title": "", "intro": "", "text": ""},
    )

    assert response.status_code == 200
    assert "Название статьи обязательно.".encode() in response.data
    with app.app_context():
        assert Article.query.count() == 0


def test_article_crud_flow(client, app):
    response = client.get("/posts/add")
    token = csrf_token(response)
    response = client.post(
        "/posts/add",
        data={
            "csrf_token": token,
            "title": "First post",
            "intro": "Short intro",
            "text": "Full text",
        },
    )
    assert response.status_code == 302

    with app.app_context():
        article = Article.query.one()
        article_id = article.id
        assert article.title == "First post"

    response = client.get(f"/posts/{article_id}")
    assert response.status_code == 200
    assert b"First post" in response.data

    response = client.get(f"/posts/edit/{article_id}")
    token = csrf_token(response)
    response = client.post(
        f"/posts/edit/{article_id}",
        data={
            "csrf_token": token,
            "title": "Updated post",
            "intro": "Updated intro",
            "text": "Updated text",
        },
    )
    assert response.status_code == 302

    with app.app_context():
        assert db.session.get(Article, article_id).title == "Updated post"

    assert client.get(f"/posts/delete/{article_id}").status_code == 405

    response = client.get(f"/posts/{article_id}")
    token = csrf_token(response)
    response = client.post(f"/posts/delete/{article_id}", data={"csrf_token": token})
    assert response.status_code == 302

    with app.app_context():
        assert Article.query.count() == 0


def test_missing_article_returns_404(client):
    assert client.get("/posts/999").status_code == 404
    assert client.get("/posts/edit/999").status_code == 404
