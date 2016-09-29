import json

from flask import request
from flask_restful import Resource, Api, reqparse

from app import app, db
from models import User, Accounts, Outlets, Goods
from serializer import ServicesSchema, AccountsSchema, OutletSchema, GoodsSchema

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
                # check if a user by provided username already s
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


class AccountListResource(Resource):

    def __init__(self):
        """
        Instantiates class instance variables upon object instance creation.
        """
        self.accounts_schema = AccountsSchema()

    def get(self):
        """
        List all accounts belonging to the currently logged in user.
        """
        token = request.headers.get('username')
        if token:
            current_user = User.verify_auth_token(token)
            if current_user:
                all_accounts = Accounts.query.filter_by(
                    user_id=current_user.user_id
                )
                result = self.accounts_schema.dumps(all_accounts, many=True)
                result_dict = json.loads(result.data)
                return result_dict, 200
            return {'message': 'Invalid token'}, 403
        return {'message': 'Unauthenticated request'}, 401

    def post(self):
        """
        Create a new Account where the owner will be the currently logged in
        user.
        """
        token = request.headers.get('username')
        if token:
            current_user = User.verify_auth_token(token)
            if current_user:
                parser = reqparse.RequestParser()
                parser.add_argument('name')
                parser.add_argument('phone_no')
                parser.add_argument('account_no')
                parser.add_argument('account_provider')
                values = parser.parse_args()
                if None not in values.values() and '' not in values.values():
                    account = Accounts(**values)
                    account.user_id = current_user.user_id
                    db.session.add(account)
                    db.session.commit()
                    return {'message': 'Account created'}, 201
                return {
                        'message': 'Account name, phone no, account no\
                        and account provider are all required'
                        }, 400
            return {'message': 'Invalid token'}, 403
        return {'message': 'Unauthenticated request'}, 401


class AccountDetailResource(Resource):
    """
    Class encapsulates restful implementation of the Accounts detail routes.
    """

    def __init__(self):
        """
        Instantiates class instance variables upon object instance creation.
        """
        self.accounts_schema = AccountsSchema()

    def get(self, account_id):
        """
        Returns details of Account whose id is `account_id`.
        """
        token = request.headers.get('username')
        if token:
            current_user = User.verify_auth_token(token)
            if current_user:
                ac = Accounts.query.get(account_id)
                if ac:
                    if ac.user_id == current_user.user_id:
                        result = self.accounts_schema.dumps(ac)
                        result_dict = json.loads(result.data)
                        return result_dict, 200
                    return {
                            'message': 'Access to account is restricted to owner'
                        }, 403
                return {'message': 'Account does not exist'}, 404
            return {'message': 'Invalid token'}, 400
        return {'message': 'Unauthenticated request'}, 401

    def put(self, account_id):
        """
        Updates account of id `account_id` with user provided data.
        """
        token = request.headers.get('username')
        if token:
            current_user = User.verify_auth_token(token)
            if current_user:
                ac = Accounts.query.get(account_id)
                if ac:
                    if ac.user_id == current_user.user_id:
                        if 'phone_no' in request.form and 'name' in request.form:
                            ac.phone_no = request.form.get('phone_no')
                            ac.name = request.form.get('name')
                            db.session.add(ac)
                            db.session.commit()
                            result = self.accounts_schema.dumps(ac)
                            result_dict = json.loads(result.data)
                            return result_dict, 200
                        return {'message': 'Missing parameter data'}, 400
                    return {
                            'message': 'Access to account is restricted to owner'
                        }, 403
                return {'message': 'Account does not exist'}, 404
            return {'message': 'Invalid token'}, 403
        return {'message': 'Unauthenticated request'}, 401

    def delete(self, account_id):
        """
        Deletes Account of id `account_id`.
        """
        token = request.headers.get('username')
        if token:
            current_user = User.verify_auth_token(token)
            if current_user:
                ac = Accounts.query.get(account_id)
                if ac:
                    if ac.user_id == current_user.user_id:
                        db.session.delete(ac)
                        db.session.commit()
                        return {}, 204
                    return {
                            'message': 'Access to account is restricted to owner'
                        }, 403
                return {'message': 'Account does not exist'}, 404
            return {'message': 'Invalid token'}, 403
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


class GoodsListResource(Resource):
    """
    Class encapsulates restful implementation of the Goods list route.
    """

    def __init__(self):
        self.goods_schema = GoodsSchema()

    def get(self):
        token = request.headers.get('username')
        if token:
            current_user = User.verify_auth_token(token)
            if current_user:
                all_goods = Goods.query.filter_by(user_id=current_user.user_id)
                json_result = self.goods_schema.dumps(all_goods, many=True)
                result_dict = json.loads(json_result.data)
                return result_dict, 200
            return {'message': 'Invalid token'}, 403
        return {'message': 'Unauthenticated request'}, 401

    def post(self):
        token = request.headers.get('username')
        if token:
            current_user = User.verify_auth_token(token)
            if current_user:
                parser = reqparse.RequestParser()
                parser.add_argument('name')
                parser.add_argument('price')
                parser.add_argument('necessary')
                values = parser.parse_args()

                if None not in values.values():
                    result = self.goods_schema.load(values)
                    db.session.add(result.data)
                    db.session.commit()

                    json_result = self.goods_schema.dumps(result.data)
                    return json.loads(json_result.data), 201
                return {
                        'message': 'Name, price and necessary fields are' +
                        ' all required'
                        }, 400
            return {'message': 'Invalid token'}, 403
        return {'message': 'Unauthenticated request'}, 401


