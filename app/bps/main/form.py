from flask_wtf import FlaskForm
from wtforms import PasswordField, IntegerField, BooleanField, StringField
from wtforms.validators import DataRequired, Length


class StudentLoginForm(FlaskForm):
    code = IntegerField("学号", validators=[DataRequired("请填写学号")])
    password = PasswordField("密码", validators=[DataRequired("请填写密码")])
    remember_me = BooleanField("记住我")


class StudentSignUpForm(FlaskForm):
    code = IntegerField("学号", validators=[
        DataRequired("请填写学号"),
        Length(6, message="至少为6位数字")
    ])
    name = StringField("姓名", validators=[DataRequired("请填写姓名")])
    password = PasswordField("密码", validators=[
        DataRequired("请填写密码"),
        Length(6, message="密码至少6个字符")
    ])
