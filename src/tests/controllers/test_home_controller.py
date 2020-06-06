import unittest

from app import app
from app.version import Version


class TestHome(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_home_version(self):
        response = self.app.get('/')
        self.assertEqual(response.json, {'version': Version.get()})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
