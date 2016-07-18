import json

from test_base import TestBase
from models import User, Accounts


class TestAccount(TestBase):
    """Test CRUD operations and their respective permissions."""

    fixtures = ['user.json']

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

    def test_account_creation_no_authentication(self):
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

   