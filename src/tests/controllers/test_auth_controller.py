import unittest

import mock
from app import app

from tests.clients import AppServerTestClient
from tests.clients import WebAdminTestClient


class TestVideoController(unittest.TestCase):

    def setUp(self):
        # creates a test client
        app.test_client_class = AppServerTestClient
        self.app_server_client = app.test_client()
        app.test_client_class = WebAdminTestClient
        self.web_admin_client = app.test_client()
        # propagate the exceptions to the test client
        self.app_server_client.testing = True
        self.web_admin_client.testing = True

    @mock.patch('app.services.auth_service.AuthService.validate_app_server', return_value=False)
    def test_app_server_invalid_api_key(self, mock_auth):
        r = self.app_server_client.get('/videos')

        self.assertEqual(mock_auth.call_count, 1)
        self.assertEqual(r.status_code, 401)

    @mock.patch('app.services.auth_service.AuthService.validate_admin_token', return_value=False)
    def test_web_admin_with_invalid_access_token(self, mock_auth):
        r = self.web_admin_client.get('/videos')

        self.assertEqual(mock_auth.call_count, 1)
        self.assertEqual(r.status_code, 401)


if __name__ == '__main__':
    unittest.main()
