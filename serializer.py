from marshmallow import Schema, fields


class OutletSchema(Schema):
	name = fields.Str()
	postal_address = fields.Str()