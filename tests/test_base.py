import os
import unittest

from faker import Factory

from app import db
from starters import app


class TestBase(unittest.TestCase):
    """Base unittest class to be inherited from by other test classes."""

    def setUp(self):
        """Method to initialize test resources for every test that is run."""
        test_url = os.environ.get('TEST_DATABASE_URL')
        app.config['SQLALCHEMY_DATABASE_URI'] = test_url
        db.create_all()
        self.client = app.test_client()
        self.fake = Factory.create()

    def tearDown(self):
        """Method to destroy/free up test resources once a test is run."""
        db.session.remove()
        db.drop_all()
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        