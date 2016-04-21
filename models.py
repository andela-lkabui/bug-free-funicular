from app import db


class Outlets(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	postal_address = db.Column(db.String(100))

	def __init__(self, name, postal_address):
		self.name = name
		self.postal_address = postal_address

	def __repr__(self):
		return '<Outlets {0}>'.format(self.name)


class Goods(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	price = db.Column(db.Integer)
	necessary = db.Column(db.Boolean)

	def __repr__(self):
		return '<Goods {0}'.format(self.name)


class Services(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	price = db.Column(db.Integer)

	def __repr__(self):
		return '<Services {0}'.format(self.name)


if __name__ == '__main__':
	ans = input('\n\nProceed to create database? [y|n] \
		\nCaution: Any existing database will be overwritten!\n')
	if ans == 'y':
		db.create_all()
		print('New database created!')
