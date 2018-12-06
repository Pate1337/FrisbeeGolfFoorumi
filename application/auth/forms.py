from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(max=144)])
    password = PasswordField("Password", [validators.Length(max=144)])
  
    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.Length(max=144), validators.Length(min=2), validators.InputRequired()])
    password = PasswordField("Password", [
        validators.InputRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(max=144),
        validators.Length(min=5)
        ])
    confirm = PasswordField("Repeat password", [validators.Length(max=144), validators.InputRequired()])
    name = StringField("Name", [validators.Length(max=144), validators.InputRequired()])

    class Meta:
        csrf = False

class ChangePassword(FlaskForm):
    old_password = PasswordField("Old password", [validators.Length(max=144), validators.InputRequired()])
    new_password = PasswordField("New password", [
        validators.InputRequired(),
        validators.EqualTo('confirm', message='New passwords must match'),
        validators.Length(max=144),
        validators.Length(min=5)
        ])
    confirm = PasswordField("Repeat password", [validators.Length(max=144), validators.InputRequired()])

    class Meta:
        csrf = False

class UserInfoForm(FlaskForm):
    username = StringField("Username", [validators.Length(max=144), validators.Length(min=2), validators.InputRequired()])
    name = StringField("Name", [validators.Length(max=144), validators.InputRequired()])

    class Meta:
        csrf = False
