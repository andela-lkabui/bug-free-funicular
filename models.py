from flask import current_app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (
            TimedJSONWebSignatureSerializer as Serializer,
            BadSignature, SignatureExpired
    )
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import db, app

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Outlets(db.Model):
    """ORM for shopping outlets that sell goods and/or services."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    postal_address = db.Column(db.String(100))
    purchases = db.relationship(
                'GoodsPurchased', backref=db.backref('outlets', lazy='joined'),
                lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    location = db.Column(db.String(100))

    def __init__(self, name, postal_address, location):
        """Custom outlets model constructor."""
        self.name = name
        self.postal_address = postal_address
        self.location = location

    def __repr__(self):
        """Defines custom representation for Outlet model instances."""
        return '<Outlets {0}>'.format(self.name)


class Goods(db.Model):
    """ORM for purchaseable goods."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    necessary = db.Column(db.Boolean)
    purchases = db.relationship(
        'GoodsPurchased', backref='goods', lazy='dynamic')

    def __repr__(self):
        """Defines custom representation for Goods model instances."""
        return '<Goods {0}>'.format(self.name)


class Services(db.Model):
    """ORM for purchaseable services."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)

    def __repr__(self):
        """Defines custom representation for Services model instances."""
        return '<Services {0}>'.format(self.name)


class User(db.Model):
    """ORM for system users."""
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=False)
    purchases = db.relationship(
        'GoodsPurchased', backref='user', lazy='dynamic')
    accounts = db.relationship('Accounts', backref='user', lazy='dynamic')
    outlets = db.relationship('Outlets', backref='user', lazy='dynamic')

    def __repr__(self):
        """Defines custom representation for User model instances."""
        return '<User {0}>'.format(self.username)

    def hash_password(self, password):
        """
        Hashes plain text password argument and saves result to instance
        variable.
        """
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        """
        Returns True if password is verified and False if otherwise.

        Compares the plain text password argument to the hashed password value
        from the database.
        Returns True if comparison matches and False if otherwise.
        """
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        """
        Generates and returns unique authentication token.

        This method generates an authentication token that is used for user
        authentication in this REST API.
        The default expiry time is 600 seconds unless expiry time is explicitly
        specified as the second numerical argument when this method is invoked.
        """
        s = Serializer(
            current_app.config.get('SECRET_KEY'),
            expires_in=expiration
        )
        return s.dumps({'id': self.user_id})

    @staticmethod
    def verify_auth_token(token):
        """
        Verifies validity of the authentication token argument.

        Checks the validity of the authentication token against expiry and
        forgery.
        Returns the user authenticated by the token if its valid. Returns None
        if token is invalid.
        """
        s = Serializer(current_app.config.get('SECRET_KEY'))
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.get(data.get('id'))
        return user


class GoodsPurchased(db.Model):
    """ORM relating goods and services purchased to a user."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    good_id = db.Column(db.Integer, db.ForeignKey('goods.id'))
    outlet_id = db.Column(db.Integer, db.ForeignKey('outlets.id'))
    price = db.Column(db.Integer)
    purchase_date = db.Column(db.DateTime)

    def __repr__(self):
        """Defines custom representation for GoodsPurchased model instances."""
        return '<GoodsPurchased {0}>'.format(self.price)


class Accounts(db.Model):
    """ORM for monetary Accounts."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone_no = db.Column(db.String(25), nullable=False)
    account_no = db.Column(db.String(20), nullable=False)
    account_provider = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
        """Defines custom representation for Accounts model instances."""
        return '<Accounts {0}>'.format(self.name)


if __name__ == '__main__':
    manager.run()
