import json

from flask import request
from flask_restful import reqparse
from jinja2 import Environment, PackageLoader

from models import Outlets, Goods, Services, User
from serializer import OutletSchema, GoodsSchema, ServicesSchema
from restful.resources import app, api, db
from restful.resources import UserResource, LoginResource, AccountResource

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


@app.route('/goods/', methods=['GET', 'POST'])
def goods_list():
    goods_schema = GoodsSchema()
    if request.method == 'GET':
        all_goods = Goods.query.all()
        json_result = goods_schema.dumps(all_goods, many=True)
        return json_result.data, 200

    if request.method == 'POST':
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('price')
        parser.add_argument('necessary')
        values = parser.parse_args()

        result = goods_schema.load(values)
        db.session.add(result.data)
        db.session.commit()

        json_result = goods_schema.dumps(result.data)
        return json_result.data, 201


@app.route('/goods/<good_id>/', methods=['GET', 'PUT', 'DELETE'])
def goods_detail(good_id):
    goods_schema = GoodsSchema()
    if request.method == 'GET':
        get_good = Goods.query.get(good_id)
        json_result = goods_schema.dumps(get_good)
        return json_result.data, 200

    if request.method == 'PUT':
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('price')
        parser.add_argument('necessary')
        values = parser.parse_args()
        # fetch the object from the DB
        edit_good = Goods.query.get(good_id)
        if edit_good:
            if values.get('name'):
                edit_good.name = values.get('name')
            if values.get('price'):
                edit_good.price = values.get('price')
            if values.get('necessary') == 'True':
                edit_good.necessary = values.get('necessary')
            db.session.add(edit_good)
            db.session.commit()
            json_result = goods_schema.dumps(edit_good)
            return json_result.data, 200
        return json.dumps(not_found), 400

    if request.method == 'DELETE':
        del_good = Goods.query.get(good_id)
        if del_good:
            db.session.delete(del_good)
            db.session.commit()
            return '', 204
        return json.dumps(not_found), 400


@app.route('/services/', methods=['GET', 'POST'])
def services_list():
    services_schema = ServicesSchema()
    if request.method == 'GET':
        all_services = Services.query.all()
        json_result = services_schema.dumps(all_services, many=True)
        return json_result.data, 200

    if request.method == 'POST':
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('price')
        values = parser.parse_args()

        result = services_schema.load(values)
        db.session.add(result.data)
        db.session.commit()

        json_result = services_schema.dumps(result.data)
        return json_result.data, 201


@app.route('/services/<service_id>/', methods=['GET', 'PUT', 'DELETE'])
def services_detail(service_id):
    services_schema = ServicesSchema()
    if request.method == 'GET':
        get_service = Services.query.get(service_id)
        json_result = services_schema.dumps(get_service)
        return json_result.data, 200

    if request.method == 'PUT':
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('price')
        values = parser.parse_args()
        # fetch the object from the DB
        edit_service = Services.query.get(service_id)
        if edit_service:
            if values.get('name'):
                edit_service.name = values.get('name')
            if values.get('price'):
                edit_service.price = values.get('price')
            db.session.add(edit_service)
            db.session.commit()
            json_result = services_schema.dumps(edit_service)
            return json_result.data, 200
        return json.dumps(not_found), 400

    if request.method == 'DELETE':
        del_service = Services.query.get(service_id)
        if del_service:
            db.session.delete(del_service)
            db.session.commit()
            return '', 204
        return json.dumps(not_found), 400


api.add_resource(UserResource, '/auth/new/')
api.add_resource(LoginResource, '/auth/logout/', '/auth/login/')
api.add_resource(AccountResource, '/accounts/')

if __name__ == '__main__':
    app.run(debug=True)