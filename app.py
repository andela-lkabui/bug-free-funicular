import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)