from flask_wtf import FlaskForm
from wtforms import PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class StudentLoginForm(FlaskForm):
    code = IntegerField("学号", validators=[DataRequired()])
    password = PasswordField("密码")
    submit = SubmitField("登录")
