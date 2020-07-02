import unittest

from app import app
from mock import patch, Mock
from app.services.auth_service import AuthService
from app.exceptions import AuthenticationError, AuthorizationError


class TestAuthService(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    @patch('app.services.auth_service.requests.get')
    def test_check_admin_token_success(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: {"privilege": True})
        r = AuthService.validate_admin_token('fake_token')

        self.assertEqual(mock_get.call_count, 1)
        self.assertTrue(r)

    @patch('app.services.auth_service.requests.get')
    def test_validate_admin_token_with_invalid_token(self, mock_get):
        with self.assertRaises(AuthenticationError):
            mock_get.return_value = Mock(status_code=401)
            AuthService.validate_admin_token('invalid_token')

    @patch('app.services.auth_service.requests.get')
    def test_validate_admin_token_not_admin(self, mock_get):
        with self.assertRaises(AuthorizationError):
            mock_get.return_value = Mock(status_code=200, json=lambda: {"privilege": False})
            AuthService.validate_admin_token('fake_token_not_admin')

    @patch('app.services.auth_service.requests.get')
    def test_validate_app_server_api_key_success(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: {})
        r = AuthService.validate_app_server('fake_api_key')

        self.assertEqual(mock_get.call_count, 1)
        self.assertTrue(r)

    @patch('app.services.auth_service.requests.get')
    def test_validate_app_server_api_key_fail(self, mock_get):
        with self.assertRaises(AuthenticationError):
            mock_get.return_value = Mock(status_code=403)
            AuthService.validate_app_server('fake_api_key')

    def test_validate_app_server_api_key_with_empty_key(self):
        r = AuthService.validate_app_server(None)

        self.assertFalse(r)

    def validate_admin_token_with_empty_token(self):
        r = AuthService.validate_admin_token(None)

        self.assertFalse(r)


if __name__ == '__main__':
    unittest.main()
