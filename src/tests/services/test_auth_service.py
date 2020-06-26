import unittest

from app import app
from mock import patch, Mock
from app.services.auth_service import AuthService


class TestAuthService(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    @patch('app.services.auth_service.requests.get')
    def test_check_admin_token_success(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: {"privilege": True})
        r = AuthService.check_admin_token('fake_token')

        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(r.status_code, 200)

    @patch('app.services.auth_service.requests.get')
    def test_check_admin_token_with_invalid_token(self, mock_get):
        mock_get.return_value = Mock(status_code=401)
        r = AuthService.check_admin_token('invalid_token')

        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(r.status_code, 502)

    @patch('app.services.auth_service.requests.get')
    def test_check_admin_token_not_admin(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: {"privilege": False})
        r = AuthService.check_admin_token('fake_token')

        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(r.status_code, 403)


if __name__ == '__main__':
    unittest.main()
