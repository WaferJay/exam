import os

base_dir, _ = os.path.split(os.path.abspath(__file__))


def _get_file_path(path, *paths):
    full_path = os.path.join(base_dir, path, *paths)

    file_path, _ = os.path.split(full_path)
    if not os.path.isdir(file_path):
        os.makedirs(file_path)

    return full_path


def _get_dir_path(path, *paths):
    full_path = os.path.join(base_dir, path, *paths)
    if not os.path.isdir(full_path):
        os.makedirs(full_path)

    return full_path


class BaseConfig:
    APP_BASE_PATH = base_dir
    LOGGING_CONFIG_FILE = None
    SECRET_KEY = "this is a secret key..."
    BOOTSTRAP_SERVE_LOCAL = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOGGING_CONFIG_FILE = _get_file_path("resources", "logging.dev.conf")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + _get_file_path("resources/db", "dev", "develop.db")
    SQLALCHEMY_BINDS = {
        "config": "sqlite:///" + _get_file_path("resources/db", "dev", "config.db")
    }


class ProductionConfig(BaseConfig):
    DEBUG = False
    LOGGING_CONFIG_FILE = _get_file_path("resources", "logging.conf")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + _get_file_path("resources/db", "prod", "product.db")
    SQLALCHEMY_BINDS = {
        "config": "sqlite:///" + _get_file_path("resources/db", "prod", "config.db")
    }


configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": ProductionConfig
}
