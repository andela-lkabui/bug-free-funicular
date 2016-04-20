import os

from starters import app
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class Outlets(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	postal_address = db.Column(db.String(100))

	def __repr__(self):
		return '<name {0}'.format(self.name)

if __name__ == '__main__':
	ans = input('\n\nProceed to create database? [y|n] \
		\nCaution: Any existing database will be overwritten!\n')
	if ans == 'y':
		db.create_all()
		print('New database created!')
