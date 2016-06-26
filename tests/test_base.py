import os
import unittest

from faker import Factory
from flask.ext.fixtures import FixturesMixin

from models import db
from starters import app

test_url = os.environ.get('TEST_DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = test_url
app.config['TESTING'] = True

FixturesMixin.init_app(app, db)


class TestBase(unittest.TestCase, FixturesMixin):
    """Base unittest class to be inherited from by other test classes."""

    def setUp(self):
        """Method to initialize test resources for every test that is run."""
        db.create_all()
        self.client = app.test_client()
        self.fake = Factory.create()
        # import ipdb; ipdb.set_trace()
        
    def tearDown(self):
        """Method to destroy/free up test resources once a test is run."""
        db.session.remove()
        db.drop_all()
        test_db_path = test_url[10::]
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
