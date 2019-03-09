from flask import url_for
from flask_login import login_user

from app import db
from app.bps.api import api
from app.bps.api.result.json_result import JSONResult, json_result, ResultCode
from app.bps.main.form import StudentLoginForm, StudentSignUpForm
from app.model.user import Student


@api.route("/auth/login", methods=("POST",))
@json_result
def login():
    form = StudentLoginForm()

    if form.validate_on_submit():

        stu: Student = Student.query.filter_by(stu_code=form.code.data).first()

        if not stu:
            return JSONResult(ResultCode.USER_NOT_EXISTS)
        else:
            pwd = form.password.data or form.code.data

            if stu.verify_password(pwd):
                login_user(stu, remember=form.remember_me.data)
                return JSONResult()

            return JSONResult(ResultCode.INCORRECT_PASSWORD)

    return JSONResult(ResultCode.INVALID_FORM, data=form.errors)


@api.route('/auth/signup', methods=("POST",))
@json_result
def signup():
    form = StudentSignUpForm()

    if form.validate_on_submit():
        login_url = url_for('main.login_page')

        with db.session.begin_nested():
            exists = Student.query.filter_by(stu_code=form.code.data).count()

            if not exists:
                stu = Student(form.name.data, form.code.data, form.password.data)
                db.session.add(stu)

                return JSONResult(ResultCode.OK, data={'login_url': login_url})

        return JSONResult(ResultCode.ALREADY_REGISTERED, data={'login_url': login_url})

    return JSONResult(ResultCode.INVALID_FORM, data=form.errors)
