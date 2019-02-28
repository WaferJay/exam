from flask_wtf import FlaskForm
from wtforms import PasswordField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class StudentLoginForm(FlaskForm):
    code = IntegerField("学号", validators=[DataRequired()], description="如: 17121618")
    password = PasswordField("密码", validators=[DataRequired(), Length(6)], description="至少6个字符")
    remember_me = BooleanField("记住我")
    submit = SubmitField("登录")
