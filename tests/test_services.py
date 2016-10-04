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