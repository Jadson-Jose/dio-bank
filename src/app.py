import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from src.models import db

migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()


def create_app(environment=None):
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development")

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{environment.title()}Config")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # type: ignore
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    app.bcrypt = bcrypt  # type: ignore

    # Register blueprints
    from src.controllers.auth import bp as auth_bp
    from src.controllers.role import bp as role_bp
    from src.controllers.user import bp as user_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(role_bp)

    return app
