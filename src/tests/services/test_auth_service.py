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
        self.assertEqual(r.status_code, 200)

    @patch('app.services.auth_service.requests.get')
    def test_check_admin_token_with_invalid_token(self, mock_get):
        with self.assertRaises(AuthenticationError):
            mock_get.side_effect = Mock(status_code=401)
            AuthService.validate_admin_token('invalid_token')

    @patch('app.services.auth_service.requests.get')
    def test_check_admin_token_not_admin(self, mock_get):
        with self.assertRaises(AuthorizationError):
            mock_get.return_value = Mock(status_code=200, json=lambda: {"privilege": False})
            AuthService.validate_admin_token('fake_token_not_admin')


if __name__ == '__main__':
    unittest.main()
