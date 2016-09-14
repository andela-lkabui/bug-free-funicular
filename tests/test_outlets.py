import json

from test_base import TestBase


class TestOutlet(TestBase):
    """Test CRUD operations on Outlet resource."""

    fixtures = ['user.json']

    def test_successful_outlet_creation(self):
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
            'outlet_name': self.fake.name(),
            'po_box': self.fake.street_address(),
            'location': self.fake.city()
        }
        headers = {
            'username': token
        }
        response = self.client.post('/outlet/', data=data, headers=headers)
        self.assertEqual(response.status, '201 CREATED')
        self.assertEqual(response.status_code, 201)
        # fetch outlet from DB and confirm logged in user is owner
        outlet = Outlets.query.filter_by(
            name=data.get('outlet_name')).first()
        self.assertEqual(outlet.user.username, user.get('username'))