class GoodsDetailResource(Resource):
    """
    Class encapsulates restful implementation of the Goods detail route.
    """

    def __init__(self):
        self.goods_schema = GoodsSchema()

    def get(self, good_id):
        token = request.headers.get('username')
        if token:
            current_user = User.verify_auth_token(token)
            if current_user:
                get_good = Goods.query.get(good_id)
                if get_good:
                    if get_good.user_id == current_user.user_id:
                        json_result = self.goods_schema.dumps(get_good)
                        return json.loads(json_result.data), 200
                    return {
                        'message': 'Access to good is restricted to owner'
                    }, 403
                feedback = 'Good of id {0} does not exist'.format(good_id)
                return {'message': feedback}, 404
            return {'message': 'Invalid token'}, 403
        return {'message': 'Unauthenticated request'}, 401

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


class OutletsListResource(Resource):
    """
    Class encapsulates restful implementation of the Outlets list route.
    """

    def __init__(self):
        """
        Instantiates class instance variables upon object instance creation.
        """
        self.outlet_schema = OutletSchema()

    def get(self):
        """
        List all outlets created by currently logged in user.
        """
        token = request.headers.get('username')
        if token:
            current_user = User.verify_auth_token(token)
            if current_user:
                all_outlets = Outlets.query.filter_by(user=current_user)
                json_result = self.outlet_schema.dumps(all_outlets, many=True)
                return json_result.data, 200
            return {'message': 'Invalid token'}, 403
        return {'message': 'Unauthenticated request'}, 401

    def post(self):
        """
        Create new outlet where creator will be the currently logged in user.
        """
        token = request.headers.get('username')
        if token:
            current_user = User.verify_auth_token(token)
            if current_user:
                parser = reqparse.RequestParser()
                parser.add_argument('name')
                parser.add_argument('postal_address')
                parser.add_argument('location')
                values = parser.parse_args()
                if None not in values.values() and '' not in values.values():
                    new_outlet = Outlets(**values)
                    new_outlet.user_id = current_user.user_id
                    db.session.add(new_outlet)
                    db.session.commit()
                    return {'message': 'Outlet created'}, 201
                return {
                        'message': 'Name, postal address and location are' +
                        ' all required'
                        }, 400
            return {'message': 'Invalid token'}, 403
        return {'message': 'Unauthenticated request'}, 401


class OutletsDetailResource(Resource):
    """
    Class encapsulates restful implementation of the Outlets detail route.
    """

    def __init__(self):
        """
        Instantiates class instance variables upon object instance creation.
        """
        self.outlet_schema = OutletSchema()

    def get(self, outlet_id):
        """
        Returns details of Outlet whose id is `outlet_id`.
        """
        token = request.headers.get('username')
        if token:
            current_user = User.verify_auth_token(token)
            if current_user:
                one_outlet = Outlets.query.get(outlet_id)
                if one_outlet:
                    if one_outlet.user_id == current_user.user_id:
                        json_result = self.outlet_schema.dumps(one_outlet)
                        return json_result.data, 200
                    return {
                            'message': 'Get operation restricted to owner'
                            }, 403
                return {'message': 'Outlet does not exist'}, 404
                return
            return {'message': 'Invalid token'}, 403
        return {'message': 'Unauthenticated request'}, 401

    def put(self, outlet_id):
        """
        Updates `name` and/or `postal_address` of Outlet whose id is
        `outlet_id`.
        """
        token = request.headers.get('username')
        if token:
            current_user = User.verify_auth_token(token)
            if current_user:
                # get the update data from the client
                parser = reqparse.RequestParser()
                parser.add_argument('name')
                parser.add_argument('postal_address')
                values = parser.parse_args()
                # fetch the object from the DB
                edit_outlet = Outlets.query.get(outlet_id)
                if edit_outlet:
                    if edit_outlet.user_id == current_user.user_id:
                        # update object properties only when new values have been provided
                        # by the client
                        if values.get('name'):
                            edit_outlet.name = values.get('name')
                        if values.get('postal_address'):
                            edit_outlet.postal_address = values.get(
                                'postal_address')
                        db.session.add(edit_outlet)
                        db.session.commit()
                        json_result = self.outlet_schema.dumps(edit_outlet)
                        return json_result.data, 200
                    return {
                            'message': 'Put operation restricted to owner'
                            }, 403
                return {'message': 'Outlet does not exist'}, 404
            return {'message': 'Invalid token'}, 403
        return {'message': 'Unauthenticated request'}, 401

    def delete(self, outlet_id):
        """
        Deletes Outlet whose id is `outlet_id`.
        """
        token = request.headers.get('username')
        if token:
            current_user = User.verify_auth_token(token)
            if current_user:
                del_outlet = Outlets.query.get(outlet_id)
                if del_outlet:
                    if current_user.user_id == del_outlet.user_id:
                        db.session.delete(del_outlet)
                        db.session.commit()
                        return '', 204
                    return {
                            'message': 'Delete operation restricted to owner'
                            }, 403
                return {'message': 'Outlet does not exist'}, 404
            return {'message': 'Invalid token'}, 403
        return {'message': 'Unauthenticated request'}, 401