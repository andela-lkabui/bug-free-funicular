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
