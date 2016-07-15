import json

from flask import request
from flask_restful import reqparse
from jinja2 import Environment, PackageLoader

from models import Outlets, Goods, Services, User
from serializer import OutletSchema, GoodsSchema, ServicesSchema
from restful.resources import app, api, db
from restful.resources import (
    UserResource, LoginResource, AccountResource, ServicesResource,
    GoodsResource
    )

not_found = {'detail': 'Not found.'}


@app.route('/')
def hello():
    env = Environment(loader=PackageLoader('app', 'templates'))
    template = env.get_template('home.html')
    return template.render()


@app.route('/outlets/', methods=['GET', 'POST'])
def outlets_list():
    outlet_schema = OutletSchema()
    if request.method == 'GET':
        # list view
        all_outlets = Outlets.query.all()
        json_result = outlet_schema.dumps(all_outlets, many=True)
        return json_result.data, 200

    if request.method == 'POST':
        # specify data fields to look out for from user
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('postal_address')
        values = parser.parse_args()
        # create outlet object from data
        new_outlet = Outlets(**values)
        db.session.add(new_outlet)
        db.session.commit()
        # display details of object just created
        json_result = outlet_schema.dumps(new_outlet)
        return json_result.data, 201


@app.route('/outlets/<outlet_id>/', methods=['GET', 'PUT', 'DELETE'])
def outlets_detail(outlet_id):
    outlet_schema = OutletSchema()
    if request.method == 'GET':
        one_outlet = Outlets.query.get(outlet_id)
        json_result = outlet_schema.dumps(one_outlet)
        return json_result.data, 200

    if request.method == 'PUT':
        # get the update data from the client
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('postal_address')
        values = parser.parse_args()
        # fetch the object from the DB
        edit_outlet = Outlets.query.get(outlet_id)
        if edit_outlet:
            # update object properties only when new values have been provided
            # by the client
            if values.get('name'):
                edit_outlet.name = values.get('name')
            if values.get('postal_address'):
                edit_outlet.postal_address = values.get('postal_address')
            db.session.add(edit_outlet)
            db.session.commit()
            json_result = outlet_schema.dumps(edit_outlet)
            return json_result.data, 200
        return json.dumps(not_found), 400

    if request.method == 'DELETE':
        del_outlet = Outlets.query.get(outlet_id)
        if del_outlet:
            db.session.delete(del_outlet)
            db.session.commit()
            return '', 204
        return json.dumps(not_found), 400

api.add_resource(UserResource, '/auth/new/')
api.add_resource(LoginResource, '/auth/logout/', '/auth/login/')
api.add_resource(AccountResource, '/accounts/')
api.add_resource(ServicesResource, '/services/', '/services/<int:service_id>/')
api.add_resource(GoodsResource, '/goods/', '/goods/<int:good_id>/')

if __name__ == '__main__':
    app.run(debug=True)