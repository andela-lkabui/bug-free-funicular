from flask.ext.wtf import Form
from wtforms import StringField, BooleanField


class SignupForm(Form):
    username = StringField()
    password = StringField()