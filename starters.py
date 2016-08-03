import json

from flask import request
from flask_restful import reqparse
from jinja2 import Environment, PackageLoader

from models import Outlets, Goods, Services, User
from serializer import OutletSchema, GoodsSchema, ServicesSchema
from restful.resources import app, api, db
from restful.resources import (
    UserResource, LoginResource, AccountListResource, AccountDetailResource,
    ServicesResource, GoodsResource, OutletsResource
    )

not_found = {'detail': 'Not found.'}


@app.route('/')
def hello():
    env = Environment(loader=PackageLoader('app', 'templates'))
    template = env.get_template('home.html')
    return template.render()

api.add_resource(UserResource, '/auth/new/')
api.add_resource(LoginResource, '/auth/logout/', '/auth/login/')
api.add_resource(AccountListResource, '/accounts/')
api.add_resource(AccountDetailResource, '/accounts/<int:account_id>/')
api.add_resource(ServicesResource, '/services/', '/services/<int:service_id>/')
api.add_resource(GoodsResource, '/goods/', '/goods/<int:good_id>/')
api.add_resource(OutletsResource, '/outlets/', '/outlets/<int:outlet_id>/')

if __name__ == '__main__':
    app.run(debug=True)
