import json

from test_base import TestBase
from models import Goods


class TestGoods(TestBase):
    """Test CRUD operations on Goods resource."""

    fixtures = ['user.json', 'goods.json']

    def test_get_list_goods_resource_successful(self):
        """
        Test successful retrieval of multiple goods.
        """
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        response = self.client.get('/goods/', headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Silvio Wolf' in response.data)
        self.assertTrue('true' in response.data)
        self.assertTrue('Mr. Lucas Stracke IV' in response.data)
        self.assertTrue('false' in response.data)

    def test_get_list_goods_resource_no_authentication_token(self):
        """
        Test response when a get list request is sent without authentication
        token.
        """
        response = self.client.get('/goods/')
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertTrue('Unauthenticated request' in response.data)

    def test_get_list_goods_resource_not_owner(self):
        """
        Test filtering out of items that do not belong to currently
        authenticated user.
        """
        user = {
            'username': 'ruby',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        response = self.client.get('/goods/', headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data)
        self.assertEqual(len(json_response), 1)
        self.assertFalse('Silvio Wolf' in response.data)
        self.assertFalse('true' in response.data)
        self.assertFalse('Mr. Lucas Stracke IV' in response.data)
        ruby_good = json_response[0]
        self.assertEqual('Mrs. Kaaren Stokes', ruby_good.get('name'))
        self.assertEqual(False, ruby_good.get('necessary'))

    def test_get_list_goods_resource_invalid_token(self):
        """
        Test response to request at get list with invalid authentication token.
        """
        token = self.fake.sha256()
        headers = {
            'username': token
        }
        response = self.client.get('/goods/', headers=headers)
        self.assertTrue(response.status, '403 FORBIDDEN')
        self.assertTrue(response.status, 403)
        self.assertTrue('Invalid token' in response.data)

    def test_post_goods_resource_successful(self):
        """
        Test successful post request on Goods resource.
        """
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        data = {
            'name': self.fake.name(),
            'necessary': self.fake.boolean(),
            'price': self.fake.random_number()
        }
        response = self.client.post('/goods/', data=data, headers=headers)
        self.assertEqual(response.status, '201 CREATED')
        self.assertEqual(response.status_code, 201)
        json_response = json.loads(response.data)
        self.assertTrue(data.get('name') in response.data)
        self.assertEqual(data.get('price'), int(json_response.get('price')))

    def test_post_goods_resource_invalid_authentication_token(self):
        """
        Test post request on Goods resource when the authentication token is
        invalid
        """
        token = self.fake.sha256()
        headers = {
            'username': token
        }
        data = {
            'name': self.fake.name(),
            'necessary': self.fake.boolean(),
            'price': self.fake.random_number()
        }
        response = self.client.post('/goods/', data=data, headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        self.assertTrue('Invalid token' in response.data)

    def test_post_goods_resource_no_authentication_token(self):
        """
        Test post request on Goods resource when authentication token is not
        provided.
        """
        data = {
            'name': self.fake.name(),
            'necessary': self.fake.boolean(),
            'price': self.fake.random_number()
        }
        response = self.client.post('/goods/', data=data)
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertTrue('Unauthenticated request' in response.data)

    def test_post_goods_resource_missing_name_parameter_in_data(self):
        """
        Test post request on Goods resource when name parameter is not
        provided.
        """
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        data = {
            'necessary': self.fake.boolean(),
            'price': self.fake.random_number()
        }
        response = self.client.post('/goods/', data=data, headers=headers)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(
            response.data,
            'Name[,\sa-zA-Z]+required',
            msg='Expected `Name ... required` to be part of the\
                error message'
        )

    def test_post_goods_resource_missing_necessary_parameter_in_data(self):
        """
        Test post request on Goods resource when necessary parameter is not
        provided.
        """
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        data = {
            'name': self.fake.name(),
            'price': self.fake.random_number()
        }
        response = self.client.post('/goods/', data=data, headers=headers)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(
            response.data,
            'necessary[,\sa-zA-Z]+required',
            msg='Expected `necessary ... required` to be part of the\
                error message'
        )

    def test_post_goods_resource_missing_price_parameter_in_data(self):
        """
        Test post request on Goods resource when price parameter is not
        provided.
        """
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        data = {
            'name': self.fake.name(),
            'necessary': self.fake.boolean(),
        }
        response = self.client.post('/goods/', data=data, headers=headers)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(
            response.data,
            'price[,\sa-zA-Z]+required',
            msg='Expected `price ... required` to be part of the\
                error message'
        )

    def test_get_detail_goods_resource_successful(self):
        """
        Test a successful get detail request on Goods resource.
        """
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        response = self.client.get('/goods/1/', headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Silvio Wolf' in response.data)
        json_response = json.loads(response.data)
        self.assertEqual(1, json_response.get('id'))

    def test_get_detail_goods_resource_not_owner(self):
        """
        Test get detail on Goods resource when authenticated request is not
        from owner.
        """
        user = {
            'username': 'ruby',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        response = self.client.get('/goods/1/', headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            'Access to good is restricted to owner' in response.data)
        self.assertFalse('Silvio Wolf' in response.data)

    def test_get_detail_goods_resource_no_authentication_token(self):
        """
        Test get detail on Goods resource when authentication token is not
        included in the header.
        """
        response = self.client.get('/goods/1/')
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertTrue(
            'Unauthenticated request' in response.data)
        self.assertFalse('Silvio Wolf' in response.data)

    def test_get_detail_goods_resource_invalid_auth_token(self):
        """
        Test get detail on Goods resource when authentication token is invalid.
        """
        token = self.fake.sha256()
        headers = {
            'username': token
        }
        response = self.client.get('/goods/1/', headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            'Invalid token' in response.data)
        self.assertFalse('Silvio Wolf' in response.data)

    def test_get_detail_goods_resource_non_existent_good_id(self):
        """
        Test get detail on Goods resource where a good of id 4 does not exist.
        """
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        response = self.client.get('/goods/4/', headers=headers)
        self.assertEqual(response.status, '404 NOT FOUND')
        self.assertEqual(response.status_code, 404)
        self.assertTrue('Good of id 4 does not exist' in response.data)

    def test_put_goods_resource_successful(self):
        """
        Test a successful put resource on the Goods resource.
        """
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        data = {
            'name': self.fake.name(),
            'necessary': self.fake.boolean(),
            'price': self.fake.random_number()
        }
        response = self.client.put('/goods/1/', data=data, headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Silvio Wolf' in response.data)
        edited_good = Goods.query.get(1)
        self.assertEqual(edited_good.name, data.get('name'))

    def test_put_goods_resource_not_owner(self):
        """
        Test a request where Good of good_id does not belong to authenticated
        user.
        """
        user = {
            'username': 'ruby',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        data = {
            'name': self.fake.name(),
            'necessary': self.fake.boolean(),
            'price': self.fake.random_number()
        }
        response = self.client.put('/goods/1/', data=data, headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            'Access to good is restricted to owner' in response.data)
        edited_good = Goods.query.get(1)
        self.assertNotEqual(edited_good.name, data.get('name'))

    def test_put_goods_resource_non_existent_good_id(self):
        """
        Test a put request where Good of id good_id does not exist.
        """
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        data = {
            'name': self.fake.name(),
            'necessary': self.fake.boolean(),
            'price': self.fake.random_number()
        }
        response = self.client.put('/goods/24/', data=data, headers=headers)
        self.assertEqual(response.status, '404 NOT FOUND')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            'Good of id 24 does not exist' in response.data)
        edited_good = Goods.query.get(1)
        self.assertNotEqual(edited_good.name, data.get('name'))

    def test_put_goods_resource_no_authentication_token(self):
        """
        Test a put request where authentication token has not been provided.
        """
        data = {
            'name': self.fake.name(),
            'necessary': self.fake.boolean(),
            'price': self.fake.random_number()
        }
        response = self.client.put('/goods/1/', data=data)
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertTrue(
            'Unauthenticated request' in response.data)
        edited_good = Goods.query.get(1)
        self.assertNotEqual(edited_good.name, data.get('name'))

    def test_put_goods_resource_invalid_authentication_token(self):
        """
        Test a put request where invalid authentication token has been
        provided.
        """
        token = self.fake.sha256()
        headers = {
            'username': token
        }
        data = {
            'name': self.fake.name(),
            'necessary': self.fake.boolean(),
            'price': self.fake.random_number()
        }
        response = self.client.put('/goods/24/', data=data, headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            'Invalid token' in response.data)
        edited_good = Goods.query.get(1)
        self.assertNotEqual(edited_good.name, data.get('name'))

    def test_put_goods_resource_only_name_parameter_provided(self):
        """
        Test a successful put request on the Goods resource when name is the
        only parameter provided.
        """
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        data = {
            'name': self.fake.name()
        }
        unedited_good = Goods.query.get(1)
        necessary = unedited_good.necessary
        price = unedited_good.price
        response = self.client.put('/goods/1/', data=data, headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Silvio Wolf' in response.data)
        edited_good = Goods.query.get(1)
        self.assertEqual(edited_good.name, data.get('name'))
        self.assertEqual(edited_good.necessary, necessary)
        self.assertEqual(edited_good.price, price)

    def test_put_goods_resource_only_necessary_parameter_provided(self):
        """
        Test a successful put request on the Goods resource when necessary is
        the only parameter provided.
        """
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        data = {
            'necessary': self.fake.boolean()
        }
        unedited_good = Goods.query.get(1)
        name = unedited_good.name
        price = unedited_good.price
        response = self.client.put('/goods/1/', data=data, headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Silvio Wolf' in response.data)
        edited_good = Goods.query.get(1)
        self.assertEqual(edited_good.necessary, data.get('necessary'))
        self.assertEqual(edited_good.name, name)
        self.assertEqual(edited_good.price, price)

    def test_put_goods_resource_only_price_parameter_provided(self):
        """
        Test a successful put request on the Goods resource when price is
        the only parameter provided.
        """
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        headers = {
            'username': token
        }
        data = {
            'price': self.fake.random_number()
        }
        unedited_good = Goods.query.get(1)
        name = unedited_good.name
        necessary = unedited_good.necessary
        response = self.client.put('/goods/1/', data=data, headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Silvio Wolf' in response.data)
        edited_good = Goods.query.get(1)
        self.assertEqual(edited_good.price, data.get('price'))
        self.assertEqual(edited_good.name, name)
        self.assertEqual(edited_good.necessary, necessary)