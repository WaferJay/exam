import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import configs


db = SQLAlchemy()
bootstrap = Bootstrap()
lm = LoginManager()


def _load_blueprints(pkgname):

    direct = pkgname.replace(".", "/")
    files = os.listdir(direct)

    bps_pkgs = __import__(pkgname, fromlist=files)

    bps = []

    for pkg_name in dir(bps_pkgs):

        if not pkg_name.startswith("_"):

            pkg = getattr(bps_pkgs, pkg_name)

            if not hasattr(pkg, 'blueprint'):
                continue

            if hasattr(pkg, '__bp_prefix__'):
                prefix = pkg.__bp_prefix__
            else:
                _, prefix = pkg.__name__.rsplit(".", 1)

            bps.append((prefix, pkg.blueprint))

    return bps


def create_app(config_name: str=None):

    if config_name is None:
        env_config_name = os.environ.get("EXAM_CONFIG_NAME")
        config_name = env_config_name or "default"

    app = Flask(__name__)
    app.config.from_object(configs.configs[config_name])

    for prefix, bp in _load_blueprints("app.bps"):
        app.register_blueprint(bp, url_prefix=prefix)

    from app.template_globals import globals_dict
    for name, func in globals_dict.items():
        app.add_template_global(func, name)

    db.init_app(app)
    bootstrap.init_app(app)
    lm.init_app(app)

    return app
