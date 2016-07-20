from marshmallow import Schema, fields, post_load

from models import Goods, Services, Accounts


class OutletSchema(Schema):
    name = fields.Integer()
    name = fields.Str()
    postal_address = fields.Str()


class GoodsSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    price = fields.Str()
    necessary = fields.Boolean()

    @post_load
    def create_good(self, data):
        return Goods(**data)


class ServicesSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    price = fields.Str()

    @post_load
    def create_service(self, data):
        return Services(**data)


class AccountsSchema(Schema):
    name = fields.Str()
    phone_no = fields.Str()
    account_no = fields.Str()
    account_provider = fields.Str()

    @post_load
    def create_service(self, data):
        return Accounts(**data)