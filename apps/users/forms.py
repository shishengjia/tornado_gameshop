from wtforms_tornado import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

MOBILE_REGEX = "^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\\d{8}$"


class SmsCodeForm(Form):
    mobile = StringField("mobile", validators=[DataRequired(message="请输入手机号"),
                                               Regexp(MOBILE_REGEX, message="请输入合法手机号")])


class LoginFrom(Form):
    mobile = StringField("mobile", validators=[DataRequired(message="请输入手机号"),
                                               Regexp(MOBILE_REGEX, message="请输入合法手机号")])

    password = StringField("password", validators=[DataRequired(message="请输入密码")])


class RegisterForm(Form):
    mobile = StringField("mobile", validators=[DataRequired(message="请输入手机号"),
                                               Regexp(MOBILE_REGEX, message="请输入合法手机号")])

    code = StringField("verify_code", validators=[DataRequired(message="请输入验证码")])
    password = StringField("password", validators=[DataRequired(message="请输入密码")])



