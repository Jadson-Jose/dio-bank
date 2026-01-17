import pytest

from src.app import create_app
from src.models import db, User, Role


@pytest.fixture
def app():
    """Cria uma aplicação Flask para testes"""
    app = create_app(environment="Testing")
    
    with app.app_context():
        # Criar tabelas
        db.create_all()
        
        # Criar dados básicos para testes
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        
        # Criar roles
        admin_role = Role(name='admin')
        user_role = Role(name='user')
        db.session.add_all([admin_role, user_role])
        db.session.commit()  # Commitar para gerar IDs
        
        # Criar usuário admin para autenticação
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin_user = User(
            username='admin', 
            password=hashed_password, 
            role_id=admin_role.id
        )
        db.session.add(admin_user)
        db.session.commit()
        
        yield app
        
        # Limpar
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cria um cliente de teste para a aplicação"""
    return app.test_client()


@pytest.fixture
def access_token(client, app):
    """Obtém um token de acesso para testes"""
    with app.app_context():
        # Fazer login para obter token
        response = client.post('/auth/login', json={
            'username': 'admin',
            'password': 'admin123'
        })
        
        if response.status_code == 200:
            print(f"✅ Token obtido: {response.json.get('access_token')[:30]}...")
            return response.json.get('access_token')
        else:
            print(f"❌ Login falhou: {response.status_code}, {response.json}")
            # Criar um token manualmente para testes
            from flask_jwt_extended import create_access_token
            from src.models import User
            user = User.query.filter_by(username='admin').first()
            if user:
                return create_access_token(identity=user.id)
            return None
