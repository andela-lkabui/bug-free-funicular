from test_base import TestBase
from models import User


class TestRegistration(TestBase):
    """Create tests for user registration routes."""

    def test_successful_registration(self):
        """Test successful registration when valid username and password is
        provided."""
        username = self.fake.user_name()
        password = self.fake.password()
        user = {
            'username': username,
            'password': password
        }
        response = self.client.post('/auth/new/', data=user)
        self.assertEqual(response.status, '201 CREATED')
        self.assertEqual(response.status_code, 201)
        # Assert that the record is in the database
        self.assertEqual(User.query.get(1).username, user.get('username'))
        self.assertTrue(b'User successfully registered' in response.data)

    def test_registration_without_password(self):
        """Test registration when password is missing."""
        username = self.fake.user_name()
        user = {
            'username': username,
            'password': None
        }
        response = self.client.post('/auth/new/', data=user)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        # Assert that user has not been created in the database
        self.assertEqual(len(User.query.all()), 0)
        self.assertTrue(b'Password missing' in response.data)

    def test_registration_without_username(self):
        """Test registration when username is missing."""
        password = self.fake.password()
        user = {
            'username': None,
            'password': password
        }
        response = self.client.post('/auth/new/', data=user)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        # Assert that user has not been created in the database
        self.assertEqual(len(User.query.all()), 0)
        self.assertTrue(b'Username missing' in response.data)

    def test_registration_invalid_credentials(self):
        """Test registration when username exists."""
        user = {
            'username': None,
            'password': None
        }
        response = self.client.post('/auth/new/', data=user)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        # Assert that user has not been created in the database
        self.assertEqual(len(User.query.all()), 0)
        self.assertTrue(b'Username missing' in response.data)