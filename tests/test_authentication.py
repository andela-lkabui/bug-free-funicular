from test_base import TestBase


class TestAuth(TestBase):
    """Create tests for authentication routes."""

    fixtures = ['user.json']

    def test_successful_login(self):
        """Test successful login when correct credentials are provided."""
        # User exists in DB (from fixture) with the password "pythonista"
        user = {
            'username': 'pythonista',
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

    def test_login_without_password(self):
        """Test login when password is missing."""
        user = {
            'username': 'pythonista',
            'password': None
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Password is required' in response.data)

    def test_login_without_username(self):
        """Test login when username is missing."""
        user = {
            'username': None,
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Username is required' in response.data)

    def test_login_wrong_password(self):
        """Test login when password is incorrect."""
        user = {
            'username': 'pythonista',
            'password': self.fake.password()
        }
        response = self.client.post('/auth/login/', data=user)
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Incorrect password' in response.data)

    def test_login_non_existent_username(self):
        """Test login when password is incorrect."""
        user = {
            'username': self.fake.user_name(),
            'password': 'pythonista'
        }
        response = self.client.post('/auth/login/', data=user)
        # import ipdb; ipdb.set_trace()
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('User does not exist' in response.data)