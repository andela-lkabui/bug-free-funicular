import json

from flask_restful import Resource, Api, reqparse

from app import app, db
from models import User

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
                        return json.dumps({'token': decoded}), 200
                    return json.dumps({'message': 'Incorrect password'}), 400
                return json.dumps(
                        {'message': 'Password is required'}
                    ), 400
            return json.dumps({'message': 'User does not exist'}), 400
        return json.dumps({'message': 'Username is required'}), 400