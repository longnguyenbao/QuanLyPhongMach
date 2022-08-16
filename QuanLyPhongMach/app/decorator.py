from functools import wraps
from flask import redirect, url_for, request
from flask_login import current_user
from app.models import UserRole


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.user_role == UserRole.ADMIN:
            return f(*args, **kwargs)

        return redirect(url_for('login', next=request.url))

    return decorated_function