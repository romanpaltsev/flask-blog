import secrets

from flask import abort, session


CSRF_SESSION_KEY = "_csrf_token"


def csrf_token():
    token = session.get(CSRF_SESSION_KEY)
    if token is None:
        token = secrets.token_urlsafe(32)
        session[CSRF_SESSION_KEY] = token
    return token


def validate_csrf(form_token):
    if not form_token or form_token != session.get(CSRF_SESSION_KEY):
        abort(400, description="Invalid CSRF token")
