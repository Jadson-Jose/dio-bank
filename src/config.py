import os


class Config:
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # + os.path.join(app.instance_path, "blog.sqlite")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class ProductionConfig(Config):
    SECRET_KEY = "dev"
    DATABASE_URI = "sqlite:///blog.sqlite"
    JWT_SECRET_KEY = "super-secret"


class DevelopmentConfig(Config):
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.sqlite"
    # + os.path.join(app.instance_path, "blog.sqlite")
    JWT_SECRET_KEY = "super-secret"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = "test"
    DATABASE_URI = "sqlite://"
    JWT_SECRET_KEY = "test"
