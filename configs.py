import os

base_dir, _ = os.path.split(os.path.abspath(__file__))


def _get_path(path, *paths):
    return os.path.join(base_dir, path, *paths)


class BaseConfig:
    SECRET_KEY = "this is a secret key..."
    BOOTSTRAP_SERVE_LOCAL = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + _get_path("db", "develop.db")
    SQLALCHEMY_BINDS = {
        "config": "sqlite:///" + _get_path("db", "config.dev.db")
    }


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + _get_path("db", "product.db")
    SQLALCHEMY_BINDS = {
        "config": "sqlite:///" + _get_path("db", "config.db")
    }


configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": ProductionConfig
}
