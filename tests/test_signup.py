from test_base import TestBase


class TestSignUp(TestBase):
    """
    Class contains tests to test signup process.
    """

    def test_presence_of_signup_template(self):
        """
        Test presence of signup template with username and password fields and
        signup button.
        """
        response = self.client.get('/signup')
        self.assertEqual(
            response.status,
            '200 OK',
            msg="Expected a status of '200 OK'"
        )
        self.assertEqual(
            response.status_code,
            200,
            msg="Expected a status code of '200'"
        )
        # would have preferred to use the regexp assert
        self.assertIn(
            'name="password"',
            response.data)