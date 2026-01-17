from http import HTTPStatus

from flask import Blueprint, current_app, request
from flask_jwt_extended import create_access_token

from src.models import User, db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return {"msg": "Missing username or password"}, HTTPStatus.BAD_REQUEST

    # Buscar usuário
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()

    if not user:
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    # Verificar senha - usar current_app.bcrypt
    if not current_app.bcrypt.check_password_hash(user.password, password):
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    # Verificar se o usuário está ativo
    if not user.active:
        return {"msg": "User is not active"}, HTTPStatus.UNAUTHORIZED

    # Criar token JWT
    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}, HTTPStatus.OK
