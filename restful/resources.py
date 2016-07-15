import json

from flask_restful import Resource, Api, reqparse

from app import app, db
from models import User

api = Api(app)


class UserResource(Resource):
    """
    Class represents restful implementation of the User resource.
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