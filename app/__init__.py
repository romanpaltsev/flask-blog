from flask import Flask, render_template
from app.db import db
from app.config import Config
from app.posts.routes import posts_bp


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)
    db.init_app(app)
    app.register_blueprint(posts_bp)

    @app.route('/')
    @app.route('/home')
    def index():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    return app
