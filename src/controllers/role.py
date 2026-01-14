from http import HTTPStatus

from flask import Blueprint, request

from src.app import Role, db

bp = Blueprint("role", __name__, url_prefix="/roles")


@bp.route("/", methods=["POST"])
def create_role():
    data = request.json
    role = Role(username=data["username"])
    db.session.add(role)
    db.session.commit()
    return {"message": "Role created!"}, HTTPStatus.CREATED
