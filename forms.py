from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

USERNAME_VALIDATORS = [DataRequired(), Length(min=3)]
PASSWORD_VALIDATORS = [DataRequired(), Length(min=4)]

class RegisterForm(FlaskForm):
    username = StringField("username", validators=USERNAME_VALIDATORS)
    password = PasswordField("password", validators=PASSWORD_VALIDATORS)
    password_confirmation = PasswordField(
        "confirm",
        validators=[DataRequired(), EqualTo("password")]
    )

class LoginForm(FlaskForm):
    username = StringField("username", validators=USERNAME_VALIDATORS)
    password = PasswordField("password", validators=PASSWORD_VALIDATORS)