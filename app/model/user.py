import datetime

from flask_login import UserMixin

from app import db
from app.util.secret import encrypt_password, verify_password


class Student(db.Model, UserMixin):

    __tablename__ = "student_user"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, default="")
    stu_code = db.Column(db.Integer, nullable=False)
    pwd = db.Column(db.String(36), nullable=False, default="")
    register_time = db.Column(db.Date, nullable=False, default=datetime.date.today)

    def __init__(self, name, code, pwd=None):
        self.name = name
        self.stu_code = code

        if pwd is not None:
            self.password = pwd
        else:
            self.password = self.stu_code

    @property
    def password(self):
        raise AttributeError()

    @password.setter
    def password(self, v):
        self.pwd = encrypt_password(v)

    def verify_password(self, pwd):
        return verify_password(pwd, self.pwd)


class Admin(db.Model, UserMixin):
    __tablename__ = "admin_user"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    pwd = db.Column(db.String(36), nullable=False)

    def __init__(self, name, pwd):
        self.name = name
        self.password = pwd

    @property
    def password(self):
        raise AttributeError()

    @password.setter
    def password(self, v):
        self.pwd = encrypt_password(v)

    def verify_password(self, pwd):
        return verify_password(pwd, self.pwd)
