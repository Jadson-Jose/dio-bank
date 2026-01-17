from http import HTTPStatus

from .utils import requires_role
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.app import bcrypt
from src.models import User, db

bp = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    data = request.get_json()
    required_fields = {"username", "password", "role_id"}
    missing = required_fields - data.keys()
    if missing:
        return {
            "error": f"Compos obrigatórios uasentes: {', '.join(missing)}",
        }, HTTPStatus.BAD_REQUEST
    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]),  # type: ignore
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "role": {
                "id": user.role.id,
                "username": user.role.username,
            },
        }
        for user in users
    ]


@bp.route("/", methods=["GET", "POST"])
@jwt_required()
@requires_role("admin")
def list_or_create_user():
    if request.method == "POST":
        _create_user()
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()}


@bp.route("<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user_id,
        "username": user.username,
    }


@bp.route("<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    if "username" in data:
        user.username = data["username"]
        db.session.commit()
    return {
        "id": user_id,
        "username": user.username,
    }


@bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
