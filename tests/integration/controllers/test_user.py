from http import HTTPStatus

from sqlalchemy import func
from src.models import Role, User, db


def test_get_user_success(client, app):
    with app.app_context():
        # Given
        role = Role(username="admin")
        db.session.add(role)
        db.session.commit()

        user = User(username="jhon-doe", password="test", role_id=role.id)
        db.session.add(user)
        db.session.commit()

        user_id = user.id

    # when
    response = client.get(f"/users/{user_id}")

    # then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": user.id,
        "username": user.username,
    }


def test_get_user_not_found(client, app):
    with app.app_context():
        # Given
        role = Role(username="admin")
        db.session.add(role)
        db.session.commit()

        user_id = 1

    # when
    response = client.get(f"/users/{user_id}")

    # then
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_user(client, access_token):
    # Given
    role_id = db.session.execute(
        db.select(Role.id).where(Role.username == "admin")
    ).scalar()
    payload = {"username": "user2", "password": "user2", "role_id": role_id}

    # When
    response = client.post(
        "/users/", json=payload, headers={"Authorization": f"Bearer {access_token}"}
    )

    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "User created!"}
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 2


def test_list_users(client, access_token):
    # Given
    user = db.session.execute(
        db.select(User).where(User.username == "jhon-doe")
    ).scalar()

    # When
    response = client.post(
        "/auth/login",
        json={
            "username": user.username,
            "password": user.password,
        },
    )
    access_token = response.json["access_token"]

    user_id = user.id

    # when
    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {access_token}"}
    )

    # then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "role": {
                    "id": user.role.id,
                    "username": user.role.username,
                },
            }
        ]
    }
