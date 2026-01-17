from functools import wraps
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity

from src.models import User, db


def requires_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = int(get_jwt_identity())
            user = db.get_or_404(User, user_id)

            if user.role.username != role_name:
                return {"message": "User do not have access."}, HTTPStatus.FORBIDDEN
            return f(*args, **kwargs)

        return wrapped

    return decorator


def elevar_quadrado(x):
    return x
