from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.db import db
from app.models import Article
from app.security import csrf_token, validate_csrf


posts_bp = Blueprint("posts", __name__)


def _article_form_data():
    title = request.form.get("title", "").strip()
    intro = request.form.get("intro", "").strip()
    text = request.form.get("text", "").strip()
    errors = []

    if not title:
        errors.append("Название статьи обязательно.")
    if not intro:
        errors.append("Короткое описание обязательно.")
    if not text:
        errors.append("Основной текст обязателен.")

    return {"title": title, "intro": intro, "text": text}, errors


@posts_bp.route("/posts", endpoint="posts")
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@posts_bp.route("/posts/<int:id>", endpoint="post_detail")
def post_detail(id):
    article = db.get_or_404(Article, id)
    return render_template("post_detail.html", article=article, csrf_token=csrf_token())


@posts_bp.route("/posts/delete/<int:id>", methods=["POST"], endpoint="post_delete")
def post_delete(id):
    validate_csrf(request.form.get("csrf_token"))
    article = db.get_or_404(Article, id)

    db.session.delete(article)
    db.session.commit()
    flash("Статья удалена.", "success")
    return redirect(url_for("posts.posts"))


@posts_bp.route("/posts/edit/<int:id>", methods=["POST", "GET"], endpoint="post_update")
def post_update(id):
    article = db.get_or_404(Article, id)
    errors = []

    if request.method == "POST":
        validate_csrf(request.form.get("csrf_token"))
        data, errors = _article_form_data()

        if not errors:
            article.title = data["title"]
            article.intro = data["intro"]
            article.text = data["text"]
            db.session.commit()
            flash("Статья обновлена.", "success")
            return redirect(url_for("posts.posts"))

        article.title = data["title"]
        article.intro = data["intro"]
        article.text = data["text"]

    return render_template(
        "post_edit.html",
        article=article,
        errors=errors,
        csrf_token=csrf_token(),
    )


@posts_bp.route("/posts/add", methods=["POST", "GET"], endpoint="add_post")
def add_post():
    errors = []
    data = {"title": "", "intro": "", "text": ""}

    if request.method == "POST":
        validate_csrf(request.form.get("csrf_token"))
        data, errors = _article_form_data()

        if not errors:
            article = Article(title=data["title"], intro=data["intro"], text=data["text"])
            db.session.add(article)
            db.session.commit()
            flash("Статья добавлена.", "success")
            return redirect(url_for("posts.posts"))

    return render_template(
        "add_article.html",
        article=data,
        errors=errors,
        csrf_token=csrf_token(),
    )
