import json

from flask import request
from flask_restful import Resource, Api, reqparse

from app import app, db
from models import User, Accounts
from serializer import ServicesSchema

api = Api(app)


class UserResource(Resource):
    """
    Class encapsulates the restful implementation of the User resource.
    """

    def post(self):
        """
        Creates a new user when the `/auth/new` url is requested using a POST
        http method.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        values = parser.parse_args()

        if values.get('username'):
            if values.get('password'):
                # check if a user by provided username already exists
                exists = User.query.filter_by(username=values.get('username')).first()
                if exists:
                    return json.dumps({'message': 'User already exists'}), 400
                user = User(username=values.get('username'))
                user.hash_password(values.get('password'))
                db.session.add(user)
                db.session.commit()
                return json.dumps(
                                {'message': 'User successfully registered'}
                    ), 201
            return json.dumps({'message': 'Password missing'}), 400
        return json.dumps({'message': 'Username missing'}), 400


class LoginResource(Resource):
    """
    Class encapsulates logic involving the authorization processes.
    """

    def get(self):
        """
        Logs out the currently logged in user when the url `/auth/logout/` is
        requested with a get http method.
        """
        user = User.verify_auth_token(request.headers.get('username'))
        if user:
            user.is_active = False
            db.session.add(user)
            db.session.commit()
            return json.dumps({'message': 'User successfully logged out'}), 200
        return json.dumps({'message': 'User is not logged in'}), 400

    def post(self):
        """
        Returns an authentication token when a valid `username` and `password`
        combination is provided by the user.

        The authentication token is required to access protected resources.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        values = parser.parse_args()

        if values.get('username'):
            user = User.query.filter_by(username=values.get('username')).first()
            if user:
                if values.get('password'):
                    if user.verify_password(values.get('password')):
                        token = user.generate_auth_token()
                        decoded = token.decode('ascii')
                        user.is_active = True
                        db.session.add(user)
                        db.session.commit()
                        return {'token': decoded}, 200
                    return json.dumps({'message': 'Incorrect password'}), 400
                return json.dumps(
                        {'message': 'Password is required'}
                    ), 400
            return json.dumps({'message': 'User does not exist'}), 400
        return json.dumps({'message': 'Username is required'}), 400


class AccountResource(Resource):
    """
    Class encapsulates restful implementation of the Accounts resource.
    """

    def post(self):
        """
        Create a new Account where the owner will be the currently logged in
        user.
        """
        current_user = User.verify_auth_token(request.headers.get('username'))
        if current_user:
            parser = reqparse.RequestParser()
            parser.add_argument('name')
            parser.add_argument('phone_no')
            parser.add_argument('account_no')
            parser.add_argument('account_provider')
            values = parser.parse_args()
            account = Accounts(**values)
            account.user_id = current_user.user_id
            db.session.add(account)
            db.session.commit()
            return {'message': 'Account created'}, 201
        return {'message': 'Unauthenticated request'}, 401


class ServicesResource(Resource):
    """
    Class encapsulates restful implementation of the Services resource.
    """

    def __init__(self):
        self.services_schema = ServicesSchema()

    def get(self):
        all_services = Services.query.all()
        json_result = self.services_schema.dumps(all_services, many=True)
        return json_result.data, 200

    def get(self, service_id):
        get_service = Services.query.get(service_id)
        json_result = services_schema.dumps(get_service)
        return json_result.data, 200

    def put(self):
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

    def delete(self):
        del_service = Services.query.get(service_id)
        if del_service:
            db.session.delete(del_service)
            db.session.commit()
            return '', 204
        return json.dumps(not_found), 400

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('price')
        values = parser.parse_args()

        result = self.services_schema.load(values)
        db.session.add(result.data)
        db.session.commit()

        json_result = self.services_schema.dumps(result.data)
        return json_result.data, 201


class GoodsResource(Resource):
    """
    Class encapsulates restful implementation of the Goods resource.
    """

    def __init__(self):
        self.goods_schema = GoodsSchema()

    def get(self):
        all_goods = Goods.query.all()
        json_result = goods_schema.dumps(all_goods, many=True)
        return json_result.data, 200

    def post(self):
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

    def get(self, good_id):
        get_good = Goods.query.get(good_id)
        json_result = goods_schema.dumps(get_good)
        return json_result.data, 200

    def put(self, good_id):
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

    def delete(self, good_id):
        del_good = Goods.query.get(good_id)
        if del_good:
            db.session.delete(del_good)
            db.session.commit()
            return '', 204
        return json.dumps(not_found), 400


class OutletsResource(Resource):
    """
    Class encapsulates restful implementation of the Outlets resource.
    """

    def __init__(self):
        self.outlet_schema = OutletSchema()

    def get(self):
        # list view
        all_outlets = Outlets.query.all()
        json_result = outlet_schema.dumps(all_outlets, many=True)
        return json_result.data, 200

    def post(self):
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

    def get(self, outlet_id):
        one_outlet = Outlets.query.get(outlet_id)
        json_result = outlet_schema.dumps(one_outlet)
        return json_result.data, 200

    def put(self, outlet_id):
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

    def delete(self, outlet_id):
        del_outlet = Outlets.query.get(outlet_id)
        if del_outlet:
            db.session.delete(del_outlet)
            db.session.commit()
            return '', 204
        return json.dumps(not_found), 400