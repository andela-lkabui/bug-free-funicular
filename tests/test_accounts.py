import json

from test_base import TestBase
from models import User, Accounts


class TestAccount(TestBase):
    """Test CRUD operations and their respective permissions."""

    fixtures = ['user.json', 'accounts.json']

    def test_successful_account_creation(self):
        """
        Tests successful creation of an account.
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
        # create the account
        data = {
            'name': self.fake.name(),
            'phone_no': self.fake.phone_number(),
            'account_no': self.fake.postalcode_plus4(),
            'account_provider': self.fake.name()
        }
        headers = {
            'username': token
        }
        response = self.client.post('/accounts/', data=data, headers=headers)
        self.assertEqual(response.status, '201 CREATED')
        self.assertEqual(response.status_code, 201)
        # fetch account from DB and confirm logged in user is owner
        ac = Accounts.query.filter_by(name=data.get('name')).first()
        self.assertEqual(ac.user.username, user.get('username'))
        # import ipdb; ipdb.set_trace()

    def test_account_creation_without_authentication(self):
        """
        Test attempt to create Account when request is not authenticated.
        """
        data = {
            'name': self.fake.name(),
            'phone_no': self.fake.phone_number(),
            'account_no': self.fake.postalcode_plus4(),
            'account_provider': self.fake.name()
        }
        response = self.client.post('/accounts/', data=data)
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        # fetch account from DB and confirm logged in user is owner
        ac = Accounts.query.filter_by(name=data.get('name')).first()
        self.assertFalse(ac)

    def test_account_creation_without_account_name(self):
        """
        Test attempt to create a new Account when `name` is not provided.
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
        data = {
            'phone_no': self.fake.phone_number(),
            'account_no': self.fake.postalcode_plus4(),
            'account_provider': self.fake.name()
        }
        headers = {
            'username': token
        }
        response = self.client.post('/accounts/', data=data, headers=headers)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(
            response.data,
            'Account name[,\sa-zA-Z]+required',
            msg='Expected `account name ... required` to be part of the\
                error message'
        )
        # Ensure no account object has been persisted to DB
        ac = Accounts.query.filter_by(name=data.get('account_no')).first()
        self.assertFalse(ac)

    def test_account_creation_without_phone_no(self):
        """
        Test attempt to create a new Account when `phone_no` is not provided.
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
        data = {
            'name': self.fake.name(),
            'account_no': self.fake.postalcode_plus4(),
            'account_provider': self.fake.name()
        }
        headers = {
            'username': token
        }
        response = self.client.post('/accounts/', data=data, headers=headers)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(
            response.data,
            'phone no[,\sa-zA-Z]+required',
            msg='Expected `phone no ... required` to be part of the\
                error message'
        )
        # Ensure no account object has been persisted to DB
        ac = Accounts.query.filter_by(name=data.get('name')).first()
        self.assertFalse(ac)

    def test_account_creation_without_account_num(self):
        """
        Test attempt to create a new Account when `account_no` is not provided.
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
        data = {
            'name': self.fake.name(),
            'phone_no': self.fake.phone_number(),
            'account_provider': self.fake.name()
        }
        headers = {
            'username': token
        }
        response = self.client.post('/accounts/', data=data, headers=headers)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(
            response.data,
            'account no[,\sa-zA-Z]+required',
            msg='Expected `account no ... required` to be part of the\
                error message'
        )
        # Ensure no account object has been persisted to DB
        ac = Accounts.query.filter_by(name=data.get('name')).first()
        self.assertFalse(ac)

    def test_account_creation_without_account_provider(self):
        """
        Test attempt to create a new Account when `account_provider` is not
        included.
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
        data = {
            'name': self.fake.name(),
            'phone_no': self.fake.phone_number(),
            'account_no': self.fake.postalcode_plus4()
        }
        headers = {
            'username': token
        }
        response = self.client.post('/accounts/', data=data, headers=headers)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(
            response.data,
            'account provider[,\sa-zA-Z]+required',
            msg='Expected `account provider ... required` to be part of the\
                error message'
        )
        # Ensure no account object has been persisted to DB
        ac = Accounts.query.filter_by(name=data.get('name')).first()
        self.assertFalse(ac)

    def test_account_list_view_with_authenticated_user(self):
        """
        Test response when authenticated user requests list view.
        """
        # user should only see his/her accounts
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
        response = self.client.get('/accounts/', headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data)
        self.assertEqual(len(json_data), 2)
        # fetch account belonging to user-ruby
        ac = Accounts.query.filter_by(user_id=2).first()
        # ensure this account doesn't appear in response
        self.assertNotIn(ac.name, response.data)

    def test_accounts_list_view_without_authentication(self):
        """
        Test response when Account list view is requested without an
        authentication token.
        """
        response = self.client.get('/accounts/')
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertTrue('Unauthenticated request' in response.data)

    def test_accounts_detail_view_with_authenticated_user(self):
        """
        Test response when Account resource detail view is requested by an
        authenticated user.
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
        response = self.client.get('/accounts/1/', headers=headers)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        ac1 = Accounts.query.get(1)
        self.assertTrue(ac1.name in response.data)

    def test_accounts_detail_view_without_authenticated_user(self):
        """
        Test response when Account resource detail view is requested by an
        unauthenticated user.
        """
        response = self.client.get('/accounts/1/')
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertTrue('Unauthenticated request' in response.data)

    def test_accounts_detail_view_authenticated_user_not_owner(self):
        """
        Test response when Account resource detail view is requested and
        account of specified id doesn't belong to current user.
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
        response = self.client.get('/accounts/3/', headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            'Access to account is restricted to owner' in response.data)

    def test_accounts_detail_view_non_existent_account_id(self):
        """
        Test response when Account resource detail view is requested with an id
        that isn't available in the database.
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
        response = self.client.get('/accounts/101/', headers=headers)
        self.assertEqual(response.status, '404 NOT FOUND')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            'Account does not exist' in response.data)

    def test_account_resource_edit_functionality(self):
        """
        Test edit functionality for the account resource.
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
            'phone_no': self.fake.phone_number(),
        }
        ac = Accounts.query.get(1)
        ac_name = ac.name
        response = self.client.put('/accounts/1/', headers=headers, data=data)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        print('=' * 80)
        print('response.data')
        print(response.data)
        print('posted data')
        print(data)
        print('=' * 80)
        self.assertTrue(data.get('name') in response.data)
        self.assertTrue(data.get('phone_no') in response.data)
        ac_edit = Accounts.query.get(1)
        self.assertNotEqual(ac_name, ac_edit.name)

    def test_account_resource_edit_functionality_missing_name(self):
        """
        Test edit functionality for the account resource when the user doesn't
        specify a value for the name parameter.
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
            'phone_no': self.fake.phone_number(),
        }
        response = self.client.put('/accounts/1/', headers=headers, data=data)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Missing parameter data' in response.data)

    def test_account_resource_edit_functionality_not_account_owner(self):
        """
        Test edit functionality for the account resource when the user trying to
        send the edit request is not the owner of the account being edited.
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
            'phone_no': self.fake.phone_number(),
        }
        response = self.client.put('/accounts/1/', headers=headers, data=data)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        self.assertTrue('Access to account is restricted to owner' in response.data)

    def test_account_resource_edit_functionality_account_doesnt_exist(self):
        """
        Test edit functionality for the account resource when the user requests
        to edit an account which doesn't exist in the database.
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
            'phone_no': self.fake.phone_number(),
        }
        # account of id 4 doesn't exist (no fixture where id=4)
        response = self.client.put('/accounts/4/', headers=headers, data=data)
        self.assertEqual(response.status, '404 NOT FOUND')
        self.assertEqual(response.status_code, 404)
        self.assertTrue('Account does not exist' in response.data)

    def test_account_resource_edit_functionality_invalid_auth_token(self):
        """
        Test edit functionality for the account resource when the user sends
        an edit request with an invalid authentication token.
        """
        token = self.fake.sha256()
        headers = {
            'username': token
        }
        data = {
            'name': self.fake.name(),
            'phone_no': self.fake.phone_number(),
        }
        response = self.client.put('/accounts/1/', headers=headers, data=data)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        self.assertTrue('Invalid token' in response.data)

    def test_account_resource_edit_functionality_without_auth_token(self):
        """
        Test edit functionality for the account resource when the user sends
        an edit request without an authentication token.

        The auth token is not provided in the username header.
        """
        data = {
            'phone_no': self.fake.phone_number(),
            'name': self.fake.name()
        }
        response = self.client.put('/accounts/1/', data=data)
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertTrue('Unauthenticated request' in response.data)

    def test_account_resource_delete_functionality(self):
        """
        Test delete functionality for the account resource.
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
        response = self.client.delete('/accounts/1/', headers=headers)
        self.assertEqual(response.status, '204 NO CONTENT')
        self.assertEqual(response.status_code, 204)
        ac = Accounts.query.get(1)
        self.assertFalse(ac)
        response = self.client.get('/accounts/1/', headers=headers)
        self.assertEqual(response.status, '404 NOT FOUND')
        self.assertEqual(response.status_code, 404)

    def test_account_resource_delete_functionality_not_account_owner(self):
        """
        Test delete functionality for the account resource when user sending the
        request to delete an account is not the account owner.
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
        response = self.client.delete('/accounts/1/', headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            'Access to account is restricted to owner' in response.data)
        ac = Accounts.query.get(1)
        self.assertTrue(ac)

    def test_account_resource_delete_functionality_account_doesnt_exist(self):
        """
        Test delete functionality for the account resource when the user requests
        to delete an account that doesn't exist in the database.
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
        # account of id 4 doesn't exist in account fixtures
        response = self.client.delete('/accounts/4/', headers=headers)
        self.assertEqual(response.status, '404 NOT FOUND')
        self.assertEqual(response.status_code, 404)
        self.assertTrue('Account does not exist' in response.data)
        # Confirm account of id 4 doesn't exist in the database
        ac = Accounts.query.get(4)
        self.assertFalse(ac)

    def test_account_resource_delete_functionality_invalid_auth_token(self):
        """
        Test delete functionality for the account resource when the request is
        sent with an invalid token.
        """
        token = self.fake.sha256()
        headers = {
            'username': token
        }
        response = self.client.delete('/accounts/1/', headers=headers)
        self.assertEqual(response.status, '403 FORBIDDEN')
        self.assertEqual(response.status_code, 403)
        self.assertTrue('Invalid token' in response.data)

    def test_account_resource_delete_functionality_without_auth_token(self):
        """
        Test delete functionality for the account resource when the request is
        sent without an authentication token.
        """
        response = self.client.delete('/accounts/1/')
        self.assertEqual(response.status, '401 UNAUTHORIZED')
        self.assertEqual(response.status_code, 401)
        self.assertTrue('Unauthenticated request' in response.data)
