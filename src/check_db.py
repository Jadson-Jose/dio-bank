# check_db.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src import create_app
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    # Verifica quais tabelas existem
    from src.models import db

    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    print("📋 Tabelas existentes no banco:")
    for table in tables:
        print(f"  - {table}")

    # Verifica conteúdo
    if "user" in tables:
        from src.models import User

        users = User.query.all()
        print(f"\n👥 Usuários cadastrados: {len(users)}")
        for user in users:
            print(f"  - {user.username} (ID: {user.id})")

    if "role" in tables:
        from src.models import Role

        roles = Role.query.all()
        print(f"\n👑 Roles cadastradas: {len(roles)}")
        for role in roles:
            print(f"  - {role.name} (ID: {role.id})")

    # Verifica o caminho do banco
    print(f"\n📍 Caminho do banco: {app.config['SQLALCHEMY_DATABASE_URI']}")
