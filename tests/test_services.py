import json

from test_base import TestBase
from models import Services


class TestServices(TestBase):
    """Test CRUD operations on Services resource."""

    fixtures = ['user.json', 'services.json']

    def test_get_list_services_resource_successful(self):
        """
        Test successful retrieval of multiple services.
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
        response = self.client.get('/services/', headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Tempora quam recusandae eos minima' in response.data)
        self.assertTrue('416935' in response.data)
        self.assertTrue(
            'Ipsum rerum illo suscipit tempore a perferendis' in response.data)
        self.assertTrue('470' in response.data)

    def test_get_list_services_resource_no_authentication_token(self):
        """
        Test attempt to retrieve multiple services without providing an
        authentication token.
        """
        response = self.client.get('/services/')
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertFalse('Tempora quam recusandae eos minima' in response.data)
        self.assertFalse('416935' in response.data)
        self.assertTrue('Unauthenticated request' in response.data)

    def test_get_list_services_resource_permissions(self):
        """
        Test attempt to retrieve multiple services when one of them does not
        belong to the currently logged in user.
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
        response = self.client.get('/services/', headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Tempora quam recusandae eos minima' in response.data)
        self.assertTrue('416935' in response.data)
        self.assertTrue(
            'Ipsum rerum illo suscipit tempore a perferendis' in response.data)
        self.assertTrue('470' in response.data)
        self.assertFalse('Reiciendis qui odit tenetur neque' in response.data)
        self.assertFalse('118' in response.data)
        json_response = json.loads(response.data)
        self.assertEqual(len(json_response), 2)

    def test_get_list_services_resource_invalid_token(self):
        """
        Test attempt to retrieve multiple services when the authentication
        token is invalid.
        """
        token = self.fake.sha256()
        headers = {
            'username': token
        }
        response = self.client.get('/services/', headers=headers)
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertFalse('Tempora quam recusandae eos minima' in response.data)
        self.assertFalse('416935' in response.data)
        self.assertFalse(
            'Ipsum rerum illo suscipit tempore a perferendis' in response.data)
        self.assertFalse('470' in response.data)
        self.assertTrue('Invalid token' in response.data)

    def test_post_services_resource_successful(self):
        """
        Test a successful post request on the Services resource.
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
        response = self.client.post('/services/', headers=headers, data=data)
        self.assertEqual(response.status, '201 CREATED')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data.get('name') in response.data)
        str_price = str(data.get('price'))
        self.assertTrue(str_price in response.data)
        created_service = Services.query.filter_by(
            name=data.get('name'), price=data.get('price')).first()
        self.assertTrue(created_service)

    def test_post_services_resource_invalid_authentication_token(self):
        """
        Test a post request on the Services resource when an invalid
        authentication token has been provided.
        """
        token = self.fake.sha256()
        headers = {
            'username': token
        }
        data = {
            'name': self.fake.name(),
            'price': self.fake.random_number()
        }
        response = self.client.post('/services/', headers=headers, data=data)
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data.get('name') in response.data)
        str_price = str(data.get('price'))
        self.assertFalse(str_price in response.data)
        created_service = Services.query.filter_by(
            name=data.get('name'), price=data.get('price')).first()
        self.assertFalse(created_service)

    def test_post_services_resource_no_authentication_token(self):
        """
        Test a post request on the Services resource when the authentication
        token has not been provided.
        """
        data = {
            'name': self.fake.name(),
            'price': self.fake.random_number()
        }
        response = self.client.post('/services/', data=data)
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data.get('name') in response.data)
        str_price = str(data.get('price'))
        self.assertFalse(str_price in response.data)
        created_service = Services.query.filter_by(
            name=data.get('name'), price=data.get('price')).first()
        self.assertFalse(created_service)
        self.assertTrue('Unauthenticated request' in response.data)

    def test_post_services_resource_missing_name_parameter(self):
        """
        Test a post request on the Services resource when the `name` parameter
        has not been provided.
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
        response = self.client.post('/services/', headers=headers, data=data)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(
            response.data,
            'name[,\sa-zA-Z]+required',
            msg='Expected `name ... required` to be part of the\
                error message'
        )
        created_service = Services.query.filter_by(
            price=data.get('price')).first()
        self.assertFalse(created_service)

    def test_post_services_resource_missing_price_parameter(self):
        """
        Test a post request on the Services resource when the `price` parameter
        has not been provided.
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
        response = self.client.post('/services/', headers=headers, data=data)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(
            response.data,
            'price[,\sa-zA-Z]+required',
            msg='Expected `price ... required` to be part of the\
                error message'
        )
        created_service = Services.query.filter_by(
            price=data.get('name')).first()
        self.assertFalse(created_service)