from flask_login import current_user
from functools import wraps
from flask import redirect, url_for


def redirect_if_authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("public.products_page"))
        return f(*args, **kwargs)

    return decorated_function
