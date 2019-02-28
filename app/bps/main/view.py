from __future__ import absolute_import

from flask import render_template, jsonify
from flask_login import login_user

from app import db
from app.model.user import Student
from app.config import LoginConfigGroup
from . import main
from .form import StudentLoginForm


@main.route("/")
def index():
    return render_template("base.html")


@main.route("/login", methods=("GET",))
def login_page():
    form = StudentLoginForm()
    return render_template("login.html", form=form)


@main.route("/ajax/login", methods=("POST",))
def login():
    form = StudentLoginForm()

    if form.validate_on_submit():

        stu: Student = Student.query.filter_by(stu_code=form.code.data).first()

        if not stu:

            if LoginConfigGroup.auto_create_user:
                stu = Student(form.code.data, form.password.data or form.code.data)
                db.session.add(stu)
                db.session.commit()

                login_user(stu)
                return jsonify(success=True, msg="成功")

            return jsonify(success=False, msg="无此用户")
        else:
            pwd = form.password.data or form.code.data

            if stu.verify_password(pwd):
                login_user(stu)
                return jsonify(success=True, msg="成功")

            return jsonify(success=False, msg="密码错误")

    return jsonify(success=False, msg="表单错误", errors=form.errors)
