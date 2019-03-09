from flask import url_for
from flask_login import login_user, current_user, logout_user

from app import db
from app.bps.api import api
from app.bps.api.result.json_result import JSONResult, json_result, ResultCode
from app.bps.main.form import StudentLoginForm, StudentSignUpForm
from app.model.user import Student


@api.route("/auth/login", methods=("POST",))
@json_result
def login():

    if current_user.is_authenticated:
        return JSONResult(ResultCode.ALREADY_LOGGED_IN)

    form = StudentLoginForm()

    if form.validate_on_submit():

        stu: Student = Student.query.filter_by(stu_code=form.code.data).first()

        if not stu:
            return JSONResult(ResultCode.USER_NOT_EXISTS)
        else:
            pwd = form.password.data or form.code.data

            if stu.verify_password(pwd):
                login_user(stu, remember=form.remember_me.data)
                return JSONResult(data={"redirect_to": url_for("main.home_page")})

            return JSONResult(ResultCode.INCORRECT_PASSWORD)

    return JSONResult(ResultCode.INVALID_FORM, data=form.errors)


@api.route('/auth/logout')
@json_result
def logout():
    logout_user()
    return JSONResult()


@api.route('/auth/signup', methods=("POST",))
@json_result
def signup():
    form = StudentSignUpForm()

    if form.validate_on_submit():

        stu = None
        with db.session.begin_nested():
            exists = Student.query.filter_by(stu_code=form.code.data).count()

            if not exists:
                stu = Student(form.name.data, form.code.data, form.password.data)
                db.session.add(stu)

        result = JSONResult()
        if stu:
            login_user(stu)
            result.data['redirect_to'] = url_for('main.home_page')
        else:
            result.code = ResultCode.ALREADY_REGISTERED
            assert result.code == ResultCode.ALREADY_REGISTERED
            result.data['redirect_to'] = url_for('main.login_page')

        return result

    return JSONResult(ResultCode.INVALID_FORM, data=form.errors)
