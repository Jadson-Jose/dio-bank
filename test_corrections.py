# test_corrections.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_corrections():
    print("🔧 Testando correções...")

    from src.app import create_app
    from src.models import Role, User, db

    app = create_app()

    with app.app_context():
        # Configurar banco limpo
        db.drop_all()
        db.create_all()

        # Criar roles
        admin_role = Role(name="admin")
        user_role = Role(name="user")
        db.session.add_all([admin_role, user_role])
        db.session.commit()

        # Criar usuário admin
        hashed_password = app.bcrypt.generate_password_hash("admin123").decode("utf-8")
        admin_user = User(
            username="admin", password=hashed_password, role_id=admin_role.id
        )
        db.session.add(admin_user)
        db.session.commit()

        print(f"✅ Admin role name: {admin_role.name}")
        print(f"✅ Admin user role name: {admin_user.role.name}")

        # Testar o decorator requires_role
        from flask_jwt_extended import create_access_token

        token = create_access_token(identity=admin_user.id)
        print("\n✅ Token criado para admin")

        # Testar endpoint
        with app.test_client() as client:
            print("\n🔐 Testando endpoint protegido...")
            response = client.get(
                "/users/", headers={"Authorization": f"Bearer {token}"}
            )
            print(f"   Status: {response.status_code}")
            print(f"   Resposta: {response.get_json()}")


if __name__ == "__main__":
    try:
        test_corrections()
    except Exception as e:
        print(f"❌ Erro: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
