# tests/integration/controllers/test_user.py - Adicione no topo
from http import HTTPStatus


def test_get_user_success(client, access_token):
    """Testa a obtenção de um usuário existente."""
    # Primeiro, criar um usuário
    from flask_bcrypt import Bcrypt
    from src.models import Role, User, db

    with client.application.app_context():
        bcrypt = Bcrypt()
        user_role = Role.query.filter_by(name="user").first()

        hashed_password = bcrypt.generate_password_hash("testpassword").decode("utf-8")
        new_user = User(
            username="testuser", password=hashed_password, role_id=user_role.id
        )
        db.session.add(new_user)
        db.session.commit()
        user_id = new_user.id

    response = client.get(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json["id"] == user_id
    assert response.json["username"] == "testuser"


def test_get_user_not_found(client, access_token):
    """Testa a obtenção de um usuário inexistente."""
    response = client.get(
        "/users/9999", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_user(client, access_token, app):
    """Testa a criação de um novo usuário."""
    # Primeiro, garantir que temos a role 'user'
    with app.app_context():
        from src.models import Role

        user_role = Role.query.filter_by(name="user").first()
        role_id = user_role.id

    user_data = {
        "username": "newuser",
        "password": "NewPassword123",
        "role_id": role_id,
    }

    response = client.post(
        "/users/", json=user_data, headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert "id" in response.json
    assert response.json["username"] == "newuser"


def test_list_users(client, access_token, app):
    """Testa a listagem de usuários."""
    # Adicionar alguns usuários para testar
    from flask_bcrypt import Bcrypt
    from src.models import Role, User, db

    with app.app_context():
        bcrypt = Bcrypt()
        user_role = Role.query.filter_by(name="user").first()

        # Criar alguns usuários de teste
        for i in range(3):
            hashed_password = bcrypt.generate_password_hash(f"password{i}").decode(
                "utf-8"
            )
            user = User(
                username=f"testuser{i}", password=hashed_password, role_id=user_role.id
            )
            db.session.add(user)
        db.session.commit()

    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == HTTPStatus.OK
    # response.json é um dicionário com a chave 'users'
    assert isinstance(response.json, dict)
    assert "users" in response.json
    assert isinstance(response.json["users"], list)
    # Verificar que temos pelo menos 4 usuários (admin + 3 criados)
    assert len(response.json["users"]) >= 4
