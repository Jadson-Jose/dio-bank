# src/controllers/user.py - VERSÃO COMPLETA CORRIGIDA
from http import HTTPStatus

from flask import Blueprint, current_app, request
from flask_jwt_extended import jwt_required

from src.models import User, db

from .utils import requires_role

bp = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    data = request.get_json()

    # Verificar se data é None
    if not data:
        return {"error": "No JSON data provided"}, HTTPStatus.BAD_REQUEST

    required_fields = {"username", "password", "role_id"}
    missing = required_fields - data.keys()
    if missing:
        return {
            "error": f"Campos obrigatórios ausentes: {', '.join(missing)}",
        }, HTTPStatus.BAD_REQUEST

    # Verificar se usuário já existe
    existing_user = db.session.execute(
        db.select(User).where(User.username == data["username"])
    ).scalar()

    if existing_user:
        return {"error": "Username already exists"}, HTTPStatus.CONFLICT

    # Usar o bcrypt do current_app
    hashed_password = current_app.bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    user = User(
        username=data["username"], password=hashed_password, role_id=data["role_id"]
    )

    db.session.add(user)
    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
        "role_id": user.role_id,
        "active": user.active,
    }, HTTPStatus.CREATED


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "role": {
                "id": user.role.id,
                "name": user.role.name,  # CORREÇÃO: 'name' em vez de 'username'
            },
            "active": user.active,
        }
        for user in users
    ]


@bp.route("/", methods=["GET", "POST"])
@jwt_required()
@requires_role("admin")
def list_or_create_user():
    if request.method == "POST":
        return _create_user()
    else:
        return {"users": _list_users()}, HTTPStatus.OK


@bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
        "role_id": user.role_id,
        "active": user.active,
    }, HTTPStatus.OK


@bp.route("/<int:user_id>", methods=["PATCH"])
@jwt_required()
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.get_json()

    if not data:
        return {"error": "No JSON data provided"}, HTTPStatus.BAD_REQUEST

    if "username" in data:
        # Verificar se o novo username já existe (exceto para o próprio usuário)
        if data["username"] != user.username:
            existing = db.session.execute(
                db.select(User).where(User.username == data["username"])
            ).scalar()
            if existing:
                return {"error": "Username already exists"}, HTTPStatus.CONFLICT
        user.username = data["username"]

    if "password" in data:
        hashed_password = current_app.bcrypt.generate_password_hash(
            data["password"]
        ).decode("utf-8")
        user.password = hashed_password

    if "role_id" in data:
        user.role_id = data["role_id"]

    if "active" in data:
        user.active = bool(data["active"])

    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
        "role_id": user.role_id,
        "active": user.active,
    }, HTTPStatus.OK


@bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@requires_role("admin")
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
