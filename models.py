from flask import current_app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (
            TimedJSONWebSignatureSerializer as Serializer,
            BadSignature, SignatureExpired
    )

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
    necessary = db.Column(db.Boolean)

    def __repr__(self):
        return '<Goods {0}>'.format(self.name)


class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)

    def __repr__(self):
        return '<Services {0}>'.format(self.name)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(
            current_app.config.get('SECRET_KEY'),
            expires_in=expiration
        )
        return s.dumps({'id': self.user_id})

    @staticmethod
    def verify_auth_token(token):
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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship(
        'User',
        backref=db.backref('goodspurchased', lazy='dynamic'))
    good_id = db.column(db.Integer, db.ForeignKey('goods.id'))
    goods = db.relationship(
        'Goods',
        backref=db.backref('goodspurchased', lazy='dynamic'))
    outlet_id = db.column(db.Integer, db.ForeignKey('outlets.id'))
    outlets = db.relationship(
        'Outlets',
        backref=db.backref('goodspurchased', lazy='dynamic'))
    price = db.column(db.Integer)
    purchase_date = db.column(db.DateTime)

    def __repr__(self):
        return '<GoodsPurchased {0}>'.format(self.price)


if __name__ == '__main__':
    ans = input('\n\nProceed to create database? [y|n] \
        \nCaution: Any existing database will be overwritten!\n')
    if ans == 'y':
        db.create_all()
        print('New database created!')
