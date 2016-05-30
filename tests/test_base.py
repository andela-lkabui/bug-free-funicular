import os
import unittest

from app import app, db


class TestBase(unittest.TestCase):
    """Base unittest class to be inherited from by other test classes."""

    def setUp(self):
        """Method to initialize test resources for every test that is run."""
        test_url = os.environ.get('TEST_DATABASE_URL')
        app.config['SQLALCHEMY_DATABASE_URI'] = test_url
        db.create_all()

    def tearDown(self):
        """Method to destroy/free up test resources once a test is run."""
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        if os.path.exists('tests/test.db'):
            os.remove('tests/test.db')
