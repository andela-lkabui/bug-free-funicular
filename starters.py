from flask import request
from flask_restful import reqparse

from models import Outlets
from serializer import OutletSchema
from app import app, db


@app.route('/')
def hello():
	return 'Welcome home!'


@app.route('/outlets/', methods=['GET', 'POST'])
def outlets():
	if request.method == 'GET':
		return 'Your outlets!'
	if request.method == 'POST':
		# specify data fields to look out for from user
		parser = reqparse.RequestParser()
		parser.add_argument('name', required=True)
		parser.add_argument('postal_address')
		values = parser.parse_args()
		# create outlet object from data
		new_outlet = Outlets(**values)
		db.session.add(new_outlet)
		db.session.commit()
		# display details of object just created
		outlet_schema = OutletSchema()
		json_result = outlet_schema.dumps(new_outlet)
		return json_result.data, 201


@app.route('/outlets/<outlet_id>/', methods=['GET', 'PUT'])
def outlets_detail(outlet_id):
	if request.method == 'GET':
		return 'Outlet of id: {0}!'.format(outlet_id)
	if request.method == 'PUT':
		return 'Detail view for outlets'


@app.route('/expenses')
def expenses():
	return 'Your expenses!'


@app.route('/accounts')
def accounts():
	return 'Your accounts!'

if __name__ == '__main__':
	app.run(debug=True)