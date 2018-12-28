
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class UserRegisterForm(FlaskForm):
    mobile = StringField('手机号',validators=[DataRequired()])
    password = StringField('密码',validators=[DataRequired()])
    password2 = StringField('确认密码',validators=[DataRequired(),EqualTo('password','密码不一致')])

class UserLoginForm(FlaskForm):
    mobile = StringField('手机号',validators=[DataRequired()])
    password = StringField('密码', validators=[DataRequired()])