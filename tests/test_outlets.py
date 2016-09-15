import json

from test_base import TestBase
from models import Outlets


class TestOutlet(TestBase):
    """Test CRUD operations on Outlet resource."""

    fixtures = ['user.json']

    def test_outlet_resource_successful_creation(self):
        """
        Tests successful creation of a outlet.
        """
        # login using credentials of the fixtures user
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token = json_data.get('token')
        # create the outlet
        data = {
            'name': self.fake.name(),
            'postal_address': self.fake.street_address(),
            'location': self.fake.city()
        }
        headers = {
            'username': token
        }
        response = self.client.post('/outlets/', data=data, headers=headers)
        self.assertEqual(response.status, '201 CREATED')
        self.assertEqual(response.status_code, 201)
        # fetch outlet from DB and confirm logged in user is owner
        outlet = Outlets.query.filter_by(
            name=data.get('name')).first()
        self.assertEqual(outlet.user.username, user.get('username'))

    def test_outlet_resource_creation_without_authentication(self):
        """
        Test attempt to create Outlet when request is not authenticated.
        """
        data = {
            'name': self.fake.name(),
            'postal_address': self.fake.street_address(),
            'location': self.fake.city()
        }
        response = self.client.post('/outlets/', data=data)
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertTrue('Unauthenticated request' in response.data)
        # fetch outlet from DB and confirm logged in user is owner
        outlet = Outlets.query.filter_by(
            name=data.get('name')).first()
        self.assertFalse(outlet)

    def test_outlet_resource_creation_without_name(self):
        """
        Test attempt to create Outlet without `name` parameter.
        """
        # login using credentials of the fixtures user
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
            'postal_address': self.fake.street_address(),
            'location': self.fake.city()
        }
        response = self.client.post('/outlets/', data=data, headers=headers)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(
            response.data,
            'Name[,\sa-zA-Z]+required',
            msg='Expected `Name ... required` to be part of the\
                error message'
        )
        # fetch outlet from DB and confirm logged in user is owner
        outlet = Outlets.query.filter_by(
            name=data.get('postal_address')).first()
        self.assertFalse(outlet)

    def test_outlet_resource_creation_without_postal_address(self):
        """
        Test attempt to create Outlet without `postal_address` parameter.
        """
        # login using credentials of the fixtures user
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
            'location': self.fake.city()
        }
        response = self.client.post('/outlets/', data=data, headers=headers)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(
            response.data,
            'postal address[,\sa-zA-Z]+required',
            msg='Expected `Name ... required` to be part of the\
                error message'
        )
        # fetch outlet from DB and confirm logged in user is owner
        outlet = Outlets.query.filter_by(
            name=data.get('name')).first()
        self.assertFalse(outlet)

    def test_outlet_resource_creation_without_location(self):
        """
        Test attempt to create Outlet without `location` parameter.
        """
        # login using credentials of the fixtures user
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
            'postal_address': self.fake.street_address()
        }
        response = self.client.post('/outlets/', data=data, headers=headers)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(
            response.data,
            'location[,\sa-zA-Z]+required',
            msg='Expected `Name ... required` to be part of the\
                error message'
        )
        # fetch outlet from DB and confirm logged in user is owner
        outlet = Outlets.query.filter_by(
            name=data.get('name')).first()
        self.assertFalse(outlet)

    def test_outlet_resource_creation_with_invalid_token(self):
        """
        Tests attempt to create an Outlet with an invalid token.
        """
        # login using credentials of the fixtures user
        token = self.fake.sha256()
        # create the outlet
        data = {
            'name': self.fake.name(),
            'postal_address': self.fake.street_address(),
            'location': self.fake.city()
        }
        headers = {
            'username': token
        }
        response = self.client.post('/outlets/', data=data, headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        # fetch outlet from DB and confirm logged in user is owner
        outlet = Outlets.query.filter_by(
            name=data.get('name')).first()
        self.assertFalse(outlet)

    def test_outlet_resource_get_list_functionality(self):
        """
        Test the correct get functionality in the list view of Outlet resource.

        Expect permissions between different users to be taken into account.
        """
        # login first user
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
        # create outlet with first user
        data = {
            'name': self.fake.name(),
            'postal_address': self.fake.street_address(),
            'location': self.fake.city()
        }
        response = self.client.post('/outlets/', data=data, headers=headers) 
        self.assertEqual(response.status, '201 CREATED')
        # login second user
        user2 = {
            'username': 'ruby',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user2)
        self.assertEqual(response.status, '200 OK')
        json_data = json.loads(response.data)
        token2 = json_data.get('token')
        headers2 = {
            'username': token2
        }
        # create another outlet with second user
        data2 = {
            'name': self.fake.name(),
            'postal_address': self.fake.street_address(),
            'location': self.fake.city()
        }
        response = self.client.post('/outlets/', data=data2, headers=headers2)
        self.assertEqual(response.status, '201 CREATED')
        # first user can only access outlet they created
        response = self.client.get('/outlets/', headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertTrue(data.get('name') in response.data)
        self.assertTrue(data2.get('name') not in response.data)
        # second user can only access outlet they created
        # first user can only access outlet they created
        response = self.client.get('/outlets/', headers=headers2)
        self.assertEqual(response.status, '200 OK')
        self.assertTrue(data.get('name') not in response.data)
        self.assertTrue(data2.get('name') in response.data)

    def test_outlet_resource_get_list_functionality_no_authentication(self):
        """
        Test Outlet get list functionality when request is not authenticated.
        """
        response = self.client.get('/outlets/')
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertTrue('Unauthenticated request' in response.data)

    def test_outlet_resource_get_list_functionality_invalid_token(self):
        """
        Test Outlet get list functionality when request is not authenticated.
        """
        token = self.fake.sha256()
        headers = {
            'username': token
        }
        response = self.client.get('/outlets/', headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        self.assertTrue('Invalid token' in response.data)