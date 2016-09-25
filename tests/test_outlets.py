import json

from test_base import TestBase
from models import Outlets
from restful.resources import db


class TestOutlet(TestBase):
    """Test CRUD operations on Outlet resource."""

    fixtures = ['user.json']

    def create_outlet(self):
        """
        Please, remove this quick fix future Lewis!
        You can do better than this
        """
        name = self.fake.name()
        outlet = Outlets(
            name=name,
            postal_address=self.fake.street_address(),
            location=self.fake.street_name())
        outlet.user_id = 1
        db.session.add(outlet)
        db.session.commit()
        return outlet
        # -----------------------------

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

    def test_outlet_resource_get_detail_functionality_no_authentication(self):
        """
        Test Outlet resource get detail functionality when request is not
        authenticated.
        """
        response = self.client.get('/outlets/1/')
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        response = self.client.get('/outlets/3/')
        self.assertEqual(response.status, '401 UNAUTHORIZED')

    def test_outlet_resource_get_detail_functionality_invalid_token(self):
        """
        Test Outlet resource get detail functionality when invalid
        authentication token is used.
        """
        token = self.fake.sha256()
        headers = {
            'username': token
        }
        response = self.client.get('/outlets/1/', headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)

    def test_outlet_resource_get_detail_functionality_successful(self):
        """
        Test successful request of get detail functionality in Outlets resource.
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
        name = self.create_outlet().name
        response = self.client.get('/outlets/1/', headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(name in response.data)

    def test_outlet_resource_get_detail_no_authentication(self):
        """
        Test attempt to send a get detail request to the outlet resource without
        authentication token.
        """
        self.create_outlet()
        response = self.client.get('/outlets/1/')
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertTrue('Unauthenticated request' in response.data)

    def test_outlet_resource_get_detail_non_existent_outlet_id(self):
        """
        Test attempt to get detail view of Outlet when outlet_id doesn't exist.
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
        response = self.client.get('/outlets/1/', headers=headers)
        self.assertEqual(response.status, '404 NOT FOUND')
        self.assertEqual(response.status_code, 404)

    def test_outlet_resource_get_detail_not_owner(self):
        """
        Test get detail request on Outlet when authenticated user is not the
        owner.
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
        outlet = self.create_outlet()
        response = self.client.get('/outlets/1/', headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        
    def test_outlet_resource_put_successful(self):
        """
        Test successful attempt to edit an outlet with new data.
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
        outlet = self.create_outlet()
        name = outlet.name
        postal_address = outlet.postal_address
        data = {
            'name': self.fake.name(),
            'postal_address': self.fake.street_address()
        }
        response = self.client.put('/outlets/1/', data=data, headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('name') in response.data)
        self.assertTrue(data.get('postal_address') in response.data)
        self.assertFalse(name in response.data)
        self.assertFalse(postal_address in response.data)

    def test_outlet_resource_put_without_name_parameter(self):
        """
        Test the success of a get detail request at Outlet resource without
        providing the `name` parameter.
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
        outlet = self.create_outlet()
        name = outlet.name
        postal_address = outlet.postal_address
        data = {
            'postal_address': self.fake.street_address()
        }
        response = self.client.put('/outlets/1/', data=data, headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('postal_address') in response.data)
        self.assertTrue(name in response.data)
        self.assertFalse(postal_address in response.data)

    def test_outlet_resource_put_without_postal_address_parameter(self):
        """
        Test the success of a get detail request at Outlet resource without
        providing the `postal_address` parameter.
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
        outlet = self.create_outlet()
        name = outlet.name
        postal_address = outlet.postal_address
        data = {
            'name': self.fake.name()
        }
        response = self.client.put('/outlets/1/', data=data, headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('name') in response.data)
        self.assertFalse(name in response.data)
        self.assertTrue(postal_address in response.data)

    def test_outlet_resource_put_without_authentication_token(self):
        """
        Test attempt to a get detail request on Outlets resource without an
        authentication token.
        """
        outlet = self.create_outlet()
        data = {
            'name': self.fake.name(),
            'postal_address': self.fake.street_address()
        }
        response = self.client.put('/outlets/1/', data=data)
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertTrue('Unauthenticated request' in response.data)

    def test_outlet_resource_put_with_invalid_authentication_token(self):
        """
        Test attempt to get detail request in an Outlet resource using an
        invalid authentication token.
        """
        token = self.fake.sha256()
        headers = {
            'username': token
        }
        outlet = self.create_outlet()
        data = {
            'name': self.fake.name(),
            'postal_address': self.fake.street_address()
        }
        response = self.client.put('/outlets/1/', data=data, headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        self.assertTrue('Invalid token' in response.data)

    def test_outlet_resource_put_non_existent_outlet_id(self):
        """
        Test attempt to get detail request of an Outlet when the outlet_id
        specified doesn't exist.
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
            'postal_address': self.fake.street_address()
        }
        response = self.client.put('/outlets/1/', data=data, headers=headers)
        self.assertEqual(response.status, '404 NOT FOUND')
        self.assertEqual(response.status_code, 404)
        self.assertTrue('Outlet does not exist' in response.data)

    def test_outlet_resource_put_not_owner(self):
        """
        Test a put request on Outlet resource when the authenticated user is
        not the owner.
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
        outlet = self.create_outlet()
        data = {
            'name': self.fake.name(),
            'postal_address': self.fake.street_address()
        }
        response = self.client.put('/outlets/1/', data=data, headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        not_edited = Outlets.query.get(1)
        self.assertEqual(outlet.name, not_edited.name)
        self.assertEqual(outlet.postal_address, not_edited.postal_address)

    def test_outlet_resource_delete_successful(self):
        """
        Test for the successful delete of an Outlet.
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
        outlet = self.create_outlet()
        response = self.client.delete('/outlets/1/', headers=headers)
        self.assertEqual(response.status, '204 NO CONTENT')
        self.assertEqual(response.status_code, 204)
        outlet = Outlets.query.get(1)
        self.assertFalse(outlet)

    def test_outlet_resource_delete_no_authentication(self):
        """
        Test attempt to delete an Outlet when authentication token is not
        provided.
        """
        outlet = self.create_outlet()
        outlet_id = outlet.id
        response = self.client.delete('/outlets/1/')
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        exists = Outlets.query.get(outlet_id)
        self.assertTrue(exists)

    def test_outlet_resource_delete_invalid_token(self):
        """
        Test attempt to delete an Outlet when an invalid token has been
        provided.
        """
        token = self.fake.sha256()
        headers = {
            'username': token
        }
        outlet = self.create_outlet()
        outlet_id = outlet.id
        response = self.client.delete('/outlets/1/', headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        exists = Outlets.query.get(outlet_id)
        self.assertTrue(exists)
        self.assertTrue('Invalid token' in response.data)

    def test_outlet_resource_delete_not_owner(self):
        """
        Test attempt to delete a resource when the request to delete is not
        coming from the owner
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
        outlet = self.create_outlet()
        response = self.client.delete('/outlets/1/', headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        outlet_exists = Outlets.query.get(1)
        self.assertTrue(outlet_exists)

    def test_outlet_resource_delete_non_existent_outlet_id(self):
        """
        Test delete on Outlets resource when the outlet_id does not exist.
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
        response = self.client.delete('/outlets/1/', headers=headers)
        self.assertEqual(response.status, '404 NOT FOUND')
        self.assertEqual(response.status_code, 404)