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
