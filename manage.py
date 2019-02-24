from flask_script import Manager, Shell

from app import create_app, db
from app.model.user import Admin

app = create_app()


def _make_shell_context():
    context = {
        'app': app,
        'db': db
    }

    return context


manager = Manager(app, with_default_commands=None)
manager.add_command("shell", Shell(make_context=_make_shell_context))


@manager.command
def reset_db():
    db.drop_all()
    db.create_all()


@manager.command
def init():
    db.create_all()
    db.create_all(bind="config")

    admin = Admin("admin", "^defAdminPWD$")
    db.session.add(admin)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
