from flask.ext.wtf import Form
from wtforms import StringField, PasswordField


class SignupForm(Form):
    username = StringField()
    password = PasswordField()
    password2 = PasswordField(label='Confirm Password')