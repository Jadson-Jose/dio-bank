from models.role import Role
from models.user import User
import pytest
from src.app import create_app, db


@pytest.fixture
def app():
    app = create_app(enviroment="test")

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def access_token(client):
    role = Role(username="admin") # type: ignore
    db.session.add(role)
    db.session.commit()

    user = User(username="jhon-doe", password="test", role_id=role.id) # type: ignore
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login",
        json={
            "username": user.username,
            "password": user.password,
        },
    )
    return response.json["access_token"]
