import unittest

from mock import patch
from app import app

from tests.clients import AppServerTestClient
from tests.clients import WebAdminTestClient


class TestVideoController(unittest.TestCase):

    def setUp(self):
        # default client (without auth headers)
        app.test_client_class = None
        self.app_client = app.test_client()
        # app server client
        app.test_client_class = AppServerTestClient
        self.app_server_client = app.test_client()
        # web admin client
        app.test_client_class = WebAdminTestClient
        self.web_admin_client = app.test_client()
        # propagate the exceptions to the test client
        self.app_server_client.testing = True
        self.web_admin_client.testing = True
        self.app_client.testing = True

    @patch('app.services.auth_service.AuthService.validate_app_server', return_value=False)
    def test_app_server_invalid_api_key_on_get_videos(self, mock_auth):
        r = self.app_server_client.get('/videos')

        self.assertEqual(mock_auth.call_count, 1)
        self.assertEqual(r.status_code, 401)

    @patch('app.services.auth_service.AuthService.validate_admin_token', return_value=False)
    def test_web_admin_with_invalid_access_token_on_get_videos(self, mock_auth):
        r = self.web_admin_client.get('/videos')

        self.assertEqual(mock_auth.call_count, 1)
        self.assertEqual(r.status_code, 401)

    def test_client_without_auth_headers_on_get_videos(self):
        r = self.app_client.get('/videos')
        self.assertEqual(r.status_code, 401)


if __name__ == '__main__':
    unittest.main()
