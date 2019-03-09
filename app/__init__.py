import logging
import logging.config
import os
from configparser import RawConfigParser

from flask import Flask
from flask.logging import default_handler
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import configs

db = SQLAlchemy()
bootstrap = Bootstrap()
lm = LoginManager()


@lm.user_loader
def _user_loader(uid: str):
    from app.model.user import Admin, Student
    if uid.startswith("admin:"):
        return Admin.query.get(int(uid[6:]))
    else:
        return Student.query.get(int(uid))


lm.login_view = "main.login_page"


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


def load_logging_config(fname, **constants):

    if fname and os.path.exists(fname):
        conf = RawConfigParser()
        conf.read(fname)

        for section in conf.sections():

            for opt, val in conf.items(section, raw=True):
                val = val.format(**constants)
                conf.set(section, opt, val)

            dirs = conf.get(section, 'makedirs', fallback=None)
            if not dirs:
                continue

            dirs = map(lambda e: e.strip(), dirs.split(","))
            dirs = filter(lambda e: not os.path.exists(e), dirs)

            for direct in dirs:
                os.makedirs(direct)

        logging.config.fileConfig(conf)
        return True

    return False


def create_app(config_name: str=None):

    if config_name is None:
        env_config_name = os.environ.get("EXAM_CONFIG_NAME")
        config_name = env_config_name or "default"

    app = Flask(__name__)
    app.config.from_object(configs.configs[config_name])

    log_conf_file = app.config.get('LOGGING_CONFIG_FILE')
    constants = {'APPDIR': app.config['APP_BASE_PATH']}
    if not load_logging_config(log_conf_file, **constants):
        logging.getLogger(__name__).addHandler(default_handler)

    app.logger.debug(f"Config name: {config_name}")

    for prefix, bp in _load_blueprints("app.bps"):
        app.logger.debug(f"Register Blueprint [{bp.name}:{prefix}]")
        app.register_blueprint(bp, url_prefix=prefix)

    from app.template_globals import globals_dict
    for name, func in globals_dict.items():
        app.logger.debug(f"Register template variable: {name}")
        app.add_template_global(func, name)

    db.init_app(app)
    bootstrap.init_app(app)
    lm.init_app(app)

    return app
